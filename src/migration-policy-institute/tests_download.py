"""Health-invariant tests for the MPI Data Hub connector.

Catch silent degradation the file-exists check misses: an empty/truncated
download, or a workbook whose layout changed so the generic extractor parsed no
numeric values.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold cells. Empty usually means the file
    moved (Cloudflare/404) or the workbook failed to parse."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_assets_have_numeric_values(spec_ids):
    """Each MPI table is fundamentally numeric (counts, shares, years). If every
    value_num is null the layout shifted and we extracted only text/garbage."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value_num")
        non_null = len(col) - col.null_count
        assert non_null > 0, f"{sid}: extracted 0 numeric values (value_num all null)"
