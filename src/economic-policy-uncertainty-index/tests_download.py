"""Health invariants for the EPU connector raw assets.

Every download node normalises its source file to the uniform long schema
[date, series, value]. These tests catch silent degradation (empty payload,
truncated download, parser regression) that file-existence alone misses.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Each spec's raw parquet must hold rows. Empty usually means the source
    file moved/changed format or the GET returned an error page."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_is_long_format(spec_ids):
    """Raw must be exactly the [date, series, value] long schema every transform
    expects; a drift here means the parser emitted something unexpected."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).schema.names)
        assert {"date", "series", "value"} <= cols, f"{sid}: columns {cols}"


def test_value_not_all_null(spec_ids):
    """The parser drops null values, so every asset should have real numbers.
    An all-null value column means every cell failed numeric coercion."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(table), f"{sid}: value column is entirely null"


def test_series_populated(spec_ids):
    """Every row must carry a non-empty series label (the column/dimension name)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        series = table.column("series")
        assert series.null_count == 0, f"{sid}: {series.null_count} null series labels"
