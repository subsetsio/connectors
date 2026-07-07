"""Post-DAG health invariants for the Bank of Canada connector.

These run in-connector after the fetches, loading raw through the same
subsets_utils loaders the download nodes used to write it.
"""
from subsets_utils import list_raw_files, load_raw_parquet


def test_catalog_assets_nonempty():
    """The two catalog snapshots must hold rows — an empty list endpoint
    means the API changed shape or returned an error envelope."""
    for sid in ("bank-of-canada-groups", "bank-of-canada-series"):
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_catalog_keys_present():
    """Each catalog row must carry its identifier; nulls there mean the
    parse silently dropped the dict key."""
    groups = load_raw_parquet("bank-of-canada-groups")
    assert groups.column("group_id").null_count == 0, "groups: null group_id"
    series = load_raw_parquet("bank-of-canada-series")
    assert series.column("series_id").null_count == 0, "series: null series_id"


def test_observations_batches_present_and_nonempty():
    """Observations are written as batch files (<asset>-<NNNNN>). At least one
    batch must exist and every batch must carry usable series/value rows. Some
    upstream payload rows can have blank dates; the transform drops them."""
    files = list_raw_files("bank-of-canada-observations-*.parquet")
    assert files, "no observation batch files written"
    total = 0
    dated = 0
    for path in files:
        asset_id = path[:-len(".parquet")]
        table = load_raw_parquet(asset_id)
        assert len(table) > 0, f"{asset_id}: observation batch has 0 rows"
        assert table.column("series_id").null_count == 0, f"{asset_id}: null series_id"
        total += len(table)
        dated += len(table) - table.column("obs_date").null_count
    assert total > 0, "observation batches hold no rows"
    assert dated > 100000, f"only {dated} dated observation rows across all batches"
