"""ISC-GEM Global Instrumental Earthquake Catalogue.

Single homogeneous corpus: one row per large instrumentally-recorded earthquake
(1904-present). Sourced from the USGS ComCat FDSN event web service, which mirrors
the curated ISC-GEM catalogue verbatim as ``catalog=iscgem`` (the official ISC
distribution is gated behind a CAPTCHA form and is not machine-fetchable).

Strategy: stateless full re-pull. The whole catalogue (~74k events, a few MB) fits
comfortably in RAM, so every run re-fetches the entire corpus and overwrites — late
corrections and version bumps in the mirror are picked up for free. The FDSN /query
endpoint requires explicit starttime/endtime bounds (an unbounded query returns
nothing) and caps a single response at 20000 events, so we page by offset under a
frozen time window ordered by time-asc.
"""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"
CATALOG = "iscgem"
# The catalogue begins in 1904; 1900 is a safe lower floor for the time window.
START_FLOOR = "1900-01-01T00:00:00"
PAGE_SIZE = 20000          # FDSN hard cap on a single response
MAX_PAGES = 50             # safety ceiling: ~74k/20k = 4 pages today; raise if blown past

# Raw schema (CSV column set is stable across the FDSN mirror). Numeric fields are
# frequently empty -> nullable; timestamps stay as ISO strings and are cast in the
# transform (the correctness gate). Column names mirror the source verbatim.
SCHEMA = pa.schema([
    ("time", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("depth", pa.float64()),
    ("mag", pa.float64()),
    ("magType", pa.string()),
    ("nst", pa.int64()),
    ("gap", pa.float64()),
    ("dmin", pa.float64()),
    ("rms", pa.float64()),
    ("net", pa.string()),
    ("id", pa.string()),
    ("updated", pa.string()),
    ("place", pa.string()),
    ("type", pa.string()),
    ("horizontalError", pa.float64()),
    ("depthError", pa.float64()),
    ("magError", pa.float64()),
    ("magNst", pa.int64()),
    ("status", pa.string()),
    ("locationSource", pa.string()),
    ("magSource", pa.string()),
])

_FLOAT_COLS = ("latitude", "longitude", "depth", "mag", "gap", "dmin", "rms",
               "horizontalError", "depthError", "magError")
_INT_COLS = ("nst", "magNst")
_STR_COLS = ("time", "magType", "net", "id", "updated", "place", "type",
             "status", "locationSource", "magSource")


def _f(v):
    v = (v or "").strip()
    return float(v) if v else None


def _i(v):
    v = (v or "").strip()
    return int(float(v)) if v else None


def _s(v):
    v = (v or "").strip()
    return v or None


@transient_retry()
def _fetch_page(params):
    resp = get(BASE, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def _parse_csv(text):
    import csv
    import io
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        rows.append({
            **{c: _f(r.get(c)) for c in _FLOAT_COLS},
            **{c: _i(r.get(c)) for c in _INT_COLS},
            **{c: _s(r.get(c)) for c in _STR_COLS},
        })
    return rows


def fetch_earthquakes(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    end_freeze = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    base_params = {
        "catalog": CATALOG,
        "format": "csv",
        "orderby": "time-asc",
        "starttime": START_FLOOR,
        "endtime": end_freeze,
        "limit": PAGE_SIZE,
    }

    all_rows = []
    offset = 1  # FDSN offset is 1-based
    for page in range(MAX_PAGES):
        text = _fetch_page({**base_params, "offset": offset})
        rows = _parse_csv(text)
        all_rows.extend(rows)
        if len(rows) < PAGE_SIZE:
            break
        offset += len(rows)
    else:
        raise RuntimeError(
            f"{asset}: hit MAX_PAGES={MAX_PAGES} (>{MAX_PAGES * PAGE_SIZE} events) "
            "without draining — catalogue grew unexpectedly; raise the ceiling."
        )

    if not all_rows:
        raise RuntimeError(f"{asset}: fetched 0 events — upstream catalog={CATALOG} empty?")

    table = pa.Table.from_pylist(all_rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="isc-gem-earthquakes", fn=fetch_earthquakes, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="isc-gem-earthquakes-transform",
        deps=["isc-gem-earthquakes"],
        sql='''
            SELECT
                id                                  AS event_id,
                CAST(time AS TIMESTAMP)             AS time,
                CAST(latitude AS DOUBLE)            AS latitude,
                CAST(longitude AS DOUBLE)           AS longitude,
                CAST(depth AS DOUBLE)               AS depth_km,
                CAST(mag AS DOUBLE)                 AS magnitude,
                magType                             AS magnitude_type,
                place,
                type                                AS event_type,
                status,
                locationSource                      AS location_source,
                magSource                           AS magnitude_source,
                CAST(horizontalError AS DOUBLE)     AS horizontal_error_km,
                CAST(depthError AS DOUBLE)          AS depth_error_km,
                CAST(magError AS DOUBLE)            AS magnitude_error,
                CAST(nst AS BIGINT)                 AS num_stations,
                CAST(gap AS DOUBLE)                 AS azimuthal_gap_deg,
                CAST(dmin AS DOUBLE)                AS min_distance_deg,
                CAST(rms AS DOUBLE)                 AS rms,
                CAST(updated AS TIMESTAMP)          AS updated
            FROM "isc-gem-earthquakes"
            WHERE id IS NOT NULL
              AND time IS NOT NULL
              AND latitude IS NOT NULL
              AND longitude IS NOT NULL
              AND mag IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY updated DESC) = 1
        ''',
    ),
]
