"""Health-invariant tests for blockchain-com-charts raw assets.

Run post-DAG inside the connector; they load raw through subsets_utils so they
behave identically locally and in the cloud.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every chart's raw parquet must hold rows. An empty payload means the
    endpoint changed format/slug or returned a non-ok status silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_columns_and_ranges(spec_ids):
    """Raw must expose exactly (x, y); x is a plausible unix-seconds timestamp
    (after 2008-10, before 2035) and never null. Catches a shape/format drift
    that would otherwise surface only after the transform mangles it."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == {"x", "y"}, f"{sid}: cols {table.column_names}"
        xs = table.column("x").to_pylist()
        assert all(x is not None for x in xs), f"{sid}: null x present"
        lo, hi = min(xs), max(xs)
        assert lo >= 1_220_000_000, f"{sid}: min x {lo} predates Bitcoin"
        assert hi <= 2_050_000_000, f"{sid}: max x {hi} implausibly far in the future"
