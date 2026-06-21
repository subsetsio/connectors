"""Health invariants for the Bank Negara Malaysia connector raw assets.

Run post-DAG, in-connector. Catch silent degradation the file-exists check
misses: empty payloads, the Accept header silently breaking (would yield 0
rows), or a resource collapsing to a single record.
"""
from subsets_utils import load_raw_ndjson

# Daily time series go back ~2007, so they should hold thousands of rows.
# Snapshots are intentionally small (current bank rates / one stale RMB record).
_SNAPSHOTS = {
    "bank-negara-malaysia-base-rate": 5,            # one row per retail bank
    "bank-negara-malaysia-renminbi-fx-forward-price": 1,
}
_MIN_TIMESERIES_ROWS = 500


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_reasonable(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _SNAPSHOTS.get(sid, _MIN_TIMESERIES_ROWS)
        assert len(rows) >= floor, (
            f"{sid}: only {len(rows)} rows, expected >= {floor} "
            f"(history fetch likely truncated)"
        )


def test_rows_have_date_or_bank(spec_ids):
    """Every time-series row must carry a date; base-rate carries a bank_code.
    A wholesale loss of the key field means the response shape changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert ("date" in sample) or ("bank_code" in sample), (
            f"{sid}: rows lack both 'date' and 'bank_code' keys: {list(sample)[:6]}"
        )
