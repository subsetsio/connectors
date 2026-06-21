"""PIOMAS daily pan-Arctic sea-ice VOLUME (10^3 km^3).

The daily filename embeds the data's end year (e.g. "1979.2026"), which rolls
forward annually, so the URL is discovered from the project data page. Gzipped
.dat, full 1979-present corpus per request.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import discover_daily_url, fetch, gunzip, parse_daily

DAILY_VOL_SCHEMA = pa.schema(
    [("date", pa.date32()), ("volume_thousand_km3", pa.float64())]
)


def fetch_volume_daily(node_id: str) -> None:
    asset = node_id
    text = gunzip(fetch(discover_daily_url("vol")).content)
    rows = parse_daily(text, "volume_thousand_km3")
    if not rows:
        raise RuntimeError(
            "PIOMAS daily volume parser produced no rows — format changed"
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=DAILY_VOL_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="psc-piomas-sea-ice-volume-daily",
        fn=fetch_volume_daily,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psc-piomas-sea-ice-volume-daily-transform",
        deps=["psc-piomas-sea-ice-volume-daily"],
        sql='''
            SELECT
                CAST(date AS DATE)                AS date,
                CAST(volume_thousand_km3 AS DOUBLE) AS volume_thousand_km3
            FROM "psc-piomas-sea-ice-volume-daily"
            WHERE volume_thousand_km3 IS NOT NULL
            ORDER BY date
        ''',
    ),
]
