"""categories — coin categories with aggregate market data."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get_json

CATEGORIES_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("market_cap", pa.float64()),
    ("market_cap_change_24h", pa.float64()),
    ("volume_24h", pa.float64()),
    ("top_3_coins", pa.string()),
    ("content", pa.string()),
    ("updated_at", pa.string()),
])


def fetch_categories(node_id: str) -> None:
    raw = _get_json("/coins/categories")
    rows = [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "market_cap": c.get("market_cap"),
            "market_cap_change_24h": c.get("market_cap_change_24h"),
            "volume_24h": c.get("volume_24h"),
            "top_3_coins": ",".join(c.get("top_3_coins_id") or []),
            "content": c.get("content"),
            "updated_at": c.get("updated_at"),
        }
        for c in raw
    ]
    table = pa.Table.from_pylist(rows, schema=CATEGORIES_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-categories", fn=fetch_categories, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-categories-transform",
        deps=["coingecko-categories"],
        sql='''
            SELECT
                id AS category_id,
                name,
                market_cap,
                market_cap_change_24h,
                volume_24h,
                top_3_coins,
                content,
                CAST(updated_at AS TIMESTAMP) AS updated_at
            FROM "coingecko-categories"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY updated_at DESC) = 1
        ''',
    ),
]
