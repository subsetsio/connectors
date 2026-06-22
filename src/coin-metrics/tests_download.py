from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty payloads usually mean
    the endpoint changed shape or the community tier stopped returning data."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_long_format(spec_ids):
    """The values asset must be long-format (asset, metric, date, value) with a
    healthy metric spread — a collapse to one metric means melt broke."""
    sid = "coin-metrics-asset-metrics-values"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert set(["asset", "metric", "date", "value"]).issubset(table.column_names), table.column_names
    distinct_metrics = len(set(table.column("metric").to_pylist()))
    assert distinct_metrics >= 5, f"{sid}: only {distinct_metrics} distinct metrics"


def test_catalog_dictionary(spec_ids):
    """The metric dictionary should carry many metric definitions with codes."""
    sid = "coin-metrics-asset-metrics-catalog"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert "metric" in table.column_names
    assert len(table) >= 50, f"{sid}: only {len(table)} metric definitions"
