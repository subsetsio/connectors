"""Health invariants for the IPU Parline raw assets."""

from subsets_utils import load_raw_ndjson

# Minimum expected row counts (well below observed, to catch silent truncation
# without being brittle to normal source growth).
_MIN_ROWS = {
    "inter-parliamentary-union-countries": 150,
    "inter-parliamentary-union-parliaments": 150,
    "inter-parliamentary-union-chambers": 200,
    "inter-parliamentary-union-elections": 2000,
    "inter-parliamentary-union-specialized-bodies": 800,
    "inter-parliamentary-union-political-parties": 2000,
    "inter-parliamentary-union-people": 3000,
    "inter-parliamentary-union-report-women-ranking": 150,
    "inter-parliamentary-union-report-age-brackets": 200,
    "inter-parliamentary-union-report-speakers": 200,
    "inter-parliamentary-union-report-secretaries-general": 200,
    "inter-parliamentary-union-report-women-speakers": 30,
    "inter-parliamentary-union-report-elections": 200,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_plausible(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: only {len(rows)} rows (<{floor}); pagination likely broke"


def test_primary_keys_populated(spec_ids):
    """Each asset's first column (its code/pk) must be non-null on most rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        pk = next(iter(rows[0].keys()))
        nonnull = sum(1 for r in rows if r.get(pk) not in (None, ""))
        assert nonnull >= 0.9 * len(rows), f"{sid}: pk {pk!r} null on >10% of rows"
