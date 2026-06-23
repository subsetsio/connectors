"""Health-invariant tests for the FCA connector raw assets.

Each download node parses a bespoke FCA XLSX workbook into a tidy long-format
NDJSON. These tests catch silent degradation a file-existence check misses:
an endpoint switching format, a workbook layout change that empties the melt,
or a truncated download.
"""
from subsets_utils import load_raw_ndjson

EXPECTED_KEYS = {
    "fca-firm-complaints": {"semester", "breakdown_type", "volume"},
    "fca-general-insurance-value-measures": {"firm_name", "product_category", "year"},
    "fca-mortgage-lending-statistics": {"metric", "year", "quarter", "value"},
    "fca-product-sales": {"category", "period", "no_of_sales"},
    "fca-retail-intermediary-market": {"section", "year", "metric", "value"},
    "fca-retirement-income-market": {"table_title", "row_label", "period", "value"},
}

# Loose floors per asset — well below the volumes observed while probing, but
# high enough that a layout change collapsing the melt to a handful of rows trips.
MIN_ROWS = {
    "fca-firm-complaints": 500,
    "fca-general-insurance-value-measures": 200,
    "fca-mortgage-lending-statistics": 5000,
    "fca-product-sales": 200,
    "fca-retail-intermediary-market": 50,
    "fca-retirement-income-market": 500,
}


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_raw_assets_have_expected_keys(spec_ids):
    for sid in spec_ids:
        expected = EXPECTED_KEYS.get(sid)
        if not expected:
            continue
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        missing = expected - keys
        assert not missing, f"{sid}: raw rows missing keys {missing}; got {sorted(keys)}"


def test_raw_assets_meet_row_floor(spec_ids):
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < floor {floor} (melt likely degraded)"
