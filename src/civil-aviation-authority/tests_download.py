"""Health-invariant tests for the civil-aviation-authority connector.

Run post-DAG inside the connector, seeing raw data through subsets_utils loaders.
Catches silent degradation that file-existence misses: empty payloads, lost
period tagging, format switches.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every table should have rows across its annual releases. Zero rows means
    discovery matched no CSV (label format changed) or the CSV came back empty."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_period_and_family_tagged(spec_ids):
    """Every row must carry the injected release_period + family tags; missing
    them means the tagging step was bypassed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        bad = [i for i, r in enumerate(rows[:50]) if not r.get("release_period") or not r.get("family")]
        assert not bad, f"{sid}: rows missing release_period/family (first checked: {bad[:3]})"


def test_multiple_years_present(spec_ids):
    """A table that publishes annually should span more than one release year; a
    single year usually means discovery stopped after the latest annual page."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        years = {r.get("release_period") for r in rows}
        assert len(years) >= 2, f"{sid}: only {len(years)} release year(s) found: {years}"
