"""Sveriges Riksbank — SWEA series catalog.

`series` — the catalog of every SWEA time series (one row per series).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_series_catalog

SERIES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("source", pa.string()),
    ("short_description", pa.string()),
    ("mid_description", pa.string()),
    ("long_description", pa.string()),
    ("group_id", pa.int64()),
    ("observation_min_date", pa.string()),
    ("observation_max_date", pa.string()),
    ("series_closed", pa.bool_()),
])


def fetch_series(node_id: str) -> None:
    asset = node_id
    series = fetch_series_catalog()
    rows = [
        {
            "series_id": s.get("seriesId"),
            "source": s.get("source"),
            "short_description": s.get("shortDescription"),
            "mid_description": s.get("midDescription"),
            "long_description": s.get("longDescription"),
            "group_id": s.get("groupId"),
            "observation_min_date": s.get("observationMinDate"),
            "observation_max_date": s.get("observationMaxDate"),
            "series_closed": s.get("seriesClosed"),
        }
        for s in series
    ]
    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sveriges-riksbank-series", fn=fetch_series, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sveriges-riksbank-series-transform",
        deps=["sveriges-riksbank-series"],
        sql='''
            SELECT
                series_id,
                source,
                short_description,
                mid_description,
                long_description,
                group_id,
                CAST(observation_min_date AS DATE) AS observation_min_date,
                CAST(observation_max_date AS DATE) AS observation_max_date,
                series_closed
            FROM "sveriges-riksbank-series"
            WHERE series_id IS NOT NULL
        ''',
    ),
]
