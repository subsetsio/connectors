"""NYC TLC Trip Record Data connector.

Mechanism (from research): a public CloudFront repository of one Parquet file
per (trip-type, calendar month) at
``https://d37ci6vzurychx.cloudfront.net/trip-data/{type}_tripdata_{YYYY}-{MM}.parquet``
for type in {yellow, green, fhv, fhvhv}, plus a small CSV zone lookup under
``/misc/``. No auth, no documented rate limit.

Scale & shape. The four trip series together are ~600 monthly files / tens of GB
(fhvhv alone is ~0.5GB/month). That is a *firehose*: each download node fetches
every available month for its series, writing one batch parquet per month
(``<node-id>-{YYYY-MM}``) and persisting state after each so a supervisor
interrupt resumes from the last completed month rather than restarting. The
SQL transform glob-unions the per-month batches automatically.

Schema drift is significant and is normalized in the download fn, NOT the
transform — the runtime registers each dep view as a positional
``read_parquet([...])`` (no ``union_by_name``), so every batch file of a series
MUST share an identical schema. Per month we DESCRIBE the source file and build
a ``TRY_CAST`` projection to a fixed canonical column list/type set: yellow's
2009-2010 lat/lon era (``Trip_Pickup_DateTime``/``Fare_Amt`` and no zone ids)
maps onto the 2011+ zone schema with nulls where a column did not exist;
per-year type wobble (``passenger_count`` BIGINT<->DOUBLE, ``airport_fee``
casing/INT<->DOUBLE, ``cbd_congestion_fee`` added 2025, fhv ``dropOff_datetime``
camelCase, fhv ``PUlocationID`` casing) is absorbed by case-insensitive column
matching + explicit casts. Normalization streams through DuckDB so a 0.5GB
fhvhv month never fully materializes in memory.

Refresh: TLC re-issues recent months in place (revisions, the 2022 CSV->Parquet
swap). We always re-fetch the last ``OVERLAP_MONTHS`` available months even if
already completed, overwriting their batch files; older completed months are
skipped via state. State holds completed-month coordinates, never a terminal
flag.
"""

from __future__ import annotations

import datetime
import os
import random
import tempfile
import time

import duckdb
import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

from subsets_utils import (
    NodeSpec,
    get,
    is_transient,
    raw_parquet_writer,
    save_raw_file,
    load_state,
    save_state,
)

BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"
MISC = "https://d37ci6vzurychx.cloudfront.net/misc"

STATE_VERSION = 1
# Re-fetch this many of the most recent available months every run — TLC revises
# recent months in place, so they must not be skipped by the completed-set.
OVERLAP_MONTHS = 2
# Rows per Arrow batch streamed from DuckDB to the parquet writer (bounds RSS on
# the large fhvhv months).
BATCH_ROWS = 200_000

# Per-series config. `floor` is the source's documented first published month
# (a fixed source fact — verified during collect); the latest month is
# discovered each run by probing back from today, so the end is never hardcoded.
# `min_months` is a sanity floor that trips if discovery silently degrades.
SERIES = {
    "yellow_tripdata": {"floor": (2009, 1), "min_months": 180},
    "green_tripdata": {"floor": (2014, 1), "min_months": 120},
    "fhv_tripdata": {"floor": (2015, 1), "min_months": 100},
    "fhvhv_tripdata": {"floor": (2019, 2), "min_months": 70},
}

# Canonical column spec per series: (out_name, duckdb_type, source_name_candidates).
# The first candidate present in the file (case-insensitive) is TRY_CAST to
# duckdb_type and aliased to out_name; absent -> CAST(NULL AS type). This fixes
# the output schema regardless of which source columns a given month carries.
_YELLOW = [
    ("VendorID", "BIGINT", ("VendorID",)),
    ("tpep_pickup_datetime", "TIMESTAMP", ("tpep_pickup_datetime", "Trip_Pickup_DateTime")),
    ("tpep_dropoff_datetime", "TIMESTAMP", ("tpep_dropoff_datetime", "Trip_Dropoff_DateTime")),
    ("passenger_count", "BIGINT", ("passenger_count", "Passenger_Count")),
    ("trip_distance", "DOUBLE", ("trip_distance", "Trip_Distance")),
    ("RatecodeID", "BIGINT", ("RatecodeID", "Rate_Code")),
    ("store_and_fwd_flag", "VARCHAR", ("store_and_fwd_flag", "store_and_forward")),
    ("PULocationID", "BIGINT", ("PULocationID",)),
    ("DOLocationID", "BIGINT", ("DOLocationID",)),
    ("payment_type", "VARCHAR", ("payment_type", "Payment_Type")),
    ("fare_amount", "DOUBLE", ("fare_amount", "Fare_Amt")),
    ("extra", "DOUBLE", ("extra", "surcharge")),
    ("mta_tax", "DOUBLE", ("mta_tax",)),
    ("tip_amount", "DOUBLE", ("tip_amount", "Tip_Amt")),
    ("tolls_amount", "DOUBLE", ("tolls_amount", "Tolls_Amt")),
    ("improvement_surcharge", "DOUBLE", ("improvement_surcharge",)),
    ("total_amount", "DOUBLE", ("total_amount", "Total_Amt")),
    ("congestion_surcharge", "DOUBLE", ("congestion_surcharge",)),
    ("airport_fee", "DOUBLE", ("airport_fee", "Airport_fee")),
    ("cbd_congestion_fee", "DOUBLE", ("cbd_congestion_fee",)),
]
_GREEN = [
    ("VendorID", "BIGINT", ("VendorID",)),
    ("lpep_pickup_datetime", "TIMESTAMP", ("lpep_pickup_datetime",)),
    ("lpep_dropoff_datetime", "TIMESTAMP", ("lpep_dropoff_datetime",)),
    ("store_and_fwd_flag", "VARCHAR", ("store_and_fwd_flag",)),
    ("RatecodeID", "BIGINT", ("RatecodeID",)),
    ("PULocationID", "BIGINT", ("PULocationID",)),
    ("DOLocationID", "BIGINT", ("DOLocationID",)),
    ("passenger_count", "BIGINT", ("passenger_count",)),
    ("trip_distance", "DOUBLE", ("trip_distance",)),
    ("fare_amount", "DOUBLE", ("fare_amount",)),
    ("extra", "DOUBLE", ("extra",)),
    ("mta_tax", "DOUBLE", ("mta_tax",)),
    ("tip_amount", "DOUBLE", ("tip_amount",)),
    ("tolls_amount", "DOUBLE", ("tolls_amount",)),
    ("ehail_fee", "DOUBLE", ("ehail_fee",)),
    ("improvement_surcharge", "DOUBLE", ("improvement_surcharge",)),
    ("total_amount", "DOUBLE", ("total_amount",)),
    ("payment_type", "BIGINT", ("payment_type",)),
    ("trip_type", "BIGINT", ("trip_type",)),
    ("congestion_surcharge", "DOUBLE", ("congestion_surcharge",)),
    ("cbd_congestion_fee", "DOUBLE", ("cbd_congestion_fee",)),
]
_FHV = [
    ("dispatching_base_num", "VARCHAR", ("dispatching_base_num",)),
    ("pickup_datetime", "TIMESTAMP", ("pickup_datetime", "Pickup_DateTime", "Pickup_date")),
    ("dropoff_datetime", "TIMESTAMP", ("dropOff_datetime", "dropoff_datetime", "DropOff_datetime")),
    ("PULocationID", "BIGINT", ("PUlocationID", "PULocationID")),
    ("DOLocationID", "BIGINT", ("DOlocationID", "DOLocationID")),
    ("SR_Flag", "BIGINT", ("SR_Flag",)),
    ("Affiliated_base_number", "VARCHAR", ("Affiliated_base_number", "Affiliated_base_num")),
]
_FHVHV = [
    ("hvfhs_license_num", "VARCHAR", ("hvfhs_license_num",)),
    ("dispatching_base_num", "VARCHAR", ("dispatching_base_num",)),
    ("originating_base_num", "VARCHAR", ("originating_base_num",)),
    ("request_datetime", "TIMESTAMP", ("request_datetime",)),
    ("on_scene_datetime", "TIMESTAMP", ("on_scene_datetime",)),
    ("pickup_datetime", "TIMESTAMP", ("pickup_datetime",)),
    ("dropoff_datetime", "TIMESTAMP", ("dropoff_datetime",)),
    ("PULocationID", "BIGINT", ("PULocationID",)),
    ("DOLocationID", "BIGINT", ("DOLocationID",)),
    ("trip_miles", "DOUBLE", ("trip_miles",)),
    ("trip_time", "BIGINT", ("trip_time",)),
    ("base_passenger_fare", "DOUBLE", ("base_passenger_fare",)),
    ("tolls", "DOUBLE", ("tolls",)),
    ("bcf", "DOUBLE", ("bcf",)),
    ("sales_tax", "DOUBLE", ("sales_tax",)),
    ("congestion_surcharge", "DOUBLE", ("congestion_surcharge",)),
    ("airport_fee", "DOUBLE", ("airport_fee",)),
    ("tips", "DOUBLE", ("tips",)),
    ("driver_pay", "DOUBLE", ("driver_pay",)),
    ("shared_request_flag", "VARCHAR", ("shared_request_flag",)),
    ("shared_match_flag", "VARCHAR", ("shared_match_flag",)),
    ("access_a_ride_flag", "VARCHAR", ("access_a_ride_flag",)),
    ("wav_request_flag", "VARCHAR", ("wav_request_flag",)),
    ("wav_match_flag", "VARCHAR", ("wav_match_flag",)),
    ("cbd_congestion_fee", "DOUBLE", ("cbd_congestion_fee",)),
]
COLSPECS = {
    "yellow_tripdata": _YELLOW,
    "green_tripdata": _GREEN,
    "fhv_tripdata": _FHV,
    "fhvhv_tripdata": _FHVHV,
}


# --- retry policy -----------------------------------------------------------
# CloudFront occasionally returns a transient 403 on a cold object that clears on
# retry, so we retry 403 in addition to the standard transient set (429/5xx/net).
def _retryable(exc: BaseException) -> bool:
    if is_transient(exc):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 403


# CloudFront throttles bursts of small-file requests per-IP with a 403, and the
# throttle window can outlast a short backoff: a cold backfill run pulls ~600
# files across four series that run CONCURRENTLY (each NodeSpec is its own
# subprocess), so the aggregate request rate against one host is ~4x a single
# series' pace and the library exposes no cross-process limiter (feedback filed).
# A prior run hit a sustained ~16min 403 on green 2017-02 (a file that verifiably
# exists) and exhausted a 12-attempt/120s-cap window. So retry 403 over a much
# longer, JITTERED window (~24 attempts, exponential to 300s + random spread ≈
# up to ~1.5h) — the jitter desynchronizes the four concurrent series so their
# retries stop landing in lockstep, and the long tail lets a throttle clear
# mid-retry rather than failing the whole DAG. Interior months of every series
# are contiguous (only the latest edge is probed for existence), so a persistent
# 403 here is always throttle, never a real gap.
_fetch_retry = retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(24),
    wait=wait_exponential(min=4, max=300) + wait_random(0, 10),
    reraise=True,
)

# Minimum spacing between successive month fetches within a series, to keep the
# request rate under CloudFront's burst threshold (the small monthly files
# otherwise fire several per second). Jittered so the four concurrent series
# don't align into synchronized bursts. Cheap insurance against a multi-hour run.
FETCH_PACING_S = 1.0
FETCH_PACING_JITTER_S = 1.0


# --- month helpers ----------------------------------------------------------
def _ym_url(stem: str, y: int, m: int) -> str:
    return f"{BASE}/{stem}_{y:04d}-{m:02d}.parquet"


def _add_month(y: int, m: int, delta: int) -> tuple[int, int]:
    idx = (y * 12 + (m - 1)) + delta
    return idx // 12, idx % 12 + 1


def _probe_present(url: str) -> bool:
    """Cheap existence check via a 2-byte ranged GET. Retries a cold-cache 403 a
    few times before concluding the object is genuinely absent."""
    for attempt in range(4):
        try:
            r = get(url, headers={"Range": "bytes=0-1"}, timeout=(10, 60))
        except Exception as exc:  # network transients only — reraise the rest
            if is_transient(exc) and attempt < 3:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        if r.status_code in (200, 206):
            return True
        if r.status_code == 404:
            return False
        if r.status_code == 403 and attempt < 3:
            time.sleep(1.5)
            continue
        if r.status_code == 403:
            return False
        r.raise_for_status()  # 5xx etc -> let it raise
    return False


def _discover_months(stem: str, floor: tuple[int, int]) -> list[str]:
    """All published months for a series as 'YYYY-MM'. The latest month is found
    by walking back from today (publication lag is ~2 months); the series is
    contiguous from `floor` to that latest month."""
    y, m = datetime.date.today().year, datetime.date.today().month
    latest = None
    for _ in range(15):
        if _probe_present(_ym_url(stem, y, m)):
            latest = (y, m)
            break
        y, m = _add_month(y, m, -1)
    if latest is None:
        raise RuntimeError(f"{stem}: no recent month found near {datetime.date.today()}")
    months = []
    cy, cm = floor
    while (cy, cm) <= latest:
        months.append(f"{cy:04d}-{cm:02d}")
        cy, cm = _add_month(cy, cm, 1)
    return months


# --- normalization ----------------------------------------------------------
@_fetch_retry
def _fetch_to_temp(url: str) -> str:
    """Download a parquet month to a temp file (full buffer, then to disk)."""
    r = get(url, timeout=(10, 300))
    r.raise_for_status()
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
    try:
        tf.write(r.content)
    finally:
        tf.close()
    return tf.name


def _projection_sql(con: duckdb.DuckDBPyConnection, path: str, colspecs) -> str:
    """Build a canonical SELECT over `path` from the file's actual columns."""
    desc = con.execute(
        "DESCRIBE SELECT * FROM read_parquet(?)", [path]
    ).fetchall()
    present = {row[0].lower(): row[0] for row in desc}
    parts = []
    for out_name, sql_type, candidates in colspecs:
        src = next((present[c.lower()] for c in candidates if c.lower() in present), None)
        if src is not None:
            parts.append(f'TRY_CAST("{src}" AS {sql_type}) AS "{out_name}"')
        else:
            parts.append(f'CAST(NULL AS {sql_type}) AS "{out_name}"')
    return f"SELECT {', '.join(parts)} FROM read_parquet('{path}')"


def _normalize_month(url: str, batch_asset: str, colspecs) -> None:
    """Fetch one month, project to the canonical schema, stream to a batch parquet."""
    import os

    path = _fetch_to_temp(url)
    con = duckdb.connect()
    try:
        reader = con.sql(_projection_sql(con, path, colspecs)).fetch_record_batch(BATCH_ROWS)
        schema = reader.schema
        with raw_parquet_writer(batch_asset, schema) as writer:
            for batch in reader:
                writer.write_batch(batch)
    finally:
        con.close()
        try:
            os.unlink(path)
        except OSError:
            pass


def _fetch_series(node_id: str) -> None:
    stem = node_id[len("nyc-tlc-"):].replace("-", "_")
    cfg = SERIES[stem]
    colspecs = COLSPECS[stem]

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "completed": []}
    completed = set(state.get("completed", []))

    months = _discover_months(stem, cfg["floor"])
    if len(months) < cfg["min_months"]:
        raise RuntimeError(
            f"{stem}: discovered {len(months)} months (< {cfg['min_months']}); "
            "month discovery likely degraded"
        )

    overlap = set(months[-OVERLAP_MONTHS:])  # always re-fetch latest for revisions
    todo = [m for m in months if m not in completed or m in overlap]
    print(f"[{node_id}] {len(months)} months {months[0]}..{months[-1]}; "
          f"{len(todo)} to fetch ({len(completed)} already done)")

    for i, month in enumerate(todo):
        if i:
            time.sleep(FETCH_PACING_S + random.uniform(0, FETCH_PACING_JITTER_S))
        url = f"{BASE}/{stem}_{month}.parquet"
        _normalize_month(url, f"{node_id}-{month}", colspecs)
        completed.add(month)
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "completed": sorted(completed),
        })


@_fetch_retry
def _fetch_zone_lookup(node_id: str) -> None:
    """Small CSV reference table (one row per taxi zone). Full re-pull each run."""
    r = get(f"{MISC}/taxi_zone_lookup.csv", timeout=(10, 120))
    r.raise_for_status()
    save_raw_file(r.text, node_id, "csv")


DOWNLOAD_SPECS = [
    NodeSpec(id="nyc-tlc-yellow-tripdata", fn=_fetch_series, kind="download"),
    NodeSpec(id="nyc-tlc-green-tripdata", fn=_fetch_series, kind="download"),
    NodeSpec(id="nyc-tlc-fhv-tripdata", fn=_fetch_series, kind="download"),
    NodeSpec(id="nyc-tlc-fhvhv-tripdata", fn=_fetch_series, kind="download"),
    NodeSpec(id="nyc-tlc-taxi-zone-lookup", fn=_fetch_zone_lookup, kind="download"),
]


def _series_transform_sql(download_id: str, stem: str) -> str:
    cols = ", ".join(f'"{c[0]}"' for c in COLSPECS[stem])
    return f'SELECT {cols} FROM "{download_id}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nyc-tlc-yellow-tripdata-transform",
        deps=["nyc-tlc-yellow-tripdata"],
        sql=_series_transform_sql("nyc-tlc-yellow-tripdata", "yellow_tripdata"),
    ),
    SqlNodeSpec(
        id="nyc-tlc-green-tripdata-transform",
        deps=["nyc-tlc-green-tripdata"],
        sql=_series_transform_sql("nyc-tlc-green-tripdata", "green_tripdata"),
    ),
    SqlNodeSpec(
        id="nyc-tlc-fhv-tripdata-transform",
        deps=["nyc-tlc-fhv-tripdata"],
        sql=_series_transform_sql("nyc-tlc-fhv-tripdata", "fhv_tripdata"),
    ),
    SqlNodeSpec(
        id="nyc-tlc-fhvhv-tripdata-transform",
        deps=["nyc-tlc-fhvhv-tripdata"],
        sql=_series_transform_sql("nyc-tlc-fhvhv-tripdata", "fhvhv_tripdata"),
    ),
    SqlNodeSpec(
        id="nyc-tlc-taxi-zone-lookup-transform",
        deps=["nyc-tlc-taxi-zone-lookup"],
        sql='''
            SELECT
                TRY_CAST("LocationID" AS BIGINT) AS location_id,
                "Borough"      AS borough,
                "Zone"         AS zone,
                "service_zone" AS service_zone
            FROM "nyc-tlc-taxi-zone-lookup"
            WHERE "LocationID" IS NOT NULL
        ''',
    ),
]
