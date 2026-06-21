"""Health-invariant tests — run post-DAG, in-connector.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated pulls, or a key column vanishing because the endpoint changed shape.
"""

from subsets_utils import load_raw_ndjson

# The stable row-identity column each entity set carries. If it disappears or
# goes null, the OData schema changed under us.
KEY_COL = {
    "global-fund-grants": "id",
    "global-fund-allfinancialindicators": "financialIndicatorId",
    "global-fund-allprogrammaticindicators": "programmaticIndicatorId",
    "global-fund-eligibility": "eligibilityId",
    "global-fund-fundingrequests": "id",
}


def test_raw_assets_nonempty_with_key(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"
        col = KEY_COL.get(sid)
        if not col:
            continue
        sample = rows[:1000]
        assert col in sample[0], f"{sid}: key column {col!r} missing from records"
        missing = sum(1 for r in sample if not r.get(col))
        assert missing == 0, f"{sid}: {missing}/{len(sample)} sampled rows null in key {col!r}"
