"""Health-invariant tests for the CBE connector's raw download assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the fetch
nodes used. They catch silent degradation that file-existence alone misses:
empty payloads (WAF block / moved files), wrong format, all-null values.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset concatenates many fiscal-year workbooks; an empty raw asset
    means scraping found no files or the WAF served reject pages instead of XLSX."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_has_numbers(spec_ids):
    """The melted value column must hold real numeric observations, not all nulls."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(table), f"{sid}: value column is entirely null"


def test_has_dated_rows(spec_ids):
    """Most rows should carry a parsed date; a fully-null date column means the
    period-header parser failed to recognise this dataset's layout."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("date")
        assert dates.null_count < len(table), f"{sid}: no row has a parsed date"
