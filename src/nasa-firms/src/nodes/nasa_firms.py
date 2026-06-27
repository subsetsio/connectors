"""NASA FIRMS active-fire detections — MODIS and VIIRS.

Two published subsets, one per sensor family (distinct schemas):
  - nasa-firms-modis-detections  (MODIS Terra+Aqua, brightness/bright_t31, numeric confidence)
  - nasa-firms-viirs-detections  (VIIRS SNPP/NOAA-20/NOAA-21, bright_ti4/bright_ti5, categorical confidence)

Mechanism (from research, chosen = bulk_country_archive):
  Full history comes from per-(source, year) bulk zips at
  https://firms.modaps.eosdis.nasa.gov/data/country/zips/{source}_{year}_all_countries.zip
  Each zip expands to one CSV per country under {source}/{year}/{source}_{year}_{Country}.csv.
  Verified sources: 'modis' (2000-2024) and 'viirs-snpp' (2012-2024). The current
  (open) year is NOT yet archived, so the rolling key-free "recent" 7-day global
  feeds (bulk_active_recent) top up the tail — and they also carry NOAA-20/NOAA-21
  VIIRS, which the yearly archive lacks.

Fetch shape — firehose / year-bucket batches (shape 3). The corpus is multi-GB
(VIIRS SNPP alone is ~200M rows), too large to re-pull whole each run, so each
download node writes one immutable parquet batch per closed archive year plus a
re-fetched "recent" batch:
    nasa-firms-<family>-detections-<year>     (one per closed archive year)
    nasa-firms-<family>-detections-recent     (rolling 7d global, overwritten)
State holds a monotonic `archive_watermark` = highest fully-written closed year;
already-written years are skipped. Raw is written before state advances. There
is NO self-imposed run budget — the loop drains every available year; the
supervisor interrupts/continues if a run nears its CI limit, and the per-batch
raw+state writes make that safe. The transform's dep view glob-unions every
`<spec_id>-*` batch automatically.
"""

import csv
import io
import tempfile
import zipfile
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
    load_state,
    save_state,
)

STATE_VERSION = 1
BASE = "https://firms.modaps.eosdis.nasa.gov"
CHUNK_ROWS = 200_000  # rows per parquet write — bounds peak memory

# --- per-family schemas -------------------------------------------------------
# Measurement columns are floats; everything else is kept as raw strings and
# typed in the transform. `country` is captured from the archive filename and is
# null for the global recent feed. `instrument`/`type` exist in the archive CSVs
# but are absent from the recent feed (nullable handles both).

_MODIS_FLOATS = ["latitude", "longitude", "brightness", "scan", "track", "bright_t31", "frp"]
_MODIS_STRINGS = ["acq_date", "acq_time", "satellite", "instrument", "confidence", "version", "daynight", "type"]
MODIS_SCHEMA = pa.schema(
    [("country", pa.string())]
    + [(c, pa.float64()) for c in _MODIS_FLOATS]
    + [(c, pa.string()) for c in _MODIS_STRINGS]
)

_VIIRS_FLOATS = ["latitude", "longitude", "bright_ti4", "scan", "track", "bright_ti5", "frp"]
_VIIRS_STRINGS = ["acq_date", "acq_time", "satellite", "instrument", "confidence", "version", "daynight", "type"]
VIIRS_SCHEMA = pa.schema(
    [("country", pa.string())]
    + [(c, pa.float64()) for c in _VIIRS_FLOATS]
    + [(c, pa.string()) for c in _VIIRS_STRINGS]
)

# Family config keyed by download spec id. start_year is a documented source
# fact (MODIS Terra from 2000-11; VIIRS SNPP from 2012-01); the END of the range
# is discovered by probing, never hardcoded.
FAMILIES = {
    "nasa-firms-modis-detections": {
        "archive_source": "modis",
        "start_year": 2000,
        "schema": MODIS_SCHEMA,
        "floats": _MODIS_FLOATS,
        "strings": _MODIS_STRINGS,
        "recent": [("modis-c6.1", "MODIS_C6_1")],
    },
    "nasa-firms-viirs-detections": {
        "archive_source": "viirs-snpp",
        "start_year": 2012,
        "schema": VIIRS_SCHEMA,
        "floats": _VIIRS_FLOATS,
        "strings": _VIIRS_STRINGS,
        # VIIRS recent feed spans all three platforms; only SNPP is in the archive.
        "recent": [
            ("suomi-npp-viirs-c2", "SUOMI_VIIRS_C2"),
            ("noaa-20-viirs-c2", "J1_VIIRS_C2"),
            ("noaa-21-viirs-c2", "J2_VIIRS_C2"),
        ],
    },
}


# --- HTTP helpers -------------------------------------------------------------

@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _zip_exists(url: str) -> bool:
    # Cheap existence probe: ask for one byte. 206/200 = present, 404 = absent.
    resp = get(url, headers={"Range": "bytes=0-0"}, timeout=(10.0, 60.0))
    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    return True


# --- parsing ------------------------------------------------------------------

def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _country_from_member(name: str, source: str, year: int) -> str:
    base = name.rsplit("/", 1)[-1]
    if base.endswith(".csv"):
        base = base[:-4]
    prefix = f"{source}_{year}_"
    if base.startswith(prefix):
        base = base[len(prefix):]
    return base.replace("_", " ")


def _rows_to_table(rows: list[dict], fam: dict) -> pa.Table:
    schema = fam["schema"]
    floats = set(fam["floats"])
    data = {}
    for field in schema:
        c = field.name
        if c in floats:
            data[c] = [r.get(c) for r in rows]  # already floats/None
        else:
            data[c] = [r.get(c) for r in rows]
    arrays = [pa.array(data[f.name], type=f.type) for f in schema]
    return pa.Table.from_arrays(arrays, schema=schema)


def _map_row(row: dict, country, fam: dict) -> dict:
    out = {"country": country}
    for c in fam["floats"]:
        out[c] = _to_float(row.get(c))
    for c in fam["strings"]:
        v = row.get(c)
        out[c] = v if (v is not None and v != "") else None
    return out


def _write_reader(writer, reader, country, fam):
    chunk = []
    for row in reader:
        chunk.append(_map_row(row, country, fam))
        if len(chunk) >= CHUNK_ROWS:
            writer.write_table(_rows_to_table(chunk, fam))
            chunk = []
    if chunk:
        writer.write_table(_rows_to_table(chunk, fam))


# --- archive (full history) ---------------------------------------------------

def _discover_archive_years(source: str, start_year: int) -> list[int]:
    """HEAD-probe the (source, year) zip matrix from the documented start year up
    to the current year. Mid-history years all exist, so the first miss near the
    end marks the end of the archive."""
    now_year = datetime.now(timezone.utc).year
    years, misses = [], 0
    for y in range(start_year, now_year + 1):
        url = f"{BASE}/data/country/zips/{source}_{y}_all_countries.zip"
        if _zip_exists(url):
            years.append(y)
            misses = 0
        else:
            misses += 1
            if years and misses >= 2:
                break
    if not years:
        raise RuntimeError(f"no archive zips discovered for source={source} from {start_year}")
    return years


def _fetch_archive_year(spec_id: str, fam: dict, year: int) -> None:
    source = fam["archive_source"]
    url = f"{BASE}/data/country/zips/{source}_{year}_all_countries.zip"
    raw = _get_bytes(url)
    asset = f"{spec_id}-{year}"
    # Spill the zip to a scratch tempfile (zipfile needs a seekable handle) so we
    # don't hold the compressed bytes AND decoded rows in memory at once.
    with tempfile.NamedTemporaryFile(suffix=".zip") as tf:
        tf.write(raw)
        tf.flush()
        del raw
        with zipfile.ZipFile(tf.name) as zf, raw_parquet_writer(asset, schema=fam["schema"]) as writer:
            for member in zf.namelist():
                if not member.endswith(".csv"):
                    continue
                country = _country_from_member(member, source, year)
                with zf.open(member) as fh:
                    text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
                    _write_reader(writer, csv.DictReader(text), country, fam)


# --- recent (current-year tail) ----------------------------------------------

def _fetch_recent(spec_id: str, fam: dict) -> None:
    asset = f"{spec_id}-recent"
    with raw_parquet_writer(asset, schema=fam["schema"]) as writer:
        for dir_name, prefix in fam["recent"]:
            url = f"{BASE}/data/active_fire/{dir_name}/csv/{prefix}_Global_7d.csv"
            text = _get_bytes(url).decode("utf-8", "replace")
            reader = csv.DictReader(io.StringIO(text))
            _write_reader(writer, reader, None, fam)


# --- node entrypoints ---------------------------------------------------------

def _run_family(spec_id: str) -> None:
    fam = FAMILIES[spec_id]
    state = load_state(spec_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "archive_watermark": 0}
    watermark = state.get("archive_watermark", 0)

    for year in _discover_archive_years(fam["archive_source"], fam["start_year"]):
        if year <= watermark:
            continue
        _fetch_archive_year(spec_id, fam, year)   # write raw FIRST
        watermark = year
        state["archive_watermark"] = watermark
        save_state(spec_id, state)                 # then advance state

    # Always refresh the rolling tail (overwrites the single recent batch).
    _fetch_recent(spec_id, fam)


def fetch_modis(node_id: str) -> None:
    _run_family(node_id)


def fetch_viirs(node_id: str) -> None:
    _run_family(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nasa-firms-modis-detections", fn=fetch_modis, kind="download"),
    NodeSpec(id="nasa-firms-viirs-detections", fn=fetch_viirs, kind="download"),
]


# --- transforms — one published Delta table per family ------------------------
# Thin parse-and-type pass over the glob-unioned batches. Year buckets are
# immutable and non-overlapping and the recent feed is distinct-platform, so no
# dedup window is needed. acq_date is a clean YYYY-MM-DD string in every product.

_MODIS_SQL = '''
WITH base AS (
    SELECT *, TRY_CAST(acq_date AS DATE) AS d
    FROM "nasa-firms-modis-detections"
)
SELECT
    country,
    latitude,
    longitude,
    d                                   AS acq_date,
    acq_time,
    CAST(year(d) AS SMALLINT)           AS year,
    satellite,
    instrument,
    TRY_CAST(confidence AS SMALLINT)    AS confidence,
    version,
    brightness,
    bright_t31,
    scan,
    track,
    frp,
    daynight,
    type
FROM base
WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND d IS NOT NULL
'''

_VIIRS_SQL = '''
WITH base AS (
    SELECT *, TRY_CAST(acq_date AS DATE) AS d
    FROM "nasa-firms-viirs-detections"
)
SELECT
    country,
    latitude,
    longitude,
    d                                   AS acq_date,
    acq_time,
    CAST(year(d) AS SMALLINT)           AS year,
    satellite,
    instrument,
    CASE lower(confidence)
        WHEN 'l' THEN 'low'
        WHEN 'n' THEN 'nominal'
        WHEN 'h' THEN 'high'
        ELSE lower(confidence)
    END                                 AS confidence,
    version,
    bright_ti4,
    bright_ti5,
    scan,
    track,
    frp,
    daynight,
    type
FROM base
WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND d IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasa-firms-modis-detections-transform",
        deps=["nasa-firms-modis-detections"],
        sql=_MODIS_SQL,
    ),
    SqlNodeSpec(
        id="nasa-firms-viirs-detections-transform",
        deps=["nasa-firms-viirs-detections"],
        sql=_VIIRS_SQL,
    ),
]
