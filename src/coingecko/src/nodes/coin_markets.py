"""coin_markets — cross-sectional market snapshot, one row per coin (full paginate)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _num, _paginate

MARKETS_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("symbol", pa.string()),
    ("name", pa.string()),
    ("current_price", pa.float64()),
    ("market_cap", pa.float64()),
    ("market_cap_rank", pa.float64()),
    ("fully_diluted_valuation", pa.float64()),
    ("total_volume", pa.float64()),
    ("high_24h", pa.float64()),
    ("low_24h", pa.float64()),
    ("price_change_24h", pa.float64()),
    ("price_change_percentage_24h", pa.float64()),
    ("market_cap_change_24h", pa.float64()),
    ("market_cap_change_percentage_24h", pa.float64()),
    ("circulating_supply", pa.float64()),
    ("total_supply", pa.float64()),
    ("max_supply", pa.float64()),
    ("ath", pa.float64()),
    ("ath_change_percentage", pa.float64()),
    ("ath_date", pa.string()),
    ("atl", pa.float64()),
    ("atl_change_percentage", pa.float64()),
    ("atl_date", pa.string()),
    ("last_updated", pa.string()),
])


_MARKETS_NUMERIC = {
    "current_price", "market_cap", "market_cap_rank", "fully_diluted_valuation",
    "total_volume", "high_24h", "low_24h", "price_change_24h",
    "price_change_percentage_24h", "market_cap_change_24h",
    "market_cap_change_percentage_24h", "circulating_supply", "total_supply",
    "max_supply", "ath", "ath_change_percentage", "atl", "atl_change_percentage",
}


def fetch_coin_markets(node_id: str) -> None:
    raw = _paginate("/coins/markets", {"vs_currency": "usd", "order": "market_cap_desc"})
    rows = [
        {name: (_num(r.get(name)) if name in _MARKETS_NUMERIC else r.get(name))
         for name in MARKETS_SCHEMA.names}
        for r in raw
    ]
    table = pa.Table.from_pylist(rows, schema=MARKETS_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-coin-markets", fn=fetch_coin_markets, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-coin-markets-transform",
        deps=["coingecko-coin-markets"],
        sql='''
            SELECT
                id AS coin_id,
                symbol,
                name,
                current_price,
                market_cap,
                CAST(market_cap_rank AS BIGINT) AS market_cap_rank,
                fully_diluted_valuation,
                total_volume,
                high_24h,
                low_24h,
                price_change_24h,
                price_change_percentage_24h,
                market_cap_change_24h,
                market_cap_change_percentage_24h,
                circulating_supply,
                total_supply,
                max_supply,
                ath,
                ath_change_percentage,
                CAST(ath_date AS TIMESTAMP) AS ath_date,
                atl,
                atl_change_percentage,
                CAST(atl_date AS TIMESTAMP) AS atl_date,
                CAST(last_updated AS TIMESTAMP) AS last_updated
            FROM "coingecko-coin-markets"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY last_updated DESC) = 1
        ''',
    ),
]
