"""Health invariants for ONS raw downloads.

Each dataset's raw asset is a parquet table with a `value` column (the typed
observation) plus one or more dimension columns. We assert every asset loaded,
holds rows, and carries the `value` column — empty payloads or a missing value
column mean the CSV format drifted or the download silently truncated.
"""
from subsets_utils import load_raw_parquet


def test_all_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, (
            f"{sid}: no 'value' column (cols={table.column_names[:8]})"
        )


def test_has_dimension_columns(spec_ids):
    """Every ONS table is value + at least one dimension; a lone value column
    means the header parse collapsed."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).column_names
        assert len(cols) >= 2, f"{sid}: only columns {cols}"
