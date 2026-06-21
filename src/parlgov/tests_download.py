"""Health invariants for ParlGov raw downloads (NDJSON per table)."""

from subsets_utils import load_raw_ndjson

# Minimum row counts per table observed during probing (2026-06); a large drop
# means a truncated download or a silently changed endpoint.
_MIN_ROWS = {
    "parlgov-data-cabinet": 1400,
    "parlgov-data-cabinet-party": 3500,
    "parlgov-data-country": 30,
    "parlgov-data-election": 900,
    "parlgov-data-election-result": 8500,
    "parlgov-data-party": 1500,
    "parlgov-view-cabinet": 3500,
    "parlgov-view-election": 8500,
    "parlgov-view-party": 1500,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's NDJSON asset must hold rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Row counts must be in the expected ballpark — guards against truncation."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows, expected >= {floor}"


def test_key_columns_present(spec_ids):
    """Each table must carry an 'id' column — the natural key the transforms cast."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert "id" in rows[0], f"{sid}: missing 'id' column; got {list(rows[0])}"
