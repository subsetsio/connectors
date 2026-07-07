"""Post-download health checks for Statistics Sweden raw assets."""
from subsets_utils import load_raw_ndjson

REQUIRED_KEYS = {"table_id", "period", "period_start", "value"}


def _download_ids(spec_ids):
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has zero rows"


def test_required_keys_present(spec_ids):
    for sid in _download_ids(spec_ids):
        row = load_raw_ndjson(sid)[0]
        missing = REQUIRED_KEYS - set(row)
        assert not missing, f"{sid}: row missing keys {sorted(missing)}"


def test_table_id_matches_asset(spec_ids):
    for sid in _download_ids(spec_ids):
        expected = sid.removeprefix("statistics-sweden-").upper()
        rows = load_raw_ndjson(sid)
        actual = {row.get("table_id") for row in rows[:100]}
        assert actual == {expected}, f"{sid}: expected {expected}, got {actual}"
