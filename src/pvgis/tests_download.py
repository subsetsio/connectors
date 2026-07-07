import pyarrow.compute as pc

from subsets_utils import load_raw_parquet


def test_raw_assets_have_expected_size(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert len(table) > 2000, f"{spec_id}: raw table has only {len(table)} rows"


def test_country_and_metric_coverage(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        country_count = len(pc.unique(table["country_code"]))
        metric_count = len(pc.unique(table["metric_group"]))
        assert country_count >= 30, f"{spec_id}: expected at least 30 countries, got {country_count}"
        assert metric_count >= 7, f"{spec_id}: expected at least 7 metric groups, got {metric_count}"


def test_values_are_positive(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        minimum = pc.min(table["value"]).as_py()
        maximum = pc.max(table["value"]).as_py()
        assert minimum >= 0, f"{spec_id}: negative PVGIS statistic value {minimum}"
        assert maximum > 1000, f"{spec_id}: maximum value {maximum} is too small for irradiation/yield data"
