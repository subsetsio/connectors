"""Health-invariant tests for the CMS connector.

Each download node writes per-dataset NDJSON (one JSON object per row). These
catch the silent-degradation failures that file existence alone misses: an
endpoint that started returning an empty body, an envelope instead of rows, or
a format switch that leaves the raw asset unparseable.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's raw asset must hold at least one row. An empty payload
    usually means the data-api/datastore changed shape or the dataset rotated."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw asset(s) empty: {empty[:10]}"


def test_rows_are_objects(spec_ids):
    """Rows must be JSON objects (dicts) with at least one column — guards
    against a scalar/array body sneaking through as 'data'."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        if not isinstance(first, dict) or not first:
            bad.append(sid)
    assert not bad, f"{len(bad)} asset(s) whose first row is not a non-empty object: {bad[:10]}"
