"""who-indicators — the WHO GHO indicator catalog.

Subset: who-indicators — the indicator catalog (IndicatorCode, IndicatorName,
Language). Stateless full re-pull from the GHO OData /Indicator collection.
"""

import logging

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, fetch_odata

log = logging.getLogger("who")


_INDICATOR_SCHEMA = pa.schema(
    [
        ("IndicatorCode", pa.string()),
        ("IndicatorName", pa.string()),
        ("Language", pa.string()),
    ]
)


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    rows = fetch_odata(f"{BASE}/Indicator")
    if not rows:
        raise RuntimeError("WHO /Indicator returned no rows")
    norm = [
        {
            "IndicatorCode": r.get("IndicatorCode"),
            "IndicatorName": r.get("IndicatorName"),
            "Language": r.get("Language"),
        }
        for r in rows
    ]
    table = pa.Table.from_pylist(norm, schema=_INDICATOR_SCHEMA)
    save_raw_parquet(table, asset)
    log.info("who-indicators: wrote %d indicators", table.num_rows)


DOWNLOAD_SPECS = [
    NodeSpec(id="who-indicators", fn=fetch_indicators, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="who-indicators-transform",
        deps=["who-indicators"],
        sql='''
            SELECT
                IndicatorCode AS indicator_code,
                IndicatorName AS indicator_name,
                Language      AS language
            FROM "who-indicators"
            WHERE IndicatorCode IS NOT NULL
        ''',
    ),
]
