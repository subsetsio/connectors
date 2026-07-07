"""Health-invariant tests for OPHI Global MPI raw downloads."""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "release_year",
    "table_number",
    "workbook_filename",
    "sheet_name",
    "row_index",
    "column_index",
    "value_text",
    "value_number",
    "value_bool",
    "value_type",
}


def test_raw_assets_have_cell_rows(spec_ids):
    """Every workbook should parse to a non-trivial non-empty cell grid."""
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert len(table) >= 100, f"{spec_id}: parsed only {len(table)} cells"


def test_raw_schema_stable(spec_ids):
    """The transform stage depends on the common cell-grid schema."""
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert set(table.column_names) == EXPECTED_COLUMNS, f"{spec_id}: unexpected columns {table.column_names}"


def test_each_asset_has_numeric_cells(spec_ids):
    """These are statistical tables; no numeric cells means the workbook parse degraded."""
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        values = table.to_pydict()
        numeric = [v for v in values["value_number"] if v is not None]
        assert len(numeric) >= 10, f"{spec_id}: only {len(numeric)} numeric cells"


def test_table_number_matches_spec_id(spec_ids):
    """The table number in raw should match the accepted table entity id."""
    for spec_id in spec_ids:
        expected = int(spec_id.rsplit("-", 1)[1])
        table = load_raw_parquet(spec_id)
        got = set(table.to_pydict()["table_number"])
        assert got == {expected}, f"{spec_id}: raw table numbers {sorted(got)}"
