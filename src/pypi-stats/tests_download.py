from subsets_utils import load_raw_parquet


EXPECTED_TOP_PACKAGE_COUNT = 21


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has 0 rows"


def test_every_asset_covers_top_packages(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        packages = set(table.column("package").to_pylist())
        assert len(packages) == EXPECTED_TOP_PACKAGE_COUNT, (
            f"{spec_id}: expected {EXPECTED_TOP_PACKAGE_COUNT} packages, got {len(packages)}"
        )


def test_timeseries_assets_have_recent_dates(spec_ids):
    for spec_id in spec_ids:
        if spec_id == "pypi-stats-recent-downloads":
            continue
        table = load_raw_parquet(spec_id)
        max_date = max(table.column("date").to_pylist())
        assert max_date is not None, f"{spec_id}: date column is empty"
