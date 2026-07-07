from subsets_utils import load_raw_parquet


def test_all_raw_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw table has no rows"


def test_all_raw_assets_have_values(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        value_index = table.schema.get_field_index("value")
        text_index = table.schema.get_field_index("value_text")
        numeric_count = table.column(value_index).combine_chunks().drop_null().length()
        text_count = table.column(text_index).combine_chunks().drop_null().length()
        assert numeric_count + text_count > 0, f"{spec_id}: no observation values found"


def test_temporal_assets_have_periods(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        period_index = table.schema.get_field_index("period")
        period_count = table.column(period_index).combine_chunks().drop_null().length()
        assert period_count > 0, f"{spec_id}: no period values found"
