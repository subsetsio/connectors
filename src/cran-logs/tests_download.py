from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty payloads usually mean
    the endpoint changed shape or the catalog fetch degraded silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_package_downloads_breadth(spec_ids):
    """The package-downloads asset must span thousands of distinct packages;
    a tiny distinct count means batching broke after the first request."""
    sid = "cran-logs-package-downloads"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    distinct = len(set(table.column("package").to_pylist()))
    assert distinct >= 10000, f"{sid}: only {distinct} distinct packages; expected >=10000"
