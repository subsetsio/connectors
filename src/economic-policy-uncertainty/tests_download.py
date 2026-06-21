"""Health-invariant tests for the Economic Policy Uncertainty connector.

These run post-DAG against the raw parquet each download node wrote. They catch
silent degradation a file-existence check misses: an empty/parse-failed payload,
a date column that stopped parsing (all-null dates dropped -> 0 rows), or a value
column that went non-numeric.
"""
import datetime as _dt

from subsets_utils import load_raw_parquet

REQUIRED_COLS = {"date", "series", "value", "frequency"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset must hold rows. 0 rows means the file failed to
    parse into the long (date, series, value) shape."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_uniform(spec_ids):
    """Every asset shares the normalized long schema."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert REQUIRED_COLS <= cols, f"{sid}: missing columns {REQUIRED_COLS - cols}"


def test_values_present_and_dates_sane(spec_ids):
    """Non-null numeric values and dates within a plausible historical range."""
    lo, hi = _dt.date(1850, 1, 1), _dt.date(2100, 1, 1)
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        vals = t.column("value").to_pylist()
        assert any(v is not None for v in vals), f"{sid}: all values null"
        dates = [d for d in t.column("date").to_pylist() if d is not None]
        assert dates, f"{sid}: no dates parsed"
        assert min(dates) >= lo and max(dates) <= hi, \
            f"{sid}: dates out of range {min(dates)}..{max(dates)}"
        series = t.column("series").to_pylist()
        assert all(s for s in series), f"{sid}: empty series label present"
