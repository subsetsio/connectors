"""Health-invariant tests for the USDA NASS download stage.

The loader node materializes one raw parquet per commodity. These tests catch
silent degradation — empty payloads, a sector dump that failed to stream, or
the schema drifting — without re-downloading anything.
"""
from subsets_utils import load_raw_parquet

# Flagship commodities whose raw assets must always be present and substantial.
_FLAGSHIPS = (
    "usda-nass-corn",
    "usda-nass-soybeans",
    "usda-nass-wheat",
    "usda-nass-cattle",
    "usda-nass-milk",
)

_EXPECTED_COLS = {
    "SOURCE_DESC", "SECTOR_DESC", "COMMODITY_DESC", "STATISTICCAT_DESC",
    "SHORT_DESC", "UNIT_DESC", "AGG_LEVEL_DESC", "YEAR", "VALUE",
}


def test_flagship_assets_nonempty():
    """The headline commodities must hold rows; empty means a sector dump
    failed to download or the partition split dropped the commodity."""
    for aid in _FLAGSHIPS:
        t = load_raw_parquet(aid)
        assert t.num_rows > 0, f"{aid}: raw parquet has 0 rows"


def test_raw_schema_has_core_columns():
    """Every raw asset must carry the core NASS columns (incl. the restored
    COMMODITY_DESC partition column) — a schema drift breaks every transform."""
    t = load_raw_parquet("usda-nass-corn")
    cols = set(t.column_names)
    missing = _EXPECTED_COLS - cols
    assert not missing, f"usda-nass-corn missing columns {missing}; have {sorted(cols)}"


def test_corn_single_commodity_and_deep_history(spec_ids):
    """Each commodity asset must contain ONLY its own commodity (the partition
    filter worked) and corn must span many decades (the YEAR column parsed)."""
    import pyarrow.compute as pc
    t = load_raw_parquet("usda-nass-corn")
    commodities = set(pc.unique(t.column("COMMODITY_DESC")).to_pylist())
    assert commodities == {"CORN"}, f"usda-nass-corn carries other commodities: {commodities}"
    years = [int(y) for y in pc.unique(t.column("YEAR")).to_pylist() if str(y).isdigit()]
    assert years and min(years) <= 1950, f"corn earliest year {min(years) if years else None} (expected deep history)"
