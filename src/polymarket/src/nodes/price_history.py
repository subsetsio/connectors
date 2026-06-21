"""Polymarket price history — CLOB /prices-history, daily YES-probability series.

CLOB /prices-history caps an explicit startTs/endTs window at ~15 days of
wall-clock regardless of fidelity, so windowed chunking costs one request per
fortnight. The `interval=max` preset bypasses that and returns the full lifetime
in a single request; at `fidelity=1440` (daily buckets) that is the whole daily
price history of a market in one call.

Price history is deliberately scoped to *binary* markets whose all-time volume
is at least PRICE_HISTORY_MIN_VOLUME_USD — the markets where a price series is
meaningful — keeping the CLOB crawl to a few thousand requests. Widen the
threshold to deepen coverage.
"""
import json

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer

from utils import _f, _get_json, _i, _keyset_pages

CLOB_PRICES_URL = "https://clob.polymarket.com/prices-history"

PRICE_HISTORY_MIN_VOLUME_USD = 100_000
PRICE_FIDELITY_MINUTES = 1440  # daily buckets


def _scoped_binary_markets():
    """Walk the markets catalog (both open and closed) and yield
    (market_id, yes_token_id) for binary Yes/No markets above the volume
    threshold. Closed markets — resolved elections, decided events — are the
    most valuable price histories, so both states must be walked."""
    for closed in ("false", "true"):
        for rows in _keyset_pages("markets", {"closed": closed}):
            for m in rows:
                mid = m.get("id")
                if not mid:
                    continue
                if (_f(m.get("volumeNum")) or 0) < PRICE_HISTORY_MIN_VOLUME_USD:
                    continue
                try:
                    outcomes = [str(o).strip().lower() for o in json.loads(m.get("outcomes") or "[]")]
                    tokens = json.loads(m.get("clobTokenIds") or "[]")
                except (TypeError, ValueError, json.JSONDecodeError):
                    continue
                if outcomes != ["yes", "no"] or len(tokens) < 1:
                    continue
                yield mid, tokens[0]


def fetch_price_history(node_id: str) -> None:
    asset = node_id  # "polymarket-price-history"
    scoped = list(_scoped_binary_markets())
    print(f"  price-history: {len(scoped):,} binary markets over "
          f"${PRICE_HISTORY_MIN_VOLUME_USD:,} volume")

    total_points = 0
    done = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for mid, token in scoped:
            payload = _get_json(
                CLOB_PRICES_URL,
                {"market": token, "interval": "max", "fidelity": PRICE_FIDELITY_MINUTES},
            )
            for pt in payload.get("history", []):
                ts = _i(pt.get("t"))
                price = _f(pt.get("p"))
                if ts is None or price is None:
                    continue
                f.write(json.dumps({"market_id": mid, "timestamp": ts, "price": price}) + "\n")
                total_points += 1
            done += 1
            if done % 200 == 0:
                print(f"    price-history: {done:,}/{len(scoped):,} markets, "
                      f"{total_points:,} points")
    print(f"  price-history: wrote {total_points:,} points across {done:,} markets")


DOWNLOAD_SPECS = [
    NodeSpec(id="polymarket-price-history", fn=fetch_price_history, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="polymarket-price-history-transform",
        deps=["polymarket-price-history"],
        sql='''
            SELECT
                CAST(market_id AS VARCHAR)                        AS market_id,
                CAST(timestamp AS BIGINT)                         AS timestamp,
                CAST(to_timestamp(timestamp) AS TIMESTAMP)       AS datetime,
                CAST(price AS DOUBLE)                            AS price
            FROM (
                SELECT
                    market_id, timestamp, price,
                    row_number() OVER (
                        PARTITION BY market_id, timestamp ORDER BY price
                    ) AS _rn
                FROM "polymarket-price-history"
                WHERE market_id IS NOT NULL
                  AND timestamp IS NOT NULL
                  AND price IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
