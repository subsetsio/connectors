"""Health invariants for the Atlantic Council raw assets.

Catch silent degradation the per-node YAML specs miss: a manifest that
quietly shrank (pagination/format break) or a chartProfiles fetch that
returned truncated payloads.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_full_corpus():
    """183 entities x 30 years x 24 indicators ~= 131k rows. A big shortfall
    means an entity loop or a manifest fetch silently dropped entities."""
    table = load_raw_parquet("atlantic-council-values")
    assert table.num_rows >= 120000, f"values rows={table.num_rows}; expected ~131k"
    entities = set(table.column("entity_id").to_pylist())
    assert len(entities) >= 180, f"only {len(entities)} distinct entities; expected ~183"


def test_entities_count():
    table = load_raw_parquet("atlantic-council-entities")
    assert 180 <= table.num_rows <= 200, f"entities rows={table.num_rows}; expected ~183"


def test_indicators_codebook():
    table = load_raw_parquet("atlantic-council-indicators")
    assert table.num_rows == 24, f"indicators rows={table.num_rows}; expected 24"
