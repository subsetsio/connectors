"""Polymarket downloads: Gamma events/markets and CLOB daily price history."""
import json

from subsets_utils import NodeSpec, raw_writer

from utils import _date, _f, _get_json, _i, _keyset_pages

CLOB_PRICES_URL = "https://clob.polymarket.com/prices-history"

PRICE_HISTORY_MIN_VOLUME_USD = 100_000
PRICE_FIDELITY_MINUTES = 1440


def _event_row(e: dict) -> dict:
    markets = e.get("markets") or []
    return {
        "event_id": e.get("id"),
        "ticker": e.get("ticker"),
        "slug": e.get("slug"),
        "title": e.get("title"),
        "category": e.get("category"),
        "description": e.get("description"),
        "volume_usd": _f(e.get("volume")),
        "volume_24h_usd": _f(e.get("volume24hr")),
        "volume_1wk_usd": _f(e.get("volume1wk")),
        "volume_1mo_usd": _f(e.get("volume1mo")),
        "volume_1yr_usd": _f(e.get("volume1yr")),
        "liquidity_usd": _f(e.get("liquidity")),
        "open_interest": _f(e.get("openInterest")),
        "comment_count": _i(e.get("commentCount")),
        "competitive": _f(e.get("competitive")),
        "neg_risk": bool(e.get("enableNegRisk") or e.get("negRisk") or e.get("negRiskAugmented")),
        "is_active": bool(e.get("active")),
        "is_closed": bool(e.get("closed")),
        "is_archived": bool(e.get("archived")),
        "is_featured": bool(e.get("featured")),
        "is_restricted": bool(e.get("restricted")),
        "market_count": len(markets),
        "start_date": _date(e.get("startDate")),
        "end_date": _date(e.get("endDate")),
        "creation_date": _date(e.get("creationDate")),
        "created_at": e.get("createdAt"),
        "updated_at": e.get("updatedAt"),
    }


def _yes_no_prices(outcomes_str, prices_str):
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


def _scoped_binary_markets():
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


def fetch_events(node_id: str) -> None:
    total = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for rows in _keyset_pages("events"):
            for e in rows:
                if not e.get("id"):
                    continue
                f.write(json.dumps(_event_row(e)) + "\n")
                total += 1
            print(f"    events: {total:,} written")
    print(f"  events: wrote {total:,} rows")


def fetch_markets(node_id: str) -> None:
    total = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for closed in ("false", "true"):
            for rows in _keyset_pages("markets", {"closed": closed}):
                for m in rows:
                    if not m.get("id"):
                        continue
                    f.write(json.dumps(_market_row(m)) + "\n")
                    total += 1
                print(f"    markets (closed={closed}): {total:,} written")
    print(f"  markets: wrote {total:,} rows")


def fetch_price_history(node_id: str) -> None:
    scoped = list(_scoped_binary_markets())
    print(
        f"  price-history: {len(scoped):,} binary markets over "
        f"${PRICE_HISTORY_MIN_VOLUME_USD:,} volume"
    )

    total_points = 0
    done = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
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
                print(
                    f"    price-history: {done:,}/{len(scoped):,} markets, "
                    f"{total_points:,} points"
                )
    print(f"  price-history: wrote {total_points:,} points across {done:,} markets")


DOWNLOAD_SPECS = [
    NodeSpec(id="polymarket-events", fn=fetch_events, kind="download"),
    NodeSpec(id="polymarket-markets", fn=fetch_markets, kind="download"),
    NodeSpec(id="polymarket-price-history", fn=fetch_price_history, kind="download"),
]
