"""Health-invariant tests for the DPIIT connector raw assets.

These run post-DAG in-connector and catch silent degradation that file
existence alone misses — empty payloads, truncated downloads, a wide-to-long
melt that collapsed, a sheet that stopped parsing.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. Empty usually means the endpoint
    returned a placeholder stub (stale rolling filename) or the format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_wpi_values_is_long_and_deep(spec_ids):
    """WPI values is the wide monthly matrix melted to long form; it must carry
    far more rows than the catalog and span many months."""
    if "dpiit-wpi-values" not in spec_ids:
        return
    t = load_raw_parquet("dpiit-wpi-values")
    assert len(t) >= 50000, f"dpiit-wpi-values: only {len(t)} rows; melt likely collapsed"
    months = set(t.column("date").to_pylist())
    assert len(months) >= 100, f"dpiit-wpi-values: only {len(months)} distinct months"


def test_core_has_nine_sectors(spec_ids):
    """The Index of Eight Core Industries must expose exactly the 8 sectors +
    the combined Overall index; a different count means the sheet layout moved."""
    if "dpiit-core-industries" not in spec_ids:
        return
    t = load_raw_parquet("dpiit-core-industries")
    sectors = set(t.column("sector").to_pylist())
    assert len(sectors) == 9, f"dpiit-core-industries: {len(sectors)} sectors, expected 9: {sorted(sectors)}"
