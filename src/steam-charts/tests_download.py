from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_games_catalog_has_pagination_depth(spec_ids):
    if "steam-charts-games" not in spec_ids:
        return
    table = load_raw_parquet("steam-charts-games")
    assert len(table) >= 100, f"games catalog unexpectedly small: {len(table)} rows"
    assert table.column("source_page").to_pylist()
    assert max(table.column("source_page").to_pylist()) >= 4, "top-page pagination stopped too early"


def test_temporal_assets_have_history(spec_ids):
    if "steam-charts-monthly-stats" in spec_ids:
        table = load_raw_parquet("steam-charts-monthly-stats")
        assert len(table) >= 1000, f"monthly stats unexpectedly small: {len(table)} rows"
    if "steam-charts-chart-values" in spec_ids:
        table = load_raw_parquet("steam-charts-chart-values")
        assert len(table) >= 1000, f"chart values unexpectedly small: {len(table)} rows"
