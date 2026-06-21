"""Health-invariant tests for the Central Statistical Bureau (Latvia) connector.

Run post-DAG, in-connector. Raw is written as gzip NDJSON (one row per non-null
PxWeb observation), so we read it back with load_raw_ndjson.
"""

from subsets_utils import load_raw_ndjson


def test_raw_assets_mostly_nonempty(spec_ids):
    """Each spec's raw asset should hold observation rows. A handful of tables
    can legitimately be all-null (→ 0 rows), but a large fraction of empties
    means the json-stat2 parse, the query plan, or auth degraded silently."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    frac = len(empty) / max(1, len(spec_ids))
    assert frac <= 0.05, (
        f"{len(empty)}/{len(spec_ids)} raw assets are empty ({frac:.0%}); "
        f"expected <=5%. First few: {empty[:10]}"
    )


def test_obs_value_present_and_numeric(spec_ids):
    """Every non-empty raw asset must carry a numeric obs_value on its rows —
    the column the transform publishes. Its absence means the parser changed
    shape or the response format flipped away from json-stat2."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        row = rows[0]
        if "obs_value" not in row or not isinstance(row["obs_value"], (int, float)):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets missing numeric obs_value; first few: {bad[:10]}"
