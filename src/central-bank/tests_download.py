"""Health invariants for the central-bank raw assets.

Each download node writes a uniform long-format parquet:
(period, date, series, series_index, value). These tests catch silent
degradation that file-existence alone misses — empty payloads, an all-null
date column (period-format drift), or a value column that no longer parses to
numbers (the endpoint changed shape).
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every .px table has history; an empty parquet means the dataapi/Get
    response lost its dataSets (format/endpoint change)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_period_and_series_present(spec_ids):
    """period and series are structural; a fully-null column means the flatten
    dropped the period code or the cross-product labelling broke."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.column("period").null_count == 0, f"{sid}: null period values"
        assert t.column("series").null_count == 0, f"{sid}: null series labels"


def test_dates_mostly_parse(spec_ids):
    """The period -> ISO date mapping should resolve for the vast majority of
    rows; a table where almost nothing parses signals an unknown period format."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        n = t.num_rows
        if not n:
            continue
        parsed = n - t.column("date").null_count
        assert parsed >= 0.9 * n, (
            f"{sid}: only {parsed}/{n} rows have a parseable date")


def test_values_parse_to_numbers(spec_ids):
    """At least some cells must be numeric after stripping commas — a table
    where nothing casts to a number means the value column is no longer data."""
    import re
    num = re.compile(r"^-?\d+(\.\d+)?$")
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        vals = t.column("value").to_pylist()
        if not vals:
            continue
        numeric = sum(1 for v in vals if v and num.match(v.replace(",", "")))
        assert numeric > 0, f"{sid}: no numeric values among {len(vals)} cells"
