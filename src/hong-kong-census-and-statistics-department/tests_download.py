"""Health invariants for the HK C&SD web-table raw assets.

Raw is NDJSON (heterogeneous columns across tables). Every asset must hold rows
and every row must carry the normalized stat_var / value keys — empty payloads or
missing keys mean the comp.json shape changed or every MDT CSV 400'd silently.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows, e.g. {empty[:5]}"


def test_rows_have_normalized_keys(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        sample = rows[0]
        for key in ("stat_var", "stat_pres", "value"):
            assert key in sample, f"{sid}: row missing normalized key '{key}': {sample}"


def test_some_values_present(spec_ids):
    """A table whose every value is null usually means obs_value parsing broke."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        assert any(r.get("value") is not None for r in rows), \
            f"{sid}: all {len(rows)} rows have null value"
