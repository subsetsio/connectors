"""Health-invariant tests for data-gov-in, run post-DAG inside the connector.

Each download node writes its resource's records as NDJSON. The dominant silent
failure for this source is an endpoint returning an empty/error payload that still
parses (auth lapse, resource pulled, format switch), so the core invariant is:
every spec's raw asset holds rows.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every resource we publish should hold at least one record. An empty raw
    asset means the /resource endpoint returned no records — auth expired, the
    resource was withdrawn, or the response format changed silently."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw asset(s) are empty, e.g. {empty[:5]}"


def test_records_are_dict_rows(spec_ids):
    """Each record must be a flat object (the resource's row). If the parser
    started yielding scalars/strings the downstream SELECT * would publish
    garbage; sample a few assets to catch a format regression cheaply."""
    bad = []
    for sid in spec_ids[:50]:
        rows = load_raw_ndjson(sid)
        if rows and not isinstance(rows[0], dict):
            bad.append(sid)
    assert not bad, f"raw rows are not dict objects, e.g. {bad[:5]}"
