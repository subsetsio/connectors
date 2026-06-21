"""Health invariants for uk-dft raw downloads.

These run post-DAG, in-connector, against the raw parquet each download node
wrote (all-VARCHAR). They catch silent degradation that file existence misses:
an empty/truncated download, a column set that shrank, a host quietly serving
an error page instead of the CSV.
"""

from subsets_utils import load_raw_parquet

# Minimum row counts — comfortably below observed sizes (road LA ~6.7k,
# nptg ~44k, naptan ~400k, STATS19 ~1.6M) but well above what a truncated or
# error-page download would yield.
_MIN_ROWS = {
    "uk-dft-gb-road-traffic-counts": 3000,
    "uk-dft-road-accidents-safety-data": 500000,
    "uk-dft-naptan": 100000,
    "uk-dft-nptg": 10000,
}

# A signature column that must survive in each asset's header.
_KEY_COLUMN = {
    "uk-dft-gb-road-traffic-counts": "local_authority_id",
    "uk-dft-road-accidents-safety-data": "collision_index",
    "uk-dft-naptan": "ATCOCode",
    "uk-dft-nptg": "NptgLocalityCode",
}


def test_raw_assets_nonempty_and_sized(spec_ids):
    """Every download asset holds at least its expected floor of rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, (
            f"{sid}: {len(table)} rows < expected floor {floor} "
            "(truncated download or error page?)"
        )


def test_key_columns_present(spec_ids):
    """The signature key column survives — guards against a silent header
    change / format switch."""
    for sid in spec_ids:
        col = _KEY_COLUMN.get(sid)
        if not col:
            continue
        names = load_raw_parquet(sid).column_names
        assert col in names, f"{sid}: key column {col!r} missing; got {names[:8]}..."
