"""Health-invariant tests for the KBA Statistikportal raw assets.

Each download node writes one NDJSON asset (full attribute table of one ArcGIS
FeatureServer layer). These catch silent degradation a file-exists check misses:
empty payloads, or a query that returned only the ArcGIS envelope with no rows.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every Statistikportal layer holds rows; an empty NDJSON means the /query
    endpoint changed shape or returned an error envelope we swallowed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_rows_are_attribute_dicts(spec_ids):
    """Rows should be flat attribute dicts (we unwrap features[].attributes).
    A list of {'attributes': ...} envelopes means the unwrap regressed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict), f"{sid}: row 0 is {type(first)}, expected dict"
        assert "attributes" not in first, f"{sid}: rows still wrapped in 'attributes' envelope"
