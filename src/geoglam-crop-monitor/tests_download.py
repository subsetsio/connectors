from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_shaped(spec_ids):
    """Raw must hold the full multi-month corpus with the expected columns.
    An empty/tiny payload or missing columns means the FeatureServer changed
    format, the TLS chain broke silently, or pagination stopped after page 1."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} rows"
        cols = set(table.column_names)
        expected = {"period", "country", "region", "crop", "conditions", "drivers"}
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"


def test_raw_period_coverage(spec_ids):
    """Each monthly layer contributes one distinct period; too few means we
    only read a handful of layers instead of the whole service."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        periods = set(table.column("period").to_pylist())
        assert len(periods) >= 24, f"{sid}: only {len(periods)} distinct periods"
        assert all(p and len(p) == 6 and p.isdigit() for p in periods), \
            f"{sid}: malformed period values present"
