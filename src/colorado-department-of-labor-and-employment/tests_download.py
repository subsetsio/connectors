"""Health-invariant tests run post-DAG, in-connector, after the download nodes.

Catch silent degradation that file existence alone misses: empty payloads,
truncated pulls, or the Socrata endpoint quietly switching format/auth.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every CDLE table holds rows. An empty NDJSON usually means the SODA
    endpoint changed format or started rejecting the request."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_rows_are_dicts_with_fields(spec_ids):
    """Each row is a JSON object with at least a few columns — guards against a
    degraded response that returns bare strings or single-key error envelopes."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict), f"{sid}: first row is not a dict: {type(first)}"
        assert len(first) >= 3, f"{sid}: first row has only {len(first)} fields"
