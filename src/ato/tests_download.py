"""Health-invariant tests for the ATO connector, run post-DAG in-connector.

These catch silent degradation that file-existence misses: empty/truncated
datastore pulls, and the income_year tag being lost during the per-year union.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every entity is a datastore-backed ATO table — a 0-row raw asset means
    the datastore resource id changed or the dump silently truncated."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_income_year_tag_present(spec_ids):
    """Every row carries the income_year key (its value may be null for
    non-yearly single-edition tables). A missing key means the union step
    dropped the tag."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and "income_year" not in rows[0]:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets missing income_year key: {bad[:10]}"
