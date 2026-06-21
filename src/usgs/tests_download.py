"""Post-DAG health invariants for the USGS raw assets.

Each download spec streams one gzipped NDJSON asset named after the spec id;
load_raw_ndjson auto-detects the .gz suffix. These tests catch silent
degradation that file existence alone misses — empty payloads, a collection
that started returning an error envelope, or a format switch."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty NDJSON asset."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 records"


def test_records_are_objects(spec_ids):
    """Each record must be a JSON object (dict) — a list/scalar means the
    parse or the source shape is wrong."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        head = rows[0]
        assert isinstance(head, dict), f"{sid}: first record is {type(head).__name__}, not object"
        assert head, f"{sid}: first record is an empty object"


def test_earthquakes_have_core_fields(spec_ids):
    """The earthquakes catalog must carry its identifying columns — guards
    against the FDSN CSV header changing or a truncated download."""
    if "usgs-earthquakes" not in spec_ids:
        return
    rows = load_raw_ndjson("usgs-earthquakes")
    for key in ("id", "time", "mag", "latitude", "longitude"):
        assert key in rows[0], f"usgs-earthquakes: missing column {key!r}"
