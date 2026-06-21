"""Health invariants for the IDMC raw downloads. Catch silent degradation that
file-existence alone misses: a feed truncated to page 1, auth quietly switched to
a 403 stub, or an endpoint that changed format and now yields zero usable rows."""
from subsets_utils import load_raw_ndjson

# Verified full-corpus counts (2026-06). Floors set well below current to allow
# normal growth/shrink, but tight enough that a truncated/empty pull trips them.
_MIN_ROWS = {
    "idmc-conflicts": 800,
    "idmc-disasters": 20000,
    "idmc-displacements": 1800,
    "idmc-idu": 40000,
    "idmc-disaggregations": 35000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must have written rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Each feed should be in the expected order of magnitude; a count far below
    floor means pagination broke or the feed silently degraded."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: got {len(rows)} rows, expected >= {floor}"


def test_keys_present(spec_ids):
    """Spot-check that the expected identifying columns survived the fetch — guards
    against an upstream rename silently nulling the join keys downstream relies on."""
    expected = {
        "idmc-conflicts": {"iso3", "year", "new_displacement"},
        "idmc-disasters": {"iso3", "year", "event_name", "hazard_type_name"},
        "idmc-displacements": {"iso3", "year", "conflict_new_displacement"},
        "idmc-idu": {"id", "iso3", "figure", "displacement_date"},
        "idmc-disaggregations": {"id", "iso3", "year", "reported_figures"},
    }
    for sid in spec_ids:
        keys = expected.get(sid)
        if not keys:
            continue
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = keys - set(sample.keys())
        assert not missing, f"{sid}: sample row missing expected keys {sorted(missing)}"
