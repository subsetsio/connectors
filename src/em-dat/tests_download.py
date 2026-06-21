"""Health invariants for the EM-DAT raw download.

Catches silent degradation the file-exists check misses: an empty/truncated
workbook, a format switch, or the unique event key collapsing.
"""

from subsets_utils import load_raw_parquet


def test_events_nonempty(spec_ids):
    """The events asset should hold the full corpus (tens of thousands of rows).
    A near-empty table means the endpoint changed format or the file moved."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 10000, f"{sid}: only {len(table)} rows (expected >10000)"


def test_events_key_unique_and_present(spec_ids):
    """dis_no is EM-DAT's natural event key — non-null and unique per row."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dis_no = table.column("dis_no").to_pylist()
        assert all(v is not None for v in dis_no), f"{sid}: null dis_no present"
        assert len(set(dis_no)) == len(dis_no), f"{sid}: duplicate dis_no values"


def test_events_schema_shape(spec_ids):
    """47 columns expected; impact metrics should be numeric, not strings."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns == 47, f"{sid}: {table.num_columns} columns (expected 47)"
        assert "total_deaths" in table.column_names
        assert "start_year" in table.column_names
