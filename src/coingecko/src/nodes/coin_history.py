"""coin_history — daily price/market-cap/volume time series for the top-N coins.

A full 17k-coin historical sweep is infeasible under the free rate limit
(30 calls/min, 10k/month with a demo key; harsher keyless), so this is scoped
to COIN_HISTORY_TOP_N coins by market cap.
"""

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get_json, _num

# Scope for the per-coin historical sweep. One call per coin under a tight rate
# limit; keep this modest. The long tail of dust coins has no analytical value.
COIN_HISTORY_TOP_N = 50

HISTORY_SCHEMA = pa.schema([
    ("coin_id", pa.string()),
    ("ts_ms", pa.int64()),
    ("price_usd", pa.float64()),
    ("market_cap_usd", pa.float64()),
    ("total_volume_usd", pa.float64()),
])


def _is_permanent_http(exc: BaseException) -> bool:
    return (
        isinstance(exc, httpx.HTTPStatusError)
        and 400 <= exc.response.status_code < 500
        and exc.response.status_code != 429
    )


def fetch_coin_history(node_id: str) -> None:
    top = _get_json(
        "/coins/markets",
        {"vs_currency": "usd", "order": "market_cap_desc", "per_page": COIN_HISTORY_TOP_N, "page": 1},
    )
    coin_ids = [c["id"] for c in top if c.get("id")]

    rows: list[dict] = []
    for coin_id in coin_ids:
        try:
            # Public/Demo tier caps historical queries at the past 365 days
            # (days=max returns 401/error 10012). 365d yields daily granularity.
            chart = _get_json(f"/coins/{coin_id}/market_chart", {"vs_currency": "usd", "days": "365"})
        except httpx.HTTPStatusError as exc:
            if _is_permanent_http(exc):
                print(f"coin_history: skipping {coin_id} — permanent {exc.response.status_code}")
                continue
            raise
        caps = {int(t): v for t, v in chart.get("market_caps", [])}
        vols = {int(t): v for t, v in chart.get("total_volumes", [])}
        for ts, price in chart.get("prices", []):
            ts = int(ts)
            rows.append({
                "coin_id": coin_id,
                "ts_ms": ts,
                "price_usd": _num(price),
                "market_cap_usd": _num(caps.get(ts)),
                "total_volume_usd": _num(vols.get(ts)),
            })

    table = pa.Table.from_pylist(rows, schema=HISTORY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="coingecko-coin-history", fn=fetch_coin_history, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coingecko-coin-history-transform",
        deps=["coingecko-coin-history"],
        sql='''
            SELECT coin_id, date, price_usd, market_cap_usd, total_volume_usd
            FROM (
                SELECT
                    coin_id,
                    CAST(to_timestamp(ts_ms / 1000.0) AS DATE) AS date,
                    price_usd,
                    market_cap_usd,
                    total_volume_usd,
                    row_number() OVER (
                        PARTITION BY coin_id, CAST(to_timestamp(ts_ms / 1000.0) AS DATE)
                        ORDER BY ts_ms DESC
                    ) AS rn
                FROM "coingecko-coin-history"
                WHERE price_usd IS NOT NULL
            )
            WHERE rn = 1
        ''',
    ),
]
