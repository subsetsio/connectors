"""Health invariants for UNODC raw downloads.

Each spec writes one collection's workbook parsed to NDJSON rows. These catch
silent degradation that file-existence alone misses: an empty/stub workbook
(the `reset_dimensions` bug yields zero rows), a wrong sheet, or a column rename
that drops the value field.
"""
from subsets_utils import load_raw_ndjson

# A small collection (wildlife) is the only one with under a few thousand rows.
_MIN_ROWS = 50


def test_all_raw_assets_nonempty(spec_ids):
    """Every collection should parse to a healthy number of rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= _MIN_ROWS, f"{sid}: only {len(rows)} rows parsed"


def test_value_column_present(spec_ids):
    """Every row must carry a 'value' field (glotip's txtVALUE is normalized to
    'value'); its absence means the header row was misdetected."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(len(rows), 1000)]
        assert all("value" in r for r in sample), f"{sid}: rows missing 'value' key"
        assert any(r.get("value") not in (None, "") for r in sample), (
            f"{sid}: no non-null values in first {len(sample)} rows"
        )
