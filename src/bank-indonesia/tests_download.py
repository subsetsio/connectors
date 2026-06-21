from subsets_utils import load_raw_parquet


def test_all_raw_nonempty(spec_ids):
    """Every product's raw parquet must hold rows; empty means the endpoint
    switched format or the feature got disabled silently."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert len(t) > 0, f"{sid}: raw parquet has 0 rows"


def test_rates_and_currencies(spec_ids):
    """Buy rates must be positive numbers, and the multi-currency products must
    expose several currencies while JISDOR stays USD-only."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).to_pydict()
        buys = [b for b in cols["buy"] if b is not None]
        assert buys, f"{sid}: no buy rates present"
        assert all(b > 0 for b in buys), f"{sid}: non-positive buy rates"
        currencies = {c for c in cols["currency"] if c}
        if sid.endswith("jisdor"):
            assert currencies == {"USD"}, f"{sid}: expected USD-only, got {sorted(currencies)}"
        else:
            assert len(currencies) >= 5, f"{sid}: only {len(currencies)} currencies: {sorted(currencies)}"
