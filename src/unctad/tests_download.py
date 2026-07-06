from subsets_utils import load_raw_parquet


def test_raw_parquet_assets_are_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has 0 rows"
        assert table.num_columns > 0, f"{spec_id}: raw parquet has 0 columns"
