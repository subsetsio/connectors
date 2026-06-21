"""Health-invariant tests for the Banco de Portugal connector.

Run post-DAG, in-connector. They load raw via the same loader the download node
used (gzipped NDJSON) and catch silent degradation: empty payloads, missing
fields, or a format switch upstream.
"""
from subsets_utils import load_raw_ndjson

_REQUIRED = {"series_id", "series_label", "reference_date", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset must yield at least one observation. An empty payload
    means pagination broke or the JSON-stat shape changed."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} datasets have 0 observations: {empty[:5]}"


def test_row_shape(spec_ids):
    """The first rows of each asset carry the expected keys and types."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = _REQUIRED - set(sample)
        assert not missing, f"{sid}: row missing keys {missing}"
        assert isinstance(sample["series_id"], int), f"{sid}: series_id not int"
        assert isinstance(sample["reference_date"], str) and len(
            sample["reference_date"]
        ) == 10, f"{sid}: reference_date not an ISO date"


def test_values_numeric(spec_ids):
    """Observations are numeric — a non-numeric value column means the
    JSON-stat value array was misread."""
    for sid in spec_ids[:25]:
        rows = load_raw_ndjson(sid)
        bad = [r for r in rows[:500] if not isinstance(r["value"], (int, float))]
        assert not bad, f"{sid}: {len(bad)} non-numeric values e.g. {bad[:2]}"
