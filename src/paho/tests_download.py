"""Post-DAG health invariants for PAHO raw assets."""

from subsets_utils import load_raw_parquet


def test_values_substantial_and_joinable():
    table = load_raw_parquet("paho-core-indicator-values")
    assert table.num_rows >= 300_000, f"values: {table.num_rows} rows; expected at least 300k"
    indicator_ids = set(table.column("paho_indicator_id").to_pylist())
    assert len(indicator_ids) >= 290, f"values: only {len(indicator_ids)} distinct indicators"
    geos = set(table.column("spatial_dim").to_pylist())
    assert len(geos) >= 45, f"values: only {len(geos)} distinct geographies"


def test_indicators_catalog_matches_values():
    values = load_raw_parquet("paho-core-indicator-values")
    indicators = load_raw_parquet("paho-core-indicators")
    value_ids = set(values.column("paho_indicator_id").to_pylist())
    catalog_ids = set(indicators.column("paho_indicator_id").to_pylist())
    assert indicators.num_rows >= 290, f"indicators: {indicators.num_rows} rows; expected at least 290"
    assert catalog_ids == value_ids, "indicator catalog ids do not match values ids"
