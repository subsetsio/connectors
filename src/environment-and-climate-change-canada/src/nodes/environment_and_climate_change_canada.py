"""Environment and Climate Change Canada — MSC GeoMet OGC API Features.

Two fetch surfaces, chosen per collection by cost:

1. **The OGC API** (`https://api.weather.gc.ca/collections/<id>/items`) for 34 of
   the 35 accepted collections. Responses are GeoJSON FeatureCollections; each
   feature is flattened to one NDJSON row (feature id + properties + geometry)
   and streamed to `<spec_id>.ndjson.gz`.

   The API is Elasticsearch-backed and pages with `offset`/`limit`, so page cost
   is O(offset): measured on `climate-monthly`, offset=10k took 1.6s, offset=100k
   7.8s, offset=500k 42s, and offset=1M timed out. Offset pagination is therefore
   only usable on small collections. Anything above ~50k rows is **partitioned by
   station** instead — property equality filters (`CLIMATE_IDENTIFIER=`,
   `STATION_NUMBER=`, ...) are exact and fast (a full single-station crawl of
   climate-monthly returns 169 rows in 0.6s), and each partition's own offset
   stays shallow. Measured end-to-end: 16-way parallel, climate-monthly's 8570
   stations crawl in ~9 minutes. The station universe for each family comes from
   that family's own `*-stations` collection. `sortby` is rejected by the server
   ("bad sort property"), so keyset pagination is not an option.

   Every partitioned fetch reconciles its row count against the collection's
   unfiltered `numberMatched` and raises on a shortfall — an observation whose
   station is missing from the station registry is invisible to a
   station-partitioned crawl and would otherwise silently hole the table.

2. **The MSC Datamart** (`https://dd.weather.gc.ca/today/climate/observations/`)
   for `climate-daily` alone. At 63.6M rows the OGC API would need ~22h even
   fully parallelised; the Datamart publishes the same data as ~211k stable
   per-station-year CSVs (1840..present, ~12.5GB) that fetch at ~33 files/s at
   16-way concurrency. They stream into one parquet fragment per province, so an
   interrupted run resumes at province granularity via the raw manifest.

No incremental query is used: every run re-pulls the full corpus and overwrites.
The API does support `datetime=start/end` filtering, but our pattern is
whole-source snapshots, and a full re-pull picks up ECCC's frequent retroactive
quality-control revisions for free.
"""

import concurrent.futures as cf
import csv
import io
import json
import os
import re

import pyarrow as pa
from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    raw_parquet_writer,
    raw_writer,
    transient_retry,
)

SLUG = "environment-and-climate-change-canada"
API = "https://api.weather.gc.ca"
DATAMART = "https://dd.weather.gc.ca/today/climate/observations"

PAGE = 10000
# Safety ceiling per pagination loop. The largest partitioned result set is a few
# thousand rows and the largest unpartitioned collection is ~29k, so 200 pages is
# ample headroom. If a collection outgrows it we want a loud failure, not silent
# truncation.
MAX_PAGES = 200
FETCH_WORKERS = 16
# Rows buffered before a parquet row group is flushed. ~100k dict rows of the
# 33-column daily schema is a few hundred MB — well inside a spawn subprocess.
DAILY_BATCH_ROWS = 100_000

# Spec ids lowercase and hyphenate, which is lossy for the three collection ids
# carrying an underscore. Keep the inverse so a fetch fn can recover the true
# collection id from the node id the runtime hands it.
_COLLECTION_BY_SPEC = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}

# collection -> (filter property, station collection, station-id property on it)
#
# Every collection listed here exceeds ~50k rows, the point where offset
# pagination costs more than the station fan-out. Station counts: climate 8570,
# hydrometric 8055, ahccd 1392, ltce 736 virtual stations.
_PARTITIONED = {
    "ahccd-annual": ("station_id__id_station", "ahccd-stations", "station_id__id_station"),
    "ahccd-monthly": ("station_id__id_station", "ahccd-stations", "station_id__id_station"),
    "ahccd-seasonal": ("station_id__id_station", "ahccd-stations", "station_id__id_station"),
    "ahccd-trends": ("station_id__id_station", "ahccd-stations", "station_id__id_station"),
    "climate-monthly": ("CLIMATE_IDENTIFIER", "climate-stations", "CLIMATE_IDENTIFIER"),
    "climate-normals": ("CLIMATE_IDENTIFIER", "climate-stations", "CLIMATE_IDENTIFIER"),
    "hydrometric-annual-peaks": ("STATION_NUMBER", "hydrometric-stations", "STATION_NUMBER"),
    "hydrometric-annual-statistics": ("STATION_NUMBER", "hydrometric-stations", "STATION_NUMBER"),
    "hydrometric-monthly-mean": ("STATION_NUMBER", "hydrometric-stations", "STATION_NUMBER"),
    "ltce-precipitation": ("VIRTUAL_CLIMATE_ID", "ltce-stations", "VIRTUAL_CLIMATE_ID"),
    "ltce-snowfall": ("VIRTUAL_CLIMATE_ID", "ltce-stations", "VIRTUAL_CLIMATE_ID"),
    "ltce-temperature": ("VIRTUAL_CLIMATE_ID", "ltce-stations", "VIRTUAL_CLIMATE_ID"),
}

# A registered station may legitimately hold no observations, but an observation
# whose station is absent from the registry cannot be reached by a
# station-partitioned crawl. Refuse to ship a hole larger than this fraction.
COVERAGE_TOLERANCE = 0.001


# --------------------------------------------------------------------------
# OGC API Features
# --------------------------------------------------------------------------


@transient_retry()
def _items(collection: str, params: dict) -> dict:
    resp = get(
        f"{API}/collections/{collection}/items",
        params={"f": "json", **params},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _row(feature: dict) -> dict:
    """Flatten one GeoJSON feature to a single record.

    Geometry becomes a JSON string rather than a nested object: most collections
    are point stations, where lon/lat are the whole story, and the few polygon
    ones (forecast zones, hurricane error cones) would otherwise force a nested
    coordinate array onto every sibling row. Point coordinates are promoted to
    `longitude`/`latitude` so the common case stays a plain numeric column.
    """
    row: dict = {"feature_id": feature.get("id")}
    row.update(feature.get("properties") or {})
    geom = feature.get("geometry") or None
    if geom:
        row["geometry_type"] = geom.get("type")
        coords = geom.get("coordinates")
        if geom.get("type") == "Point" and isinstance(coords, list) and len(coords) >= 2:
            row["longitude"], row["latitude"] = coords[0], coords[1]
        else:
            row["geometry_json"] = json.dumps(geom, separators=(",", ":"))
    return row


def _crawl(collection: str, params: dict) -> list[dict]:
    """Offset-paginate one (possibly filtered) result set to exhaustion."""
    rows: list[dict] = []
    for page in range(MAX_PAGES):
        doc = _items(collection, {"limit": PAGE, "offset": page * PAGE, **params})
        feats = doc.get("features") or []
        rows.extend(_row(f) for f in feats)
        matched = doc.get("numberMatched")
        if not feats or len(feats) < PAGE:
            return rows
        if matched is not None and len(rows) >= matched:
            return rows
    raise RuntimeError(
        f"{collection}: hit MAX_PAGES={MAX_PAGES} with params={params} "
        f"({len(rows)} rows so far) - the collection outgrew the safety ceiling"
    )


def _number_matched(collection: str) -> int:
    return int(_items(collection, {"limit": 1}).get("numberMatched") or 0)


def _station_ids(station_collection: str, prop: str) -> list[str]:
    ids = {r[prop] for r in _crawl(station_collection, {}) if r.get(prop)}
    if not ids:
        raise RuntimeError(f"{station_collection}: no {prop} values - cannot partition")
    return sorted(ids)


def fetch_collection(node_id: str) -> None:
    """Fetch one OGC API Features collection into `<node_id>.ndjson.gz`."""
    collection = _COLLECTION_BY_SPEC[node_id.removeprefix(f"{SLUG}-")]

    if collection not in _PARTITIONED:
        with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
            for row in _crawl(collection, {}):
                fh.write(json.dumps(row, default=str) + "\n")
        return

    filter_prop, station_collection, station_prop = _PARTITIONED[collection]
    stations = _station_ids(station_collection, station_prop)
    expected = _number_matched(collection)

    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        with cf.ThreadPoolExecutor(FETCH_WORKERS) as pool:
            futures = [
                pool.submit(_crawl, collection, {filter_prop: sid}) for sid in stations
            ]
            for fut in cf.as_completed(futures):
                for row in fut.result():
                    fh.write(json.dumps(row, default=str) + "\n")
                    written += 1

    if expected and written < expected * (1 - COVERAGE_TOLERANCE):
        raise RuntimeError(
            f"{collection}: station-partitioned crawl shipped {written} of {expected} "
            f"rows reported by numberMatched. Observations exist for stations absent "
            f"from {station_collection}; the partition key no longer covers the collection."
        )


# --------------------------------------------------------------------------
# MSC Datamart — climate-daily
# --------------------------------------------------------------------------

# Apache autoindex listing: skip the sort links ("?C=N;O=D") and the parent link.
_HREF = re.compile(r'href="([^"?/][^"]*)"')

DAILY_SCHEMA = pa.schema(
    [
        ("climate_id", pa.string()),
        ("station_name", pa.string()),
        ("province_code", pa.string()),
        ("date", pa.string()),
        ("year", pa.int32()),
        ("month", pa.int32()),
        ("day", pa.int32()),
        ("longitude", pa.float64()),
        ("latitude", pa.float64()),
        ("data_quality", pa.string()),
        ("max_temp", pa.float64()),
        ("max_temp_flag", pa.string()),
        ("min_temp", pa.float64()),
        ("min_temp_flag", pa.string()),
        ("mean_temp", pa.float64()),
        ("mean_temp_flag", pa.string()),
        ("heat_deg_days", pa.float64()),
        ("heat_deg_days_flag", pa.string()),
        ("cool_deg_days", pa.float64()),
        ("cool_deg_days_flag", pa.string()),
        ("total_rain", pa.float64()),
        ("total_rain_flag", pa.string()),
        ("total_snow", pa.float64()),
        ("total_snow_flag", pa.string()),
        ("total_precip", pa.float64()),
        ("total_precip_flag", pa.string()),
        ("snow_on_grnd", pa.float64()),
        ("snow_on_grnd_flag", pa.string()),
        ("dir_of_max_gust", pa.float64()),
        ("dir_of_max_gust_flag", pa.string()),
        # Text, not float: ECCC encodes sub-threshold gusts as the literal "<31",
        # which a numeric column would silently null out.
        ("spd_of_max_gust", pa.string()),
        ("spd_of_max_gust_flag", pa.string()),
    ]
)

_FLOAT_COLS = {f.name for f in DAILY_SCHEMA if f.type == pa.float64()}
_INT_COLS = {f.name for f in DAILY_SCHEMA if f.type == pa.int32()}

# CSV headers carry units and punctuation: "Max Temp (°C)", "Date/Time",
# "Dir of Max Gust (10s deg)". Normalise them onto the schema's names.
_HEADER_ALIASES = {"date_time": "date"}


def _norm_header(h: str) -> str:
    h = re.sub(r"\(.*?\)", "", h)
    h = re.sub(r"[^0-9a-zA-Z]+", "_", h.strip()).strip("_").lower()
    return _HEADER_ALIASES.get(h, h)


@transient_retry()
def _datamart_text(path: str) -> str:
    resp = get(f"{DATAMART}/{path}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    # The archive predates UTF-8: degree signs and the "?" data-quality marker
    # are latin-1.
    return resp.content.decode("latin-1")


def _provinces() -> list[str]:
    listing = _datamart_text("daily/csv/")
    provs = sorted({h.rstrip("/") for h in _HREF.findall(listing) if h.endswith("/")})
    if not provs:
        raise RuntimeError("Datamart daily/csv/ listing exposed no province directories")
    return provs


def _daily_files(province: str) -> list[str]:
    listing = _datamart_text(f"daily/csv/{province}/")
    files = sorted(h for h in _HREF.findall(listing) if h.endswith(".csv"))
    if not files:
        raise RuntimeError(f"Datamart daily/csv/{province}/ listed no CSV files")
    return files


def _parse_daily(text: str, province: str) -> list[dict]:
    reader = csv.reader(io.StringIO(text))
    try:
        header = [_norm_header(h) for h in next(reader)]
    except StopIteration:
        return []
    rows = []
    for raw in reader:
        rec = dict(zip(header, raw))
        row: dict = {"province_code": province}
        for name in DAILY_SCHEMA.names:
            if name == "province_code":
                continue
            val = (rec.get(name) or "").strip()
            if not val:
                row[name] = None
            elif name in _FLOAT_COLS:
                try:
                    row[name] = float(val)
                except ValueError:
                    row[name] = None
            elif name in _INT_COLS:
                try:
                    row[name] = int(val)
                except ValueError:
                    row[name] = None
            else:
                row[name] = val
        rows.append(row)
    return rows


def _fetch_daily_csv(province: str, filename: str) -> list[dict]:
    return _parse_daily(_datamart_text(f"daily/csv/{province}/{filename}"), province)


def fetch_climate_daily(node_id: str) -> None:
    """Stream the Datamart daily archive into one parquet fragment per province.

    Each province commits its own fragment, so a run interrupted by the
    supervisor resumes at province granularity: fragments already committed under
    this run id are skipped and everything else is refetched. The loop never
    returns early of its own accord.
    """
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag
        for frag, meta in list_raw_fragments(node_id, "parquet").items()
        if meta.get("run_id") == run_id
    }

    for province in _provinces():
        if province in done:
            continue
        files = _daily_files(province)
        with raw_parquet_writer(node_id, DAILY_SCHEMA, fragment=province) as writer:
            batch: list[dict] = []
            with cf.ThreadPoolExecutor(FETCH_WORKERS) as pool:
                for rows in pool.map(_fetch_daily_csv, [province] * len(files), files):
                    batch.extend(rows)
                    if len(batch) >= DAILY_BATCH_ROWS:
                        writer.write_table(pa.Table.from_pylist(batch, schema=DAILY_SCHEMA))
                        batch = []
            if batch:
                writer.write_table(pa.Table.from_pylist(batch, schema=DAILY_SCHEMA))


# --------------------------------------------------------------------------
# Specs
# --------------------------------------------------------------------------


def _spec(entity_id: str) -> NodeSpec:
    return NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_climate_daily if entity_id == "climate-daily" else fetch_collection,
        kind="download",
    )


DOWNLOAD_SPECS = [_spec(eid) for eid in ENTITY_IDS]
