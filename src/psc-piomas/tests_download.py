from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every product's raw parquet should hold rows. Empty means the endpoint
    switched format or the gzip/CSV parse silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_daily_spans_full_history(spec_ids):
    """Daily series cover 1979-present (~17k days). A truncated download (e.g.
    only the latest year fetched) would trip this."""
    for sid in spec_ids:
        if "daily" in sid:
            n = len(load_raw_parquet(sid))
            assert n > 15000, f"{sid}: only {n} daily rows; download truncated?"


def test_monthly_history_present(spec_ids):
    """Monthly volume spans 1979-present (~560 months)."""
    for sid in spec_ids:
        if "monthly" in sid:
            n = len(load_raw_parquet(sid))
            assert n > 500, f"{sid}: only {n} monthly rows; download truncated?"
