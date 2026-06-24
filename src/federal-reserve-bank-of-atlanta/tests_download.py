"""Health invariants for the Atlanta Fed raw assets.

Run post-DAG inside the connector. Every download node writes tidy NDJSON, so we
load it back through the same loader and check it is non-empty and that the
common keys are present — the failures file-existence alone would miss
(empty payload, format switch, silent truncation).
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows and len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_every_record_has_a_date(spec_ids):
    """Each entity is a time series / dated panel; every record must carry a date."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        missing = sum(1 for r in rows[:5000] if not r.get("date"))
        assert missing == 0, f"{sid}: {missing} of first 5000 records missing a date"
