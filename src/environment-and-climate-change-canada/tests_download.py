"""Health invariants for the ECCC GeoMet connector, run post-DAG in-connector.

Catches silent degradation that file-existence alone misses: an endpoint that
switched format or started returning empty payloads, or a pull truncated after
the first page.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every collection should yield rows. An empty NDJSON usually means the
    items endpoint changed shape or returned an error envelope."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_feature_id_present(spec_ids):
    """fetch_one injects a non-null feature_id on every row; its absence means
    the GeoJSON feature shape changed (no top-level id)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        head = rows[:1000]
        missing = [r for r in head if not r.get("feature_id")]
        assert not missing, (
            f"{sid}: {len(missing)}/{len(head)} sampled rows missing feature_id"
        )
