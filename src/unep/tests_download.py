"""Health-invariant tests for UNEP raw downloads.

Each download parses the source CSV(s) and saves typed parquet via
save_raw_parquet, so we read them back with load_raw_parquet and check the
payload has the expected columns and real data rows — catching silent
degradation (empty payload, truncated download, the endpoint switching format,
a quoting regression that shifts columns) that mere file existence misses.
"""

from subsets_utils import load_raw_parquet

# Expected columns per spec (subset; presence-checked).
_EXPECTED_COLS = {
    "unep-national": ["year", "adm0_code", "country_name", "permanent_sq_km", "seasonal_sq_km"],
    "unep-subnational-adm1": ["year", "adm0_code", "region_name", "permanent_sq_km", "seasonal_sq_km"],
    "unep-subnational-adm2": ["year", "adm0_code", "district_name", "permanent_sq_km", "seasonal_sq_km"],
    "unep-basins": ["year", "pfaf_id", "level", "permanent_sq_km", "seasonal_sq_km"],
}


def test_all_assets_have_expected_columns_and_rows():
    """Every spec's raw parquet holds its expected columns plus many rows."""
    for asset, cols in _EXPECTED_COLS.items():
        table = load_raw_parquet(asset)
        assert table.num_rows > 100, f"{asset}: only {table.num_rows} rows"
        for col in cols:
            assert col in table.column_names, f"{asset}: missing column {col!r} in {table.column_names}"


def test_year_in_expected_range():
    """The SDG 6.6.1 series spans 1984-2018 — guard against a parse that put the
    wrong column into `year` (the quoting bug that previously shifted columns)."""
    for asset in _EXPECTED_COLS:
        years = load_raw_parquet(asset).column("year").to_pylist()
        non_null = [y for y in years if y is not None]
        assert non_null, f"{asset}: no non-null years"
        assert min(non_null) >= 1980, f"{asset}: min year {min(non_null)} out of range"
        assert max(non_null) <= 2030, f"{asset}: max year {max(non_null)} out of range"


def test_basins_levels_complete():
    """basins must union all four HydroBASINS Pfafstetter levels (3-6)."""
    levels = set(load_raw_parquet("unep-basins").column("level").to_pylist())
    assert levels == {3, 4, 5, 6}, f"unep-basins: levels present = {levels}, expected 3-6"
