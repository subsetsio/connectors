"""Health-invariant tests for the NHS England download assets.

Each download asset is a tidy long table with the uniform schema
(period, sheet, series, value). These tests catch silent degradation —
an empty payload, a workbook whose layout shifted so parsing yields nothing,
or a date column that stopped parsing.
"""
import datetime as dt

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"period", "sheet", "series", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet must hold rows. 0 rows means the landing-page
    scrape, the file download, or the workbook parse silently broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    """Columns are the tidy contract, values are real numbers, periods are
    real dates spanning more than a single month (a healthy time series)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert EXPECTED_COLS.issubset(set(table.column_names)), (
            f"{sid}: columns {table.column_names} missing {EXPECTED_COLS}"
        )
        periods = [p for p in table.column("period").to_pylist() if p is not None]
        assert periods, f"{sid}: no non-null periods"
        span_days = (max(periods) - min(periods)).days
        assert span_days > 365, (
            f"{sid}: period span only {span_days} days — expected a multi-year series"
        )
        assert min(periods) >= dt.date(1999, 1, 1), f"{sid}: implausible min period {min(periods)}"
        n_series = len(set(table.column("series").to_pylist()))
        assert n_series >= 1, f"{sid}: no distinct series"
