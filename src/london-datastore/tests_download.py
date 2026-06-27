"""Health-invariant tests for the London Datastore connector.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: an endpoint that started returning an HTML error page
instead of a CSV, an auth wall, a truncated download — all of which surface as
an empty or column-less raw asset.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's CSV should yield at least one data row. An empty asset
    means the resource URL stopped serving real CSV (HTML error, redirect to a
    login, or a header-only file)."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_all_raw_assets_have_columns(spec_ids):
    """Each parquet asset should have at least one column — guards against a
    parser regression that drops the header."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have no columns: {bad[:10]}"
