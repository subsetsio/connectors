"""Health-invariant tests for the EPA Envirofacts connector.

Run post-DAG inside the connector. They read raw through the same loader the
download node wrote with (gzip-NDJSON) and catch silent degradation that file
existence alone misses — empty pulls, truncated/corrupt gzip, wrong shape.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every table pull should yield at least one record. An empty NDJSON
    usually means the endpoint changed format, the table path 404'd, or the
    pull was truncated before any page landed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 records"


def test_records_are_objects(spec_ids):
    """Each record must be a JSON object (dict). The Envirofacts JSON format is
    an array of row objects; anything else means the response shape drifted
    (e.g. an inline {'error': ...} envelope slipped through)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict), f"{sid}: first record is {type(first).__name__}, not an object"
        assert first, f"{sid}: first record is an empty object"
