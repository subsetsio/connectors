"""NFIB headline Small Business Optimism Index, monthly, via the getIndicators2
proc (indicator=OPT_INDEX).
"""

import datetime as _dt

import pyarrow as pa

from subsets_utils import save_raw_parquet, NodeSpec, SqlNodeSpec
from utils import _proc, _MIN_YEAR, _MAX_YEAR


def _parse_ymd(s):
    """getIndicators2 monthyear is 'YYYY/M/D' (e.g. '1986/1/1')."""
    return _dt.datetime.strptime(s, "%Y/%m/%d").date()


_OPT_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("optimism_index", pa.float64()),
])


def fetch_optimism_index(asset_id: str) -> None:
    rows = _proc("getIndicators2", [
        ("minYear", _MIN_YEAR), ("minMonth", 1),
        ("maxYear", _MAX_YEAR), ("maxMonth", 12),
        ("indicator", "OPT_INDEX"),
    ])
    out = {"date": [], "optimism_index": []}
    for rec in rows:
        val = rec.get("OPT_INDEX")
        if val is None:
            continue
        out["date"].append(_parse_ymd(rec["monthyear"]))
        out["optimism_index"].append(float(val))
    table = pa.table(out, schema=_OPT_SCHEMA)
    save_raw_parquet(table, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nfib-optimism-index", fn=fetch_optimism_index),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nfib-optimism-index-transform",
        deps=("nfib-optimism-index",),
        sql='''
            SELECT
                date,
                optimism_index
            FROM "nfib-optimism-index"
            WHERE optimism_index IS NOT NULL
            ORDER BY date
        ''',
    ),
]
