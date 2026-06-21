"""Health invariants for IAI raw downloads."""
from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"period_from", "period_to", "row_id", "row_name", "column_name", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every publication should parse to a non-trivial number of long-format
    rows. An empty or tiny payload means the endpoint changed or auth expired."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows >= 50, f"{sid}: only {table.num_rows} raw rows"
        assert EXPECTED_COLS.issubset(set(table.column_names)), (
            f"{sid}: unexpected columns {table.column_names}")


def test_values_finite(spec_ids):
    """Parsed values must be real numbers — a NaN/None leaking through means
    the null-skip in the parser broke."""
    import math
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value").to_pylist()
        bad = [v for v in col if v is None or (isinstance(v, float) and math.isnan(v))]
        assert not bad, f"{sid}: {len(bad)} non-finite values in raw"


def test_monthly_publications_have_recent_data(spec_ids):
    """The two monthly production series should carry data into at least 2023
    — a stale cutoff would signal a silently truncated fetch."""
    for sid in ("iai-primary-aluminium-production", "iai-alumina-production"):
        if sid not in spec_ids:
            continue
        periods = load_raw_parquet(sid).column("period_from").to_pylist()
        assert max(periods) >= "2023-01-01", f"{sid}: newest period is {max(periods)}"
