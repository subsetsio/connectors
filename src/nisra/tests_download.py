"""Health-invariant tests for the NISRA connector raw assets.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: empty/truncated cube downloads and PxStat format drift.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every PxStat cube returns at least one data cell; an empty raw asset
    means a truncated or format-changed ReadDataset response."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty, e.g. {empty[:5]}"


def test_value_column_present(spec_ids):
    """PxStat CSV always carries STATISTIC and VALUE columns; their absence
    means the response format changed."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and ("VALUE" not in rows[0] or "STATISTIC" not in rows[0]):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets missing STATISTIC/VALUE, e.g. {bad[:5]}"
