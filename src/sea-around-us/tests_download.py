"""Post-DAG health invariants for the Sea Around Us connector.

These run in-connector after the download nodes, loading raw via the same
subsets_utils loaders the fetch fns used. They catch silent degradation that
file-existence checks miss: empty payloads, truncated region enumeration,
wrong column shapes.
"""

from subsets_utils import load_raw_parquet

CATCH_COLS = {
    "region_type", "region_id", "region_name", "category",
    "scientific_name", "entity_id", "year", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset must hold rows. An empty payload usually means
    the endpoint switched shape or region enumeration broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_catch_schema_and_regions(spec_ids):
    """Catch tables must carry the expected columns and span more than one
    region type — if region enumeration silently fell back to global only, the
    per-region crawl is broken."""
    for sid in spec_ids:
        if "-catch-" not in sid:
            continue
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        missing = CATCH_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"
        region_types = set(table.column("region_type").to_pylist())
        assert len(region_types) >= 2, (
            f"{sid}: only region types {region_types}; region crawl likely broke"
        )
        years = table.column("year").to_pylist()
        assert min(years) <= 1955, f"{sid}: earliest year {min(years)} > 1955"


def test_taxa_reference(spec_ids):
    """The taxa reference must look like the full taxonomy."""
    if "sea-around-us-taxa" not in spec_ids:
        return
    table = load_raw_parquet("sea-around-us-taxa")
    assert len(table) >= 2000, f"taxa: only {len(table)} rows"
    keys = table.column("taxon_key").to_pylist()
    assert len(set(keys)) == len(keys), "taxa: duplicate taxon_key values"
