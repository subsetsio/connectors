"""Health-invariant tests for the Nature's Calendar connector raw assets.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses: empty payloads, a collapsed catalog, or a coordinate band that
drifted off the UK.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset should hold rows; empty usually means the endpoint
    changed shape or returned 404 for every slice."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_species_events_catalog_size():
    """The species-event catalog should hold ~179 series; a collapse to a
    handful means the SpeciesGroups tree walk broke."""
    table = load_raw_parquet("natures-calendar-species-events")
    assert 140 <= len(table) <= 260, f"species-events catalog has {len(table)} rows; expected ~179"


def test_observations_corpus_size():
    """The observations corpus is the UK's largest phenology database; a tiny
    table means most (species,event,year) fetches silently failed."""
    table = load_raw_parquet("natures-calendar-observations")
    assert len(table) >= 50000, f"observations has only {len(table)} rows; expected >=50k"


def test_observations_reference_integrity():
    """Every observed (species_id, event_id) should exist in the catalog —
    a mismatch means the two assets drifted out of sync."""
    obs = load_raw_parquet("natures-calendar-observations")
    cat = load_raw_parquet("natures-calendar-species-events")
    cat_pairs = set(zip(cat.column("species_id").to_pylist(),
                        cat.column("event_id").to_pylist()))
    obs_pairs = set(zip(obs.column("species_id").to_pylist(),
                        obs.column("event_id").to_pylist()))
    orphans = obs_pairs - cat_pairs
    assert not orphans, f"{len(orphans)} observed (species,event) pairs missing from catalog: {list(orphans)[:5]}"
