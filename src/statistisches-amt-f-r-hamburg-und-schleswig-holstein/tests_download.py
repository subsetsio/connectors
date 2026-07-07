from subsets_utils import load_raw_ndjson


REQUIRED_COLUMNS = {
    "package_id",
    "resource_id",
    "resource_format",
    "sheet_name",
    "row_number",
    "column_number",
    "value_text",
}


def test_all_raw_assets_have_cells(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no parsed cell records"


def test_cell_records_have_expected_shape(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = REQUIRED_COLUMNS - set(rows[0])
        assert not missing, f"{spec_id}: missing columns {sorted(missing)}"
        assert any(row.get("value_text") for row in rows[:200]), f"{spec_id}: first rows are blank"
