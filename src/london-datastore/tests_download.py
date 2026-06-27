"""Health-invariant tests for the London Datastore connector.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: an endpoint that started returning an HTML error page
instead of a CSV, an auth wall, a truncated download — all of which surface as
an empty raw asset.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's CSV should yield at least one data row. An empty asset
    means the resource URL stopped serving real CSV (HTML error, redirect to a
    login, or a header-only file)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_rows_are_objects(spec_ids):
    """Each NDJSON record should be a dict with at least one column — guards
    against a parser regression that emits scalars or empty objects."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and (not isinstance(rows[0], dict) or len(rows[0]) == 0):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have malformed rows: {bad[:10]}"
