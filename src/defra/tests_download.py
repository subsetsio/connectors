"""Health-invariant tests for the DEFRA connector raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the fetch
nodes wrote with. They catch silent degradation that file-existence misses:
empty payloads, truncated downloads, format switches.
"""

from subsets_utils import load_raw_ndjson

# Loose floors per asset — well below observed counts, tight enough that a
# pagination break (1 page) or a switched/empty endpoint trips them.
_MIN_ROWS = {
    "defra-flood-monitoring-stations": 1000,
    "defra-flood-monitoring-measures": 1000,
    "defra-flood-monitoring-readings": 500,
    "defra-flood-monitoring-floods": 1000,
    "defra-hydrology-stations": 1000,
    "defra-hydrology-measures": 1000,
    "defra-hydrology-readings": 1000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows above its floor."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows, expected >= {floor}"


def test_keys_present(spec_ids):
    """First record of each asset must carry its identifying key — guards
    against a flatten that silently dropped to empty dicts."""
    id_key = {
        "defra-flood-monitoring-stations": "notation",
        "defra-flood-monitoring-measures": "notation",
        "defra-flood-monitoring-readings": "measure_id",
        "defra-flood-monitoring-floods": "notation",
        "defra-hydrology-stations": "notation",
        "defra-hydrology-measures": "notation",
        "defra-hydrology-readings": "measure_id",
    }
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        key = id_key[sid]
        present = sum(1 for r in rows[:1000] if r.get(key) is not None)
        assert present > 0, f"{sid}: no records carry '{key}' in first 1000 rows"
