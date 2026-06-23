from subsets_utils import load_raw_ndjson

# Approximate row counts per resource (2024 Lok Sabha). The successful-candidate
# table is one row per declared seat (~543); the others are state/UT or
# constituency breakdowns. A wildly different count means pagination broke or
# the endpoint changed shape.
_EXPECTED_MIN = {
    "election-commission-of-india-0bd877c0-031d-49da-a743-d102dec6e7b7": 25,
    "election-commission-of-india-194d454f-3ea8-4621-a915-b211c66e46a7": 500,
    "election-commission-of-india-1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd": 25,
    "election-commission-of-india-a27ba4e9-73c2-40d1-90b2-41d71ea7c283": 5,
    "election-commission-of-india-f7f1bf09-7633-4474-96b2-62630c70f33c": 25,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw NDJSON should hold rows. Empty payloads usually mean the
    endpoint switched format or the api-key was rejected silently."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Pagination must walk the full table — a stop after page 1 (the demo key
    caps at 10 records/page) would leave these well under their known sizes."""
    for sid in spec_ids:
        floor = _EXPECTED_MIN.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: got {len(rows)} rows; expected >= {floor}"
