"""global — single-row global crypto market aggregate."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get_json

GLOBAL_SCHEMA = pa.schema([
    ("active_cryptocurrencies", pa.int64()),
    ("upcoming_icos", pa.int64()),
    ("ongoing_icos", pa.int64()),
    ("ended_icos", pa.int64()),
    ("markets", pa.int64()),
    ("total_market_cap_usd", pa.float64()),
    ("total_volume_usd", pa.float64()),
    ("market_cap_percentage_btc", pa.float64()),
    ("market_cap_percentage_eth", pa.float64()),
    ("market_cap_change_percentage_24h_usd", pa.float64()),
    ("updated_at", pa.int64()),
])


def fetch_global(node_id: str) -> None:
    data = _get_json("/global").get("data", {})
    pct = data.get("market_cap_percentage") or {}
    row = {
        "active_cryptocurrencies": data.get("active_cryptocurrencies"),
        "upcoming_icos": data.get("upcoming_icos"),
        "ongoing_icos": data.get("ongoing_icos"),
        "ended_icos": data.get("ended_icos"),
        "markets": data.get("markets"),
        "total_market_cap_usd": (data.get("total_market_cap") or {}).get("usd"),
        "total_volume_usd": (data.get("total_volume") or {}).get("usd"),
        "market_cap_percentage_btc": pct.get("btc"),
        "market_cap_percentage_eth": pct.get("eth"),
        "market_cap_change_percentage_24h_usd": data.get("market_cap_change_percentage_24h_usd"),
        "updated_at": data.get("updated_at"),
    }
    table = pa.Table.from_pylist([row], schema=GLOBAL_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-global", fn=fetch_global, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-global-transform",
        deps=["coingecko-global"],
        sql='''
            SELECT
                active_cryptocurrencies,
                upcoming_icos,
                ongoing_icos,
                ended_icos,
                markets,
                total_market_cap_usd,
                total_volume_usd,
                market_cap_percentage_btc,
                market_cap_percentage_eth,
                market_cap_change_percentage_24h_usd,
                CAST(to_timestamp(updated_at) AS TIMESTAMP) AS updated_at
            FROM "coingecko-global"
        ''',
    ),
]
