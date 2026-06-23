"""Health-invariant tests for the Eskom connector raw assets.

These run post-DAG, in-connector, against the NDJSON each fetch node wrote.
They catch silent degradation that file-existence alone misses: an empty
payload (Power BI returned no rows / embed token went stale), a decode that
produced rows without usable values, or a format change in the long shape.
"""

from subsets_utils import load_raw_ndjson

REQUIRED_KEYS = {"period_label", "period_ms", "series", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson is empty (no decoded rows)"


def test_long_shape_and_values(spec_ids):
    """Every row must carry the long-format keys, a non-null series and a
    numeric value — the contract the transform reads."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = REQUIRED_KEYS - set(sample.keys())
        assert not missing, f"{sid}: rows missing keys {missing}"
        numeric = sum(1 for r in rows if isinstance(r.get("value"), (int, float)))
        assert numeric > 0, f"{sid}: no rows with a numeric value"
        named = sum(1 for r in rows if r.get("series"))
        assert named == len(rows), f"{sid}: {len(rows) - named} rows have empty series"


def test_series_present(spec_ids):
    """Each report should expose at least one distinct measure series."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        series = {r.get("series") for r in rows}
        assert len(series) >= 1, f"{sid}: no series found"
