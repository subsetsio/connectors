"""Panama Canal Authority (ACP) — AQUARIUS WebPortal hydromet time-series.

Two published subsets, the canonical time-series shape:

  * `series`  — reference catalog of every observed monitoring series
  * `values`  — long-format daily observations across all series

Both are full re-pulls every run (stateless): the portal exposes no incremental
filter, and the daily roll-up keeps the corpus small enough to refetch cheaply.
Forecast/simulation series (the `SIMULACIONES` station, `Tst*` rigs, and
forecast-labelled outputs) are excluded in `utils` so only gauge readings ship.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet, raw_parquet_writer

from utils import export_daily, fetch_series

# ---- series catalog ------------------------------------------------------

SERIES_SCHEMA = pa.schema(
    [
        ("series_id", pa.string()),
        ("parameter", pa.string()),
        ("label", pa.string()),
        ("location_identifier", pa.string()),
        ("location_name", pa.string()),
        ("location_type", pa.string()),
        ("watershed", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("start_time", pa.string()),
        ("end_time", pa.string()),
        ("timezone", pa.float64()),
    ]
)


def fetch_series_catalog(node_id: str) -> None:
    asset = node_id
    series = fetch_series()
    cols = {name: [] for name in SERIES_SCHEMA.names}
    for s in series:
        for name in SERIES_SCHEMA.names:
            cols[name].append(s.get(name))
    table = pa.table(cols, schema=SERIES_SCHEMA)
    save_raw_parquet(table, asset)


# ---- daily observations --------------------------------------------------

VALUES_SCHEMA = pa.schema(
    [
        ("series_id", pa.string()),
        ("parameter", pa.string()),
        ("label", pa.string()),
        ("location_identifier", pa.string()),
        ("watershed", pa.string()),
        ("unit", pa.string()),
        ("date", pa.string()),
        ("value_mean", pa.float64()),
        ("value_min", pa.float64()),
        ("value_max", pa.float64()),
        ("value_sum", pa.float64()),
        ("n_obs", pa.int32()),
    ]
)


def _export_one(s: dict):
    """Fetch + daily-aggregate one series. Permanent 4xx -> skip (None)."""
    try:
        unit, rows = export_daily(s["series_id"])
    except httpx.HTTPStatusError as e:
        if e.response is not None and 400 <= e.response.status_code < 500 and e.response.status_code != 429:
            print(f"  skip {s['series_id']}: HTTP {e.response.status_code}")
            return None
        raise
    if not rows:
        return None
    n = len(rows)

    def col(i):
        return [r[i] for r in rows]

    batch = pa.table(
        {
            "series_id": [s["series_id"]] * n,
            "parameter": [s["parameter"]] * n,
            "label": [s["label"]] * n,
            "location_identifier": [s["location_identifier"]] * n,
            "watershed": [s["watershed"]] * n,
            "unit": [unit] * n,
            "date": pa.array(col(0), pa.date32()),
            "value_mean": col(1),
            "value_min": col(2),
            "value_max": col(3),
            "value_sum": col(4),
            "n_obs": pa.array(col(5), pa.int32()),
        },
        schema=VALUES_SCHEMA,
    )
    return batch


def fetch_values(node_id: str) -> None:
    asset = node_id
    series = fetch_series()
    written = 0
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        with ThreadPoolExecutor(max_workers=6) as ex:
            futures = {ex.submit(_export_one, s): s for s in series}
            for fut in as_completed(futures):
                batch = fut.result()
                if batch is not None and batch.num_rows:
                    writer.write_table(batch)
                    written += 1
    print(f"  wrote daily observations for {written}/{len(series)} series")


DOWNLOAD_SPECS = [
    NodeSpec(id="panama-canal-authority-series", fn=fetch_series_catalog, kind="download"),
    NodeSpec(id="panama-canal-authority-values", fn=fetch_values, kind="download"),
]

# ---- transforms: thin parse-and-type leaf nodes --------------------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="panama-canal-authority-series-transform",
        deps=["panama-canal-authority-series"],
        sql='''
            SELECT
                series_id,
                parameter,
                label,
                location_identifier,
                location_name,
                location_type,
                watershed,
                CAST(latitude  AS DOUBLE) AS latitude,
                CAST(longitude AS DOUBLE) AS longitude,
                TRY_CAST(start_time AS TIMESTAMP) AS start_time,
                TRY_CAST(end_time   AS TIMESTAMP) AS end_time,
                CAST(timezone AS DOUBLE) AS utc_offset_hours
            FROM "panama-canal-authority-series"
            WHERE series_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="panama-canal-authority-values-transform",
        deps=["panama-canal-authority-values"],
        sql='''
            SELECT
                series_id,
                parameter,
                label,
                location_identifier,
                watershed,
                unit,
                CAST(date AS DATE) AS date,
                CAST(value_mean AS DOUBLE) AS value_mean,
                CAST(value_min  AS DOUBLE) AS value_min,
                CAST(value_max  AS DOUBLE) AS value_max,
                CAST(value_sum  AS DOUBLE) AS value_sum,
                CAST(n_obs AS INTEGER) AS n_obs
            FROM "panama-canal-authority-values"
            WHERE date IS NOT NULL AND value_mean IS NOT NULL
        ''',
    ),
]
