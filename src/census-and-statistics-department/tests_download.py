"""Health-invariant tests for the C&SD connector, run post-DAG in-connector.

Catches silent degradation that file-existence alone misses: empty payloads,
a table that returned only blank observations, or a fetch that wrote rows
without the stat_var tag the transform relies on.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every web table's raw ndjson should hold rows. An empty payload means the
    MDT endpoint switched format or the table was silently dropped."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_rows_tagged_and_have_observations(spec_ids):
    """Each row must carry a stat_var tag (the transform/labelling depends on it)
    and each table must contain at least one non-null observation."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        head = rows[:2000]
        assert all(r.get("stat_var") for r in head), f"{sid}: rows missing stat_var"
        assert any(r.get("obs_value") is not None for r in head), (
            f"{sid}: no non-null obs_value in first {len(head)} rows"
        )
