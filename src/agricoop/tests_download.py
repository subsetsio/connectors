"""Health-invariant tests for agricoop, run post-DAG inside the connector.

Each download node writes one data.gov.in resource's records as NDJSON. The
dominant silent failure is the resource endpoint returning an empty/error payload
that still parses (the sample key's 10-row cap, a 429 swallowed, a resource
withdrawn), so the core invariants are: every raw asset holds rows, rows are flat
objects, and each resource carries the columns we built its transform around.
"""

from subsets_utils import load_raw_ndjson

# A signature column we expect on every row of each resource — if it's gone, the
# resource's schema changed under us and the transform is publishing the wrong thing.
_SIGNATURE_COL = {
    "agricoop-district-wise-season-wise-crop-production-statistics-from-19-c33a2e6b": "crop",
    "agricoop-current-daily-price-of-various-commodities-from-various-mark-1abe392e": "commodity",
    "agricoop-classified-area-under-land-use-statistics-lus-3db3addf": "class_name",
    "agricoop-source-wise-irrigated-area-under-land-use-statistics-lus-3c17d7f6": "irrigationsource",
    "agricoop-state-wise-number-and-area-of-operational-holdings-for-sched-2273cec3": "state__ut",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every built resource should hold rows. An empty raw asset means the
    /resource endpoint returned nothing — the page cap silently truncated to 0,
    auth lapsed, or the resource was withdrawn."""
    empty = [sid for sid in spec_ids if not load_raw_ndjson(sid)]
    assert not empty, f"{len(empty)} raw asset(s) empty: {empty}"


def test_records_are_dict_rows(spec_ids):
    """Each record must be a flat object (the resource's row). Scalars/strings
    here mean the parser or response format regressed."""
    bad = [sid for sid in spec_ids if (r := load_raw_ndjson(sid)) and not isinstance(r[0], dict)]
    assert not bad, f"raw rows are not dict objects: {bad}"


def test_signature_column_present(spec_ids):
    """Each resource must carry the column its transform keys on. A missing
    signature column = the resource's schema drifted and our SELECT would fail or
    publish nulls."""
    missing = []
    for sid in spec_ids:
        col = _SIGNATURE_COL.get(sid)
        rows = load_raw_ndjson(sid)
        if col and rows and col not in rows[0]:
            missing.append((sid, col))
    assert not missing, f"signature column missing from raw rows: {missing}"
