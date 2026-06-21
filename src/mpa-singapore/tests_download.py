"""Health-invariant tests for MPA Singapore raw downloads."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset CSV should yield rows. An empty parquet means the
    poll-download flow returned an error body or the CSV format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_has_time_column(spec_ids):
    """Each MPA table is a time series keyed by `month` (YYYY-MM) or `year`.
    Losing it means the schema drifted and the transform's date cast breaks."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).column_names
        assert "month" in cols or "year" in cols, (
            f"{sid}: no month/year column, got {cols}"
        )
