"""KNMI Data Platform connector.

Enumeration was done at collect via the CKAN catalog; here we DOWNLOAD the
selected datasets through the open-data file API (chosen mechanism `open_data`):
list a dataset's files, request a per-file presigned S3 URL, fetch the bytes.
Auth is the API key in the `Authorization` header (raw, no "Bearer"); the
presigned download URL itself needs no auth.

Strategy is stateless full re-pull: each dataset here is small (a single latest
snapshot, or a few dozen per-station CSVs), so we re-fetch and overwrite every
run. No watermark/cursor — revisions are picked up for free.

The eight published subsets need five shapes, dispatched by CONFIG[entity].mode:
  - earthquakes        : latest `aantal-aardbevingen-*` JSON, year x magnitude counts
  - stations_latest    : latest station-metadata CSV snapshot
  - homogenization     : per station x variable daily temperature CSVs
  - ice                : per location x year ice-thickness CSVs
  - matrix             : climate-normals wide matrices (metric x period) -> long format
"""
import csv
import fcntl
import io
import json
import os
import tempfile
import time

import pyarrow as pa  # noqa: F401  (kept for parity; raw is ndjson)
from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_ndjson

from constants import ANON_API_KEY, CONFIG, ENTITY_IDS

BASE = "https://api.dataplatform.knmi.nl/open-data/v1"

# Cross-process rate limit for KEYED open-data API calls (file listing + get-url).
# The anonymous key allows ~50 req/min SHARED across all anonymous users; the 8
# download specs run as parallel subprocesses on one runner, so without global
# coordination they burst past the cap and 429. All specs share this runner's
# filesystem, so a file-lock token spacer serializes their keyed calls to ~37/min
# (1.6s apart), leaving headroom under the shared cap. Presigned S3 downloads are
# NOT counted against the KNMI limit and stay unthrottled.
_LOCK_PATH = os.path.join(tempfile.gettempdir(), "knmi_opendata_ratelimit.lock")
_MIN_INTERVAL = 1.6


def _throttle() -> None:
    fd = os.open(_LOCK_PATH, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)  # auto-released if the process dies
        try:
            last = float((os.read(fd, 64) or b"0").decode().strip() or 0)
        except (ValueError, OSError):
            last = 0.0
        wait = last + _MIN_INTERVAL - time.time()
        if wait > 0:
            time.sleep(wait)
        os.lseek(fd, 0, 0)
        os.ftruncate(fd, 0)
        os.write(fd, str(time.time()).encode())
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _api_key() -> str:
    return os.environ.get("KNMI_API_KEY") or ANON_API_KEY


@transient_retry(attempts=8, min_wait=5, max_wait=90)
def _api_get_json(url: str, params: dict | None = None) -> dict:
    _throttle()
    resp = get(url, params=params, headers={"Authorization": _api_key()},
               timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _download_bytes(url: str) -> bytes:
    # Presigned S3 URL — no auth header needed.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _list_files(name: str, version: str, *, max_keys: int = 1000,
                order_by: str = "filename", sorting: str = "asc") -> list[dict]:
    out: list[dict] = []
    token = None
    pages = 0
    while True:
        params = {"maxKeys": max_keys, "orderBy": order_by, "sorting": sorting}
        if token:
            params["nextPageToken"] = token
        data = _api_get_json(f"{BASE}/datasets/{name}/versions/{version}/files", params)
        out.extend(data.get("files", []))
        token = data.get("nextPageToken")
        pages += 1
        if not data.get("isTruncated") or not token:
            break
        if pages > 50:
            raise RuntimeError(f"{name}: file listing exceeded 50 pages — source grew past expectations")
    return out


def _file_bytes(name: str, version: str, filename: str) -> bytes:
    meta = _api_get_json(f"{BASE}/datasets/{name}/versions/{version}/files/{filename}/url")
    return _download_bytes(meta["temporaryDownloadUrl"])


def _num(v):
    """Parse a KNMI numeric cell to float, or None for missing/European-decimal."""
    if v is None:
        return None
    s = str(v).strip().replace(",", ".")
    if s in ("", "-", ".", "NaN", "nan"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


# ---- mode: earthquakes -------------------------------------------------------

def _fetch_earthquakes(name, version, asset):
    files = _list_files(name, version, order_by="created", sorting="desc")
    counts = [f["filename"] for f in files if f["filename"].startswith("aantal-aardbevingen-")]
    if not counts:
        raise RuntimeError(f"{name}: no aantal-aardbevingen-*.json files found")
    latest = max(counts)  # filename carries a sortable timestamp
    doc = json.loads(_file_bytes(name, version, latest))
    rows = []
    for year, bins in doc.get("data", {}).items():
        for mag, cnt in bins.items():
            if mag == "max":  # max magnitude that year — different unit, skip
                continue
            rows.append({
                "year": int(year),
                "magnitude": _num(mag),
                "earthquake_count": int(cnt),
            })
    save_raw_ndjson(rows, asset)


# ---- mode: stations_latest ---------------------------------------------------

def _fetch_stations(name, version, asset):
    files = _list_files(name, version, order_by="lastModified", sorting="desc", max_keys=1)
    if not files:
        raise RuntimeError(f"{name}: no station CSV files found")
    text = _file_bytes(name, version, files[0]["filename"]).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for r in reader:
        r = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
        rows.append({
            "station_id": int(r["stn"]) if r.get("stn") else None,
            "wsi": r.get("wsi") or None,
            "start_date": r.get("startt") or None,
            "stop_date": r.get("stopt") or None,
            "location": r.get("locatie") or None,
            "station_type": r.get("type") or None,
            "height_m": _num(r.get("hoogte")),
            "pos_x": _num(r.get("pos_x")),
            "pos_y": _num(r.get("pos_y")),
            "latitude": _num(r.get("pos_nb")),
            "longitude": _num(r.get("pos_ol")),
        })
    save_raw_ndjson(rows, asset)


# ---- mode: homogenization ----------------------------------------------------

def _fetch_homogenization(name, version, asset):
    files = [f["filename"] for f in _list_files(name, version)
             if f["filename"].endswith(".csv")]
    rows = []
    for fn in files:
        stem = fn[:-4]
        parts = stem.split("-")  # e.g. DeBilt-TG-allversions
        station, variable = parts[0], parts[1]
        text = _file_bytes(name, version, fn).decode("utf-8-sig")
        for r in csv.DictReader(io.StringIO(text)):
            rows.append({
                "station": station,
                "variable": variable,
                "date": (r.get("date") or "").strip() or None,
                "original": _num(r.get("original")),
                "version1": _num(r.get("version1")),
                "version2": _num(r.get("version2")),
            })
    save_raw_ndjson(rows, asset)


# ---- mode: ice ---------------------------------------------------------------

def _fetch_ice(name, version, asset):
    files = [f["filename"] for f in _list_files(name, version)
             if f["filename"].endswith(".csv")]
    rows = []
    for fn in files:
        stem = fn[:-4]
        parts = stem.split("_")  # Friesland_icethickness_2010
        location = parts[0]
        year = int(parts[-1]) if parts[-1].isdigit() else None
        text = _file_bytes(name, version, fn).decode("utf-8-sig")
        for r in csv.DictReader(io.StringIO(text)):
            r = {(k or "").strip(): v for k, v in r.items()}
            rows.append({
                "location": location,
                "year": year,
                "date": (r.get("date") or "").strip() or None,
                "latitude": _num(r.get("latitude")),
                "longitude": _num(r.get("longitude")),
                "water_depth_m": _num(r.get("water_depth[m]")),
                "ice_depth_cm": _num(r.get("ice_depth[cm]")),
                "snow_depth_cm": _num(r.get("snow_depth[cm]")),
                "observer": (r.get("observer") or "").strip() or None,
            })
    save_raw_ndjson(rows, asset)


# ---- mode: matrix (climate normals) ------------------------------------------

def _parse_matrix(text, location):
    """KNMI climate-normals wide matrix -> long rows {location, metric, period, value}.

    Layout: a station-header line, then a `metric, <period labels...>` header,
    then one row per metric with a value per period column. Some files carry
    several such blocks; each `metric,...` line resets the active period set.
    """
    rows = []
    periods = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cells = [c.strip() for c in line.split(",")]
        if cells[0].lower() == "metric":
            periods = cells[1:]
            continue
        if periods is None:
            continue  # still in the station-header preamble
        metric = cells[0]
        if not metric:
            continue
        for period, raw in zip(periods, cells[1:]):
            rows.append({
                "location": location,
                "metric": metric,
                "period": period,
                "value": _num(raw),
            })
    return rows


def _fetch_matrix(name, version, prefix, asset):
    files = [f["filename"] for f in _list_files(name, version)
             if f["filename"].startswith(prefix) and f["filename"].endswith(".csv")]
    if not files:
        raise RuntimeError(f"{name}: no '{prefix}*.csv' data files found")
    rows = []
    for fn in files:
        location = fn[:-4].split("_", 1)[1]  # strip "Normalen_"/"Dagnormalen_"/... prefix token
        text = _file_bytes(name, version, fn).decode("utf-8-sig")
        rows.extend(_parse_matrix(text, location))
    save_raw_ndjson(rows, asset)


# ---- dispatch ----------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id
    entity = node_id[len("knmi-"):]
    cfg = CONFIG[entity]
    name, version, mode = cfg["name"], cfg["version"], cfg["mode"]
    if mode == "earthquakes":
        _fetch_earthquakes(name, version, asset)
    elif mode == "stations_latest":
        _fetch_stations(name, version, asset)
    elif mode == "homogenization":
        _fetch_homogenization(name, version, asset)
    elif mode == "ice":
        _fetch_ice(name, version, asset)
    elif mode == "matrix":
        _fetch_matrix(name, version, cfg["prefix"], asset)
    else:
        raise ValueError(f"unknown mode {mode!r} for {entity}")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"knmi-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# ---- transforms: one published Delta table per subset ------------------------

_SQL = {
    "knmi-aardbevingen-cijfers-1": '''
        SELECT CAST(year AS INTEGER) AS year,
               CAST(magnitude AS DOUBLE) AS magnitude,
               CAST(earthquake_count AS BIGINT) AS earthquake_count
        FROM "{dep}"
        WHERE year IS NOT NULL AND earthquake_count IS NOT NULL
    ''',
    "knmi-waarneemstations-csv-1-0": '''
        SELECT CAST(station_id AS INTEGER) AS station_id,
               wsi, location, station_type,
               TRY_CAST(start_date AS DATE) AS start_date,
               TRY_CAST(stop_date AS DATE) AS stop_date,
               CAST(height_m AS DOUBLE) AS height_m,
               CAST(latitude AS DOUBLE) AS latitude,
               CAST(longitude AS DOUBLE) AS longitude,
               CAST(pos_x AS DOUBLE) AS pos_x,
               CAST(pos_y AS DOUBLE) AS pos_y
        FROM "{dep}"
        WHERE station_id IS NOT NULL
    ''',
    "knmi-homogenization-daily-temperature-principal-stations-netherlands-1-0": '''
        SELECT station, variable,
               CAST(date AS DATE) AS date,
               CAST(original AS DOUBLE) AS original,
               CAST(version1 AS DOUBLE) AS version1,
               CAST(version2 AS DOUBLE) AS version2
        FROM "{dep}"
        WHERE date IS NOT NULL
    ''',
    "knmi-ice-thickness-observations-1-0": '''
        SELECT location,
               CAST(year AS INTEGER) AS year,
               TRY_STRPTIME(date, '%m/%d/%Y')::DATE AS obs_date,
               CAST(latitude AS DOUBLE) AS latitude,
               CAST(longitude AS DOUBLE) AS longitude,
               CAST(water_depth_m AS DOUBLE) AS water_depth_m,
               CAST(ice_depth_cm AS DOUBLE) AS ice_depth_cm,
               CAST(snow_depth_cm AS DOUBLE) AS snow_depth_cm,
               observer
        FROM "{dep}"
        WHERE date IS NOT NULL
    ''',
}

_MATRIX_SQL = '''
    SELECT location, metric, period, CAST(value AS DOUBLE) AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''


def _sql_for(dep_id: str) -> str:
    return _SQL.get(dep_id, _MATRIX_SQL).format(dep=dep_id)


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_sql_for(s.id))
    for s in DOWNLOAD_SPECS
]
