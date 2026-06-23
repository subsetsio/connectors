"""Health-invariant tests for the HKMA connector raw assets.

Runs post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used. Catches silent degradation (empty payloads, format switch, auth
expiry) that file-existence checks miss.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint we pull should return at least one record. An empty
    payload means the endpoint changed shape, started requiring a new param,
    or silently failed."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_records_are_objects(spec_ids):
    """Each record must be a JSON object (dict) so the SQL transform can read
    it as a row. A list-of-scalars or string payload means the envelope parse
    went wrong."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not isinstance(rows[0], dict):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have non-object records: {bad[:10]}"
