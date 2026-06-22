"""Health-invariant tests for the Connecticut DOL connector raw assets.

Run post-DAG in-connector. They load raw via the same loader the download node
used (NDJSON) and catch silent degradation that file-existence misses:
empty payloads, truncated pulls, format switches.
"""
from subsets_utils import load_raw_ndjson

# Floors well below probed counts (12499 / 325 / 3829 / 908 / 52092), loose
# enough for normal growth but tight enough that a truncated pull trips them.
_MIN_ROWS = {
    "connecticut-department-of-labor-8zbs-9atu": 8000,
    "connecticut-department-of-labor-h44w-mqs3": 100,
    "connecticut-department-of-labor-tids-7w95": 1000,
    "connecticut-department-of-labor-nfe2-aprv": 200,
    "connecticut-department-of-labor-7zu6-8dcr": 20000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows; empty usually means the
    endpoint switched format, paged out, or returned an error envelope."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_raw_row_counts_meet_floor(spec_ids):
    """Catch truncated pulls (e.g. pagination stopping after page 1)."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"


def test_rows_are_dicts(spec_ids):
    """Socrata JSON rows are objects; a list of scalars/strings means the
    response shape changed (or we saved the wrong thing)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert isinstance(rows[0], dict) and rows[0], f"{sid}: first row is not a non-empty dict"
