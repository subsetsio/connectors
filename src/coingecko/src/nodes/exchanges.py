"""exchanges — centralized exchanges with volume/trust metrics."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _paginate

EXCHANGES_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("year_established", pa.int64()),
    ("country", pa.string()),
    ("has_trading_incentive", pa.bool_()),
    ("trust_score", pa.int64()),
    ("trust_score_rank", pa.int64()),
    ("trade_volume_24h_btc", pa.float64()),
])


def fetch_exchanges(node_id: str) -> None:
    rows = _paginate("/exchanges", {})
    table = pa.Table.from_pylist(rows, schema=EXCHANGES_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-exchanges", fn=fetch_exchanges, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-exchanges-transform",
        deps=["coingecko-exchanges"],
        sql='''
            SELECT
                id AS exchange_id,
                name,
                year_established,
                country,
                has_trading_incentive,
                trust_score,
                trust_score_rank,
                trade_volume_24h_btc
            FROM "coingecko-exchanges"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY trust_score_rank) = 1
        ''',
    ),
]
