"""Polymarket markets — Gamma /markets/keyset, one row per market."""
import json

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer

from utils import _date, _f, _keyset_pages


def _yes_no_prices(outcomes_str, prices_str):
    """Parse Gamma's JSON-encoded outcomes/outcomePrices strings to (yes, no)."""
    if not outcomes_str or not prices_str:
        return None, None
    try:
        outcomes = json.loads(outcomes_str)
        prices = json.loads(prices_str)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, None
    yes_price = no_price = None
    for outcome, price in zip(outcomes, prices):
        value = _f(price)
        label = (outcome or "").strip().lower()
        if label == "yes":
            yes_price = value
        elif label == "no":
            no_price = value
    return yes_price, no_price


def _market_row(m: dict) -> dict:
    yes_price, no_price = _yes_no_prices(m.get("outcomes"), m.get("outcomePrices"))
    events = m.get("events") or []
    event = events[0] if events else {}
    return {
        "market_id": m.get("id"),
        "event_id": event.get("id"),
        "event_slug": event.get("slug"),
        "event_title": event.get("title"),
        "neg_risk": bool(event.get("negRisk") or event.get("negRiskAugmented") or m.get("negRisk")),
        "question": m.get("question"),
        "slug": m.get("slug"),
        "condition_id": m.get("conditionId"),
        "outcome_yes_price": yes_price,
        "outcome_no_price": no_price,
        "volume_usd": _f(m.get("volumeNum") if m.get("volumeNum") is not None else m.get("volume")),
        "volume_24h_usd": _f(m.get("volume24hr")),
        "volume_1wk_usd": _f(m.get("volume1wk")),
        "volume_1mo_usd": _f(m.get("volume1mo")),
        "volume_1yr_usd": _f(m.get("volume1yr")),
        "liquidity_usd": _f(m.get("liquidityNum") if m.get("liquidityNum") is not None else m.get("liquidity")),
        "last_trade_price": _f(m.get("lastTradePrice")),
        "best_bid": _f(m.get("bestBid")),
        "best_ask": _f(m.get("bestAsk")),
        "spread": _f(m.get("spread")),
        "competitive": _f(m.get("competitive")),
        "is_active": bool(m.get("active")),
        "is_closed": bool(m.get("closed")),
        "start_date": _date(m.get("startDateIso") or m.get("startDate")),
        "end_date": _date(m.get("endDateIso") or m.get("endDate")),
        "created_at": m.get("createdAt"),
        "updated_at": m.get("updatedAt"),
    }


def fetch_markets(node_id: str) -> None:
    asset = node_id  # "polymarket-markets"
    # The keyset endpoint defaults to closed=false (open markets only); the
    # closed corpus is the bulk of Polymarket. Walk both states for full coverage.
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for closed in ("false", "true"):
            for rows in _keyset_pages("markets", {"closed": closed}):
                for m in rows:
                    if not m.get("id"):
                        continue
                    f.write(json.dumps(_market_row(m)) + "\n")
                    total += 1
                print(f"    markets (closed={closed}): {total:,} written")
    print(f"  markets: wrote {total:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="polymarket-markets", fn=fetch_markets, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="polymarket-markets-transform",
        deps=["polymarket-markets"],
        sql='''
            SELECT * EXCLUDE (_rn) FROM (
                SELECT
                    CAST(market_id AS VARCHAR)        AS market_id,
                    CAST(event_id AS VARCHAR)         AS event_id,
                    CAST(event_slug AS VARCHAR)       AS event_slug,
                    CAST(event_title AS VARCHAR)      AS event_title,
                    CAST(neg_risk AS BOOLEAN)         AS neg_risk,
                    CAST(question AS VARCHAR)         AS question,
                    CAST(slug AS VARCHAR)             AS slug,
                    CAST(condition_id AS VARCHAR)     AS condition_id,
                    CAST(outcome_yes_price AS DOUBLE) AS outcome_yes_price,
                    CAST(outcome_no_price AS DOUBLE)  AS outcome_no_price,
                    CAST(volume_usd AS DOUBLE)        AS volume_usd,
                    CAST(volume_24h_usd AS DOUBLE)    AS volume_24h_usd,
                    CAST(volume_1wk_usd AS DOUBLE)    AS volume_1wk_usd,
                    CAST(volume_1mo_usd AS DOUBLE)    AS volume_1mo_usd,
                    CAST(volume_1yr_usd AS DOUBLE)    AS volume_1yr_usd,
                    CAST(liquidity_usd AS DOUBLE)     AS liquidity_usd,
                    CAST(last_trade_price AS DOUBLE)  AS last_trade_price,
                    CAST(best_bid AS DOUBLE)          AS best_bid,
                    CAST(best_ask AS DOUBLE)          AS best_ask,
                    CAST(spread AS DOUBLE)            AS spread,
                    CAST(competitive AS DOUBLE)       AS competitive,
                    CAST(is_active AS BOOLEAN)        AS is_active,
                    CAST(is_closed AS BOOLEAN)        AS is_closed,
                    TRY_CAST(start_date AS DATE)      AS start_date,
                    TRY_CAST(end_date AS DATE)        AS end_date,
                    TRY_CAST(created_at AS TIMESTAMP) AS created_at,
                    TRY_CAST(updated_at AS TIMESTAMP) AS updated_at,
                    row_number() OVER (
                        PARTITION BY market_id ORDER BY updated_at DESC NULLS LAST
                    ) AS _rn
                FROM "polymarket-markets"
                WHERE market_id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
