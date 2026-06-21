"""Health invariants for the Mapping Police Violence raw download. Catch silent
degradation that file-existence alone misses: a truncated Airtable fetch, an
expired/blocked signed url that returns an error stub, or a schema rename that
nulls the columns the transform depends on."""

from subsets_utils import load_raw_ndjson

# Verified full-corpus shape (2026-06): ~15.9k rows, 62 columns. Floor set well
# below current to allow normal weekly growth, tight enough that a truncated or
# empty pull trips it.
_MIN_ROWS = 14000
_EXPECTED_KEYS = {
    "name", "age", "gender", "race", "date", "city", "state", "county",
    "agency_responsible", "cause_of_death", "mpv_id", "latitude", "longitude",
}


def test_raw_nonempty(spec_ids):
    """The single download spec must have written rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_row_count_plausible(spec_ids):
    """A count far below floor means the Airtable fetch was truncated or the
    signed readSharedViewData url silently degraded."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= _MIN_ROWS, f"{sid}: got {len(rows)} rows, expected >= {_MIN_ROWS}"


def test_expected_columns_present(spec_ids):
    """Guard against an upstream column rename silently nulling the fields the
    transform selects and the platform joins on."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        missing = _EXPECTED_KEYS - keys
        assert not missing, f"{sid}: raw rows missing expected columns {sorted(missing)}"


def test_select_labels_resolved(spec_ids):
    """select/multiSelect cells must be resolved to human labels, not raw Airtable
    choice ids (sel...). If we see a 'sel<17 hex>' value in race, the choice-map
    join broke and the published data would be unreadable."""
    import re
    choice_id = re.compile(r"^sel[0-9A-Za-z]{14}$")
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        bad = [r.get("race") for r in rows[:2000]
               if isinstance(r.get("race"), str) and choice_id.match(r["race"])]
        assert not bad, f"{sid}: {len(bad)} 'race' values are unresolved choice ids"
