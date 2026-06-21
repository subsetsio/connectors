"""Health invariants for the Redfin raw downloads.

Each level's raw parquet must hold rows, carry the kept source columns, and
contain only its own geography level — a wrong/empty payload usually means the
S3 key moved or the TSV schema changed.
"""

from subsets_utils import load_raw_parquet

# loose per-level lower bounds on raw row counts (full file, all property types)
MIN_ROWS = {
    "redfin-market-tracker-national": 1_000,
    "redfin-market-tracker-state": 30_000,
    "redfin-market-tracker-metro": 500_000,
    "redfin-market-tracker-county": 2_000_000,
    "redfin-market-tracker-city": 5_000_000,
    "redfin-market-tracker-zip": 5_000_000,
}


def test_raw_nonempty_and_min_rows(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} raw rows, expected >= {floor}"


def test_required_columns_present(spec_ids):
    required = {"PERIOD_BEGIN", "REGION", "PROPERTY_TYPE",
               "IS_SEASONALLY_ADJUSTED", "MEDIAN_SALE_PRICE"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = required - cols
        assert not missing, f"{sid}: missing raw columns {missing}"


def test_all_residential_present(spec_ids):
    """The transform filters to 'All Residential'; if that property type is
    absent the published table would be empty."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        pt = pc.unique(pc.utf8_trim_whitespace(table.column("PROPERTY_TYPE")))
        vals = set(pt.to_pylist())
        assert "All Residential" in vals, f"{sid}: no 'All Residential' rows; got {sorted(v for v in vals if v)[:6]}"
