"""Health invariants for the US Census Bureau raw assets.

Each download writes uniform EAV NDJSON (one record per response cell:
vintage / geo_level / row_id / variable / value). These tests catch silent
degradation that file-existence alone misses — empty payloads, a wholesale
auth/format failure, or value columns that arrived entirely null.
"""
from subsets_utils import load_raw_ndjson

_REQUIRED_KEYS = {"geo_level", "row_id", "variable", "value"}


def test_raw_assets_have_records(spec_ids):
    """Every dataset's raw asset should hold at least one EAV record. A run
    where many assets are empty usually means the API key is missing/invalid
    (the data path 200-redirects to an HTML page) rather than genuine gaps."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw asset(s) empty, e.g. {empty[:10]}"


def test_records_well_formed(spec_ids):
    """A sampled asset's records carry the expected EAV keys and a non-empty
    variable name — guards against a melt regression or a format switch."""
    sid = spec_ids[0]
    rows = load_raw_ndjson(sid)
    assert rows, f"{sid}: no rows to validate"
    sample = rows[: min(len(rows), 200)]
    for r in sample:
        assert _REQUIRED_KEYS <= set(r), f"{sid}: record missing keys: {r}"
        assert r["variable"], f"{sid}: empty variable name in {r}"
