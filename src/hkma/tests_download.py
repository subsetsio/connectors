"""Health-invariant tests for the HKMA connector.

Run post-DAG, in-connector. They load raw through the same NDJSON loader the
download node wrote with, so they behave identically locally and in the cloud.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint should return records. An empty payload means the path
    changed, a required param was dropped, or the envelope format shifted."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} assets have 0 rows: {empty[:10]}"


def test_records_are_dicts(spec_ids):
    """Records must be flat JSON objects (the API's `result.records`), not
    stray scalars — a sign the envelope was mis-parsed."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not isinstance(rows[0], dict):
            bad.append(sid)
    assert not bad, f"non-dict records in: {bad[:10]}"


def test_segment_column_present(spec_ids):
    """Endpoints fetched across multiple `segment` values must carry the
    `segment` column on every row, with more than one distinct value — proof
    the multi-segment fetch ran rather than silently fetching one slice."""
    segmented = {
        "hkma-efbn-closing", "hkma-efbn-indicative-price",
        "hkma-efbn-tender-results-efb", "hkma-efbn-tender-results-efn",
        "hkma-govbond-price-yield-daily", "hkma-govbond-price-yield-endperiod",
        "hkma-govbond-price-yield-periodaverage", "hkma-govbond-tender-results",
        "hkma-register-svf-licensees",
    }
    for sid in segmented & set(spec_ids):
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: no rows"
        segs = {r.get("segment") for r in rows}
        assert None not in segs, f"{sid}: rows missing segment column"
        assert len(segs) >= 2, f"{sid}: only segment(s) {segs} fetched"
