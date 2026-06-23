"""Health invariants for the FRBSF connector, run post-DAG inside the connector.

Catches silent degradation the file-exists check misses: an indicator page that
stopped linking its xlsx (→ empty raw), a workbook whose layout changed so the
melt found no series, or a date axis that stopped parsing (→ all-null dates).
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator must yield long-format observations. 0 rows means the
    xlsx link vanished or the melt failed to recognise any data sheet."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_has_expected_columns(spec_ids):
    expected = {"sheet", "period", "date", "dimension", "series", "value"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"


def test_dates_mostly_parse(spec_ids):
    """The first column of every FRBSF indicator is a time axis. If fewer than
    half the rows have a parsed date, the date-axis detection broke (e.g. a new
    period format like 'YYYY:Qn' the parser doesn't recognise)."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            continue
        non_null = pc.sum(pc.is_valid(t.column("date"))).as_py() or 0
        frac = non_null / t.num_rows
        assert frac >= 0.5, f"{sid}: only {frac:.0%} of rows have a parsed date"


def test_series_named(spec_ids):
    """Every observation must carry a non-empty series label."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            continue
        bad = pc.sum(pc.invert(pc.is_valid(t.column("series")))).as_py() or 0
        assert bad == 0, f"{sid}: {bad} rows have a null series label"
