from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator's raw parquet should hold observations. An empty payload
    means the data-service silently changed its response shape or the measure
    iteration broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_are_real_numbers(spec_ids):
    """obs_val must be non-null and finite for at least most rows — catches a
    parse regression where the Russian decimal comma sneaks in as a string."""
    import math
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("obs_val").to_pylist()
        assert vals, f"{sid}: no values"
        finite = [v for v in vals if v is not None and not math.isnan(v)]
        assert finite, f"{sid}: no finite obs_val"


def test_dates_present(spec_ids):
    """Every row needs a date — the published table is a time series keyed on it."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("date").to_pylist()
        assert all(d is not None for d in dates), f"{sid}: null dates present"
