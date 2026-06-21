"""coins — reference catalog of every tracked coin (id/symbol/name)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get_json

COINS_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("symbol", pa.string()),
    ("name", pa.string()),
])


def fetch_coins(node_id: str) -> None:
    rows = _get_json("/coins/list", {"include_platform": "false"})
    table = pa.Table.from_pylist(rows, schema=COINS_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-coins", fn=fetch_coins, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-coins-transform",
        deps=["coingecko-coins"],
        sql='''
            SELECT id AS coin_id, symbol, name
            FROM "coingecko-coins"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY name) = 1
        ''',
    ),
]
