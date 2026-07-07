from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has no rows"


def test_expected_core_coverage():
    species = load_raw_parquet("pecbms-species")
    species_values = load_raw_parquet("pecbms-species-values")
    indicators = load_raw_parquet("pecbms-indicators")
    indicator_values = load_raw_parquet("pecbms-indicator-values")
    monitoring = load_raw_parquet("pecbms-monitoring-schemes")

    assert species.num_rows >= 160, f"species catalog too small: {species.num_rows}"
    assert species_values.num_rows >= 7000, f"species values too small: {species_values.num_rows}"
    assert indicators.num_rows >= 10, f"indicator catalog too small: {indicators.num_rows}"
    assert indicator_values.num_rows >= 400, f"indicator values too small: {indicator_values.num_rows}"
    assert monitoring.num_rows >= 50, f"monitoring schemes too small: {monitoring.num_rows}"
