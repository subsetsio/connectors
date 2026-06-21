"""Health invariants for the Agmarknet raw snapshot.

These run post-DAG, in-connector, and catch silent degradation that file
existence alone misses — a truncated crawl, a schema swap, an empty snapshot.
"""

from subsets_utils import load_raw_ndjson

EXPECTED_FIELDS = {
    "state", "district", "market", "commodity", "variety",
    "grade", "arrival_date", "min_price", "max_price", "modal_price",
}


def test_snapshot_substantial(spec_ids):
    """The daily snapshot has held ~18k rows; far fewer means the window-scan
    crawl truncated or the resource went (nearly) empty."""
    rows = load_raw_ndjson("agmarknet-prices")
    assert len(rows) >= 5000, f"agmarknet-prices: only {len(rows)} rows (expected ~18k)"


def test_schema_stable(spec_ids):
    """Every record must carry the 10 known fields; a missing field means the
    upstream resource schema drifted."""
    rows = load_raw_ndjson("agmarknet-prices")
    sample = rows[: min(2000, len(rows))]
    for r in sample:
        missing = EXPECTED_FIELDS - set(r.keys())
        assert not missing, f"record missing fields {missing}: {r}"


def test_state_coverage(spec_ids):
    """India reports prices from many states/UTs; the two-pass+boundary crawl
    must surface a broad spread. A handful of states means coverage collapsed
    to a single window."""
    rows = load_raw_ndjson("agmarknet-prices")
    states = {r.get("state") for r in rows}
    assert len(states) >= 15, f"only {len(states)} distinct states: {sorted(states)}"


def test_prices_numeric(spec_ids):
    """Modal price should parse as a number on the vast majority of rows;
    wholesale corruption (e.g. the field turning into text) trips this."""
    rows = load_raw_ndjson("agmarknet-prices")
    sample = rows[: min(2000, len(rows))]
    ok = 0
    for r in sample:
        try:
            float(r.get("modal_price"))
            ok += 1
        except (TypeError, ValueError):
            pass
    assert ok >= 0.9 * len(sample), f"only {ok}/{len(sample)} modal_price values numeric"
