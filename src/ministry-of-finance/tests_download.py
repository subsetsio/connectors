"""Health-invariant tests for the Ministry of Finance (India) connector.

Run post-DAG inside the connector. They load raw the same way the download node
saved it (NDJSON) and assert the pulls are non-empty and carry the resource_id
stamp — catching silent degradation (empty payloads, auth/UA stalls returning
nothing, format switches) that file existence alone misses.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every resource is a real published government table, so each raw NDJSON
    asset must hold at least one row. Zero rows means the resource endpoint
    returned nothing (auth/UA stall, or the resource id went away)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty, e.g. {empty[:5]}"


def test_resource_id_stamped(spec_ids):
    """fetch_one stamps resource_id on every row; if it is missing the row
    shape changed under us."""
    missing = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and "resource_id" not in rows[0]:
            missing.append(sid)
    assert not missing, f"{len(missing)} assets lack resource_id, e.g. {missing[:5]}"
