"""Health invariants for india-ministry-of-commerce raw assets.

Catalog connector: every download node pulls one data.gov.in resource as NDJSON.
Schemas differ per resource, so the universal invariant we can assert is that the
pull is non-empty — an empty payload means the endpoint switched format, the key
got throttled into an empty body, or the resource was depublished.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson is empty"


def test_records_are_dicts(spec_ids):
    """Each resource record must be a flat object (keyed by field id). A list or
    scalar here means the response envelope changed and `records` no longer holds
    row dicts."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict) and first, f"{sid}: record 0 is not a non-empty dict"
