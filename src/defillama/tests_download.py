"""Health-invariant tests for the DefiLlama raw downloads.

Each endpoint returns a full unpaginated table; a tiny/empty payload means the
endpoint silently changed format, got rate-gated, or auth flipped. Floors are
set well below observed volumes so normal fluctuation passes but a degraded
fetch trips.
"""
from subsets_utils import load_raw_ndjson

_FLOORS = {
    "defillama-protocols": 1000,
    "defillama-chains": 100,
    "defillama-historical-chain-tvl": 1000,
    "defillama-yield-pools": 1000,
    "defillama-stablecoins": 50,
    "defillama-fees": 100,
    "defillama-dex-volumes": 50,
    "defillama-options-volumes": 5,
}


def test_raw_assets_meet_floor(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _FLOORS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"


def test_key_columns_present(spec_ids):
    """Each table's identity column must be populated on the first row — guards
    against a response whose record shape changed underneath us."""
    key_col = {
        "defillama-protocols": "protocol_id",
        "defillama-chains": "chain",
        "defillama-historical-chain-tvl": "date",
        "defillama-yield-pools": "pool_id",
        "defillama-stablecoins": "stablecoin_id",
        "defillama-fees": "name",
        "defillama-dex-volumes": "name",
        "defillama-options-volumes": "name",
    }
    for sid in spec_ids:
        col = key_col.get(sid)
        if not col:
            continue
        rows = load_raw_ndjson(sid)
        assert rows and rows[0].get(col) is not None, f"{sid}: key column '{col}' missing/null on first row"
