from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw BULK parquet must hold rows. An empty payload means
    the BULK endpoint changed format, the table was retired, or the stream
    truncated silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present(spec_ids):
    """StatBank BULK always carries the value column INDHOLD plus at least one
    dimension column. Fewer than 2 columns means the semicolon-CSV parse broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = {c.upper() for c in table.column_names}
        assert "INDHOLD" in cols, f"{sid}: no INDHOLD value column (cols={table.column_names})"
        assert table.num_columns >= 2, f"{sid}: only {table.num_columns} column(s)"
