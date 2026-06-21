"""Health invariants for the Polymarket raw assets.

Catch silent degradation: a keyset cursor that stops advancing after one page,
an endpoint that switched shape, or a price-history scope that collapsed to
nothing. Raw is written as ndjson.gz via raw_writer, so we read it back with the
ndjson loader.
"""
import json

from subsets_utils import load_raw_ndjson


def test_markets_nonempty_and_rich(spec_ids):
    rows = load_raw_ndjson("polymarket-markets")
    # The full Polymarket corpus is well into six figures; if keyset paging broke
    # after the first page we would see ~100.
    assert len(rows) >= 10_000, f"markets: only {len(rows)} rows — keyset paging likely broke"
    sample = rows[0]
    for col in ("market_id", "question", "slug"):
        assert col in sample, f"markets: row missing '{col}': {sorted(sample)}"
    with_price = sum(1 for r in rows if r.get("outcome_yes_price") is not None)
    assert with_price > 0, "markets: no row has a parsed outcome_yes_price"


def test_events_nonempty(spec_ids):
    rows = load_raw_ndjson("polymarket-events")
    assert len(rows) >= 5_000, f"events: only {len(rows)} rows — keyset paging likely broke"
    assert all(r.get("event_id") for r in rows[:50]), "events: missing event_id in head"


def test_price_history_nonempty_and_bounded(spec_ids):
    rows = load_raw_ndjson("polymarket-price-history")
    assert len(rows) >= 10_000, f"price-history: only {len(rows)} points"
    markets = {r["market_id"] for r in rows}
    assert len(markets) >= 100, f"price-history: only {len(markets)} distinct markets"
    # prices are probabilities in [0, 1]
    bad = [r for r in rows[:5000] if not (0.0 <= r["price"] <= 1.0)]
    assert not bad, f"price-history: {len(bad)} points out of [0,1] range, e.g. {bad[:3]}"
    # timestamps are plausible unix seconds (2019..2032)
    ts = [r["timestamp"] for r in rows[:5000]]
    assert min(ts) > 1_546_300_800, "price-history: timestamp before 2019"
    assert max(ts) < 1_956_528_000, "price-history: timestamp after 2032"
