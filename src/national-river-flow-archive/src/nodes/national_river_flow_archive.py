"""National River Flow Archive (UK / CEH) connector.

Mechanism: the NRFA RESTful web service (https://nrfaapps.ceh.ac.uk/nrfa/ws),
no auth. Three endpoints are used:
  - station-ids / station-info: station list and metadata (the `stations` table).
  - time-series: one (station, data-type) series per request, returned as a flat
    [date, value, date, value, ...] `data-stream`.

Shape: stateless full re-pull (option 1). There is no incremental/change feed,
so every refresh re-fetches the whole corpus and overwrites. Each time-series
feed (gdf, cdr, amax-flow, ...) is one download node that walks every station
offering that data type and streams the long-format (station, date, value) rows
into a single parquet asset. The big daily feeds (gdf ~1.5k stations x decades,
cdr similar) are tens of millions of rows, so raw is written with the streaming
parquet writer, one row group per station, to keep memory bounded.

Attribution: "Data from the UK National River Flow Archive".
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

from constants import SLUG, BASE, TIMESERIES_TYPES, FEED_SHAPE

# Long-format time-series raw schema: which station, the raw period token as a
# string (daily "YYYY-MM-DD", monthly "YYYY-MM", or an ISO timestamp for peaks),
# and the measured value. The transform casts the token to the right type.
TS_SCHEMA = pa.schema([
    ("station_id", pa.int64()),
    ("t", pa.string()),
    ("value", pa.float64()),
])

# Curated, flat station-metadata schema for the `stations` reference table.
STATION_FIELDS = (
    "id,name,catchment-area,river,location,grid-reference,lat-long,"
    "station-level,gdf-statistics"
)
STATION_SCHEMA = pa.schema([
    ("station_id", pa.int64()),
    ("name", pa.string()),
    ("river", pa.string()),
    ("location", pa.string()),
    ("catchment_area_km2", pa.float64()),
    ("easting", pa.float64()),
    ("northing", pa.float64()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("station_level_m", pa.float64()),
    ("gdf_start_date", pa.string()),
    ("gdf_end_date", pa.string()),
    ("gdf_mean_flow_m3s", pa.float64()),
])


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _stations_with_type(data_type: str) -> list[int]:
    """Station ids that offer `data_type`, read from the bulk data-summary."""
    rows = _get_json(
        f"{BASE}/station-info",
        station="*", format="json-object", fields="id,data-summary",
    )["data"]
    out = []
    for r in rows:
        types = {dt["data-type"] for dt in r.get("data-summary", {}).get("data-types", [])}
        if data_type in types:
            out.append(int(r["id"]))
    return out


def _fetch_series(station_id: int, data_type: str):
    """Fetch one (station, data-type) series as a list of (token, value)."""
    payload = _get_json(
        f"{BASE}/time-series",
        station=station_id, **{"data-type": data_type},
        format="json-object", dates="true", flags="false",
    )
    stream = payload.get("data-stream", []) or []
    pairs = []
    for i in range(0, len(stream) - 1, 2):
        token = stream[i]
        val = stream[i + 1]
        pairs.append((token, float(val) if val is not None else None))
    return pairs


def fetch_timeseries(node_id: str) -> None:
    """One feed (gdf / cdr / amax-flow / ...) across every station offering it.

    Streams long-format rows to a single parquet asset, one row group per
    station to bound memory for the multi-million-row daily feeds."""
    data_type = node_id[len(SLUG) + 1:]          # strip "national-river-flow-archive-"
    station_ids = _stations_with_type(data_type)
    if not station_ids:
        raise AssertionError(f"{node_id}: no stations report data-type {data_type!r}")

    written = 0
    with raw_parquet_writer(node_id, TS_SCHEMA) as writer:
        for sid in station_ids:
            pairs = _fetch_series(sid, data_type)
            if not pairs:
                continue
            tokens = [p[0] for p in pairs]
            values = [p[1] for p in pairs]
            batch = pa.table(
                {
                    "station_id": pa.array([sid] * len(pairs), pa.int64()),
                    "t": pa.array(tokens, pa.string()),
                    "value": pa.array(values, pa.float64()),
                },
                schema=TS_SCHEMA,
            )
            writer.write_table(batch)
            written += len(pairs)

    if written == 0:
        raise AssertionError(f"{node_id}: every station returned an empty series")


def fetch_stations(node_id: str) -> None:
    """The NRFA gauging-station reference table — one curated flat row per
    station (location, catchment area, GDF summary)."""
    rows = _get_json(
        f"{BASE}/station-info",
        station="*", format="json-object", fields=STATION_FIELDS,
    )["data"]

    def _f(v):
        return float(v) if v is not None else None

    out = []
    for r in rows:
        gr = r.get("grid-reference") or {}
        ll = r.get("lat-long") or {}
        out.append({
            "station_id": int(r["id"]),
            "name": r.get("name"),
            "river": r.get("river"),
            "location": r.get("location"),
            "catchment_area_km2": _f(r.get("catchment-area")),
            "easting": _f(gr.get("easting")),
            "northing": _f(gr.get("northing")),
            "latitude": _f(ll.get("latitude")),
            "longitude": _f(ll.get("longitude")),
            "station_level_m": _f(r.get("station-level")),
            "gdf_start_date": r.get("gdf-start-date"),
            "gdf_end_date": r.get("gdf-end-date"),
            "gdf_mean_flow_m3s": _f(r.get("gdf-mean-flow")),
        })

    table = pa.Table.from_pylist(out, schema=STATION_SCHEMA)
    save_raw_parquet(table, node_id)


# --- Download specs: one per rank-accepted entity --------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{dt}", fn=fetch_timeseries, kind="download")
    for dt in TIMESERIES_TYPES
] + [
    NodeSpec(id=f"{SLUG}-stations", fn=fetch_stations, kind="download"),
]


# --- Transform specs: one published Delta table per subset -----------------

def _ts_transform_sql(download_id: str, shape: str, value_col: str) -> str:
    src = f'"{download_id}"'
    if shape == "daily":
        return (
            f"SELECT station_id, CAST(t AS DATE) AS date, "
            f"value AS {value_col} FROM {src} WHERE value IS NOT NULL"
        )
    if shape == "monthly":
        return (
            f"SELECT station_id, CAST(t || '-01' AS DATE) AS month, "
            f"value AS {value_col} FROM {src} WHERE value IS NOT NULL"
        )
    # event (instantaneous annual maxima / peaks over threshold)
    return (
        f"SELECT station_id, CAST(t AS TIMESTAMP) AS occurred_at, "
        f"value AS {value_col} FROM {src} WHERE value IS NOT NULL"
    )


_TS_TRANSFORMS = [
    SqlNodeSpec(
        id=f"{SLUG}-{dt}-transform",
        deps=[f"{SLUG}-{dt}"],
        sql=_ts_transform_sql(f"{SLUG}-{dt}", *FEED_SHAPE[dt]),
    )
    for dt in TIMESERIES_TYPES
]

_STATIONS_TRANSFORM = SqlNodeSpec(
    id=f"{SLUG}-stations-transform",
    deps=[f"{SLUG}-stations"],
    sql=f'''
        SELECT
            station_id,
            name,
            river,
            location,
            catchment_area_km2,
            easting,
            northing,
            latitude,
            longitude,
            station_level_m,
            CAST(gdf_start_date AS DATE) AS gdf_start_date,
            CAST(gdf_end_date   AS DATE) AS gdf_end_date,
            gdf_mean_flow_m3s
        FROM "{SLUG}-stations"
        WHERE station_id IS NOT NULL
    ''',
)

TRANSFORM_SPECS = _TS_TRANSFORMS + [_STATIONS_TRANSFORM]
