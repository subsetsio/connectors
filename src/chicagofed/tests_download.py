"""Health-invariant tests for the Chicago Fed connector.

Run post-DAG inside the connector. They load raw assets through the same
subsets_utils loader the download node used (save_raw_ndjson -> load_raw_ndjson)
and catch silent degradation that file-existence alone misses.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw long-form asset must hold rows. An empty
    payload means the CSV endpoint changed format, moved, or returned an
    error page instead of data."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"raw assets with 0 rows: {empty}"


def test_long_schema_shape(spec_ids):
    """Each row must carry the uniform long-format keys with a numeric-parseable
    value. A drift here means the melt parser silently emitted the wrong shape."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(50, len(rows))]
        for r in sample:
            assert set(r.keys()) >= {"period", "series", "value"}, (
                f"{sid}: row missing long-format keys: {r}"
            )
            assert r["period"], f"{sid}: empty period in {r}"
            assert r["series"], f"{sid}: empty series in {r}"
            float(r["value"])  # raises if value is not numeric text
