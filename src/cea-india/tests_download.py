"""Health invariants for CEA India raw downloads.

Each spec's raw asset is line-delimited JSON (one row per record). A silently
emptied or truncated endpoint is the failure mode these guard against.
"""

from subsets_utils import load_raw_ndjson

# Loose per-asset row floors: large enough to catch a truncated/empty payload,
# slack enough for normal growth. Endpoints not listed just need to be nonempty.
_MIN_ROWS = {
    "cea-india-installed-capacity-statewise": 1000,
    "cea-india-psp-energy": 1000,
    "cea-india-psp-peak": 1000,
    "cea-india-renewable-energy": 500,
    "cea-india-transmission-lines": 500,
    "cea-india-transformation-substations": 500,
    "cea-india-percapitalconsumtion": 300,
}


def test_expected_spec_count(spec_ids):
    """One download per published CEA endpoint; a different count means the
    spec set drifted from the entity union."""
    assert len(spec_ids) == 11, f"expected 11 download specs, got {len(spec_ids)}"


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint must return rows. Empty payloads usually mean the
    endpoint moved, changed format, or started erroring with a 200 body."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"
        floor = _MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, (
            f"{sid}: only {len(rows)} rows (< {floor}); likely truncated"
        )


def test_rows_are_objects(spec_ids):
    """Each record must be a JSON object — a flattening regression that left
    raw nested would surface here."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert isinstance(rows[0], dict), f"{sid}: first record is not an object"
