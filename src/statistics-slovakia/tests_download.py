from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has no rows"


def test_raw_schema_is_stable(spec_ids):
    expected = {
        "table_code",
        "table_label",
        "source_updated",
        "row_index",
        "slice_id",
        "dimensions_json",
        "dimension_labels_json",
        "value_number",
        "value_text",
    }
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert set(table.column_names) == expected, f"{spec_id}: unexpected columns {table.column_names}"
