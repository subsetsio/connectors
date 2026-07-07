from subsets_utils import load_raw_parquet


def test_cpi_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= 100, f"{spec_id}: expected monthly CPI history, got {table.num_rows} rows"


def test_cpi_raw_contains_required_measures(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        measures = set(table.column("measure").to_pylist())
        assert measures == {"index_2020_100", "annual_change_pct"}, f"{spec_id}: measures={measures!r}"
