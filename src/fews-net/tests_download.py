"""Post-DAG health invariants for FEWS NET raw downloads.

Each download streams to a single `<asset>.ndjson.gz`. We assert the file
exists for every download spec — a cheap existence check that flags a silently
empty/missing fetch without loading multi-million-row corpora into memory.
"""

from subsets_utils import raw_asset_exists


def test_all_raw_assets_present(spec_ids):
    downloads = [s for s in spec_ids if not s.endswith("-transform")]
    missing = [s for s in downloads if not raw_asset_exists(s, "ndjson.gz")]
    assert not missing, f"missing raw ndjson.gz for: {missing}"
