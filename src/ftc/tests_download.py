from subsets_utils import load_raw_ndjson

# Minimum row counts we observed during probing; a large drop signals a
# truncated download or a format/endpoint change.
_MIN_ROWS = {
    "ftc-hsr-merger-transactions-by-month": 300,
    "ftc-hsr-transactions-filings-second-requests-by-fy": 25,
    "ftc-ftc-merger-enforcement-actions": 300,
    "ftc-ftc-nonmerger-enforcement-actions": 100,
    "ftc-ftc-civil-penalty-actions": 30,
    "ftc-dnc-reported-call-numbers": 5000,
}

# A representative column that must survive parsing for each asset.
_REQUIRED_COL = {
    "ftc-hsr-merger-transactions-by-month": "TransactionReceived",
    "ftc-hsr-transactions-filings-second-requests-by-fy": "FY",
    "ftc-ftc-merger-enforcement-actions": "MatterName",
    "ftc-ftc-nonmerger-enforcement-actions": "MatterName",
    "ftc-ftc-civil-penalty-actions": "MatterName",
    "ftc-dnc-reported-call-numbers": "Company_Phone_Number",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty payloads usually mean
    the landing page layout changed or the file moved."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_reasonable(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"


def test_required_columns_present(spec_ids):
    for sid in spec_ids:
        col = _REQUIRED_COL.get(sid)
        if col is None:
            continue
        rows = load_raw_ndjson(sid)
        assert col in rows[0], f"{sid}: required column {col!r} missing from raw rows"
