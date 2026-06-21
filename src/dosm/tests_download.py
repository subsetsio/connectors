"""Health-invariant tests for the DOSM connector.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: an endpoint that started returning an empty/HTML body,
a parquet that decoded to zero rows, a column-less table.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's raw parquet must hold at least one row. A 0-row table
    means the source file vanished, returned an error page, or the schema
    drifted to something unreadable."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_all_raw_assets_have_columns(spec_ids):
    """Each table must expose at least one column — guards against a download
    that wrote an empty schema (truncated/garbage payload that still parsed)."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets have no columns: {bad[:10]}"
