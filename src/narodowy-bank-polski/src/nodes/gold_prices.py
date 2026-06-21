"""NBP accounting price of gold (single daily series).
-> (date, price_pln_per_g). History since 2013-01-02.
"""

from datetime import date

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _fetch_windows

_GOLD_START = date(2013, 1, 2)

_GOLD_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("price_pln_per_g", pa.float64()),
])


def fetch_gold(node_id: str) -> None:
    """NBP accounting price of gold (single daily series)."""
    rows = [
        {"date": d["data"], "price_pln_per_g": d["cena"]}
        for d in _fetch_windows("cenyzlota/{start}/{end}/", _GOLD_START)
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_GOLD_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="narodowy-bank-polski-gold-prices", fn=fetch_gold, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="narodowy-bank-polski-gold-prices-transform",
        deps=["narodowy-bank-polski-gold-prices"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE) AS date,
                CAST(price_pln_per_g AS DOUBLE) AS price_pln_per_g
            FROM "narodowy-bank-polski-gold-prices"
            WHERE price_pln_per_g IS NOT NULL
        ''',
    ),
]
