"""Health-invariant tests for the NIFC connector's raw downloads.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses — a layer that started returning an empty/error payload, or
pagination that stopped after page one.
"""
from subsets_utils import list_raw_files, load_raw_ndjson

# The smallest layer (~3.2k rows) — safe to fully load in a test.
_RAWS = "nifc-29185087b4594a35abe059cbdbf97ee4-1"


def test_every_spec_wrote_raw(spec_ids):
    """Each download spec must have produced a raw NDJSON file."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"


def test_raws_nonempty_and_shaped():
    """RAWS layer should hold thousands of station records with expected keys;
    a tiny count or missing keys means the endpoint changed or auth broke."""
    rows = load_raw_ndjson(_RAWS)
    assert len(rows) >= 1000, f"RAWS has only {len(rows)} rows; expected >=1000"
    sample = rows[0]
    for key in ("StationName", "Latitude", "Longitude", "State"):
        assert key in sample, f"RAWS record missing expected field {key!r}"
