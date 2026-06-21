"""PIOMAS daily mean Arctic sea-ice THICKNESS (m, cells >0.15m).

The daily filename embeds the data's end year (e.g. "1979.2026"), which rolls
forward annually, so the URL is discovered from the project data page. Gzipped
.dat, full 1979-present corpus per request.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import discover_daily_url, fetch, gunzip, parse_daily

DAILY_THICK_SCHEMA = pa.schema(
    [("date", pa.date32()), ("thickness_m", pa.float64())]
)


def fetch_thickness_daily(node_id: str) -> None:
    asset = node_id
    text = gunzip(fetch(discover_daily_url("thick")).content)
    rows = parse_daily(text, "thickness_m")
    if not rows:
        raise RuntimeError(
            "PIOMAS daily thickness parser produced no rows — format changed"
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=DAILY_THICK_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="psc-piomas-sea-ice-thickness-daily",
        fn=fetch_thickness_daily,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psc-piomas-sea-ice-thickness-daily-transform",
        deps=["psc-piomas-sea-ice-thickness-daily"],
        sql='''
            SELECT
                CAST(date AS DATE)       AS date,
                CAST(thickness_m AS DOUBLE) AS thickness_m
            FROM "psc-piomas-sea-ice-thickness-daily"
            WHERE thickness_m IS NOT NULL
            ORDER BY date
        ''',
    ),
]
