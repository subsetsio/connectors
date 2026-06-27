"""Health-invariant tests for the NuGet connector raw assets."""
from subsets_utils import load_raw_parquet, list_raw_files


def test_packages_nonempty(spec_ids):
    """The search head must hold rows including download counts; an empty
    payload means search changed format or the skip loop broke."""
    if "nuget-packages" not in spec_ids:
        return
    table = load_raw_parquet("nuget-packages")
    assert table.num_rows > 0, "nuget-packages raw parquet has 0 rows"
    assert "total_downloads" in table.column_names, "missing total_downloads column"


def test_package_versions_batches_nonempty(spec_ids):
    """The catalog harvest writes one parquet per page-range batch. Missing
    batch files or an empty first batch means the harvest silently degraded."""
    if "nuget-package-versions" not in spec_ids:
        return
    files = list_raw_files("nuget-package-versions-*.parquet")
    assert files, "no nuget-package-versions batch files found"
    asset_id = files[0][: -len(".parquet")]
    table = load_raw_parquet(asset_id)
    assert table.num_rows > 0, f"{asset_id}: batch has 0 rows"
    for col in ("package_id", "version", "commit_timestamp"):
        assert col in table.column_names, f"{asset_id}: missing {col} column"
