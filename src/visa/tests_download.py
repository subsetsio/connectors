"""Health-invariant tests for the Visa SMI connector raw assets.

These run post-DAG against the persisted raw parquet via subsets_utils loaders,
catching silent degradation (empty/truncated downloads, a workbook layout
change that yields the wrong columns)."""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "visa-north-america-smi": {
        "date", "geography", "spending_segment", "seasonal_adjustment", "index_value",
    },
    "visa-global-smi": {
        "date", "country_code", "country", "spending_segment", "index_value",
    },
}

# Each workbook has years of monthly history across several series, so the long
# tables hold hundreds of rows; a collapse to a handful means parsing broke.
MIN_ROWS = {
    "visa-north-america-smi": 500,
    "visa-global-smi": 200,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty usually means the URL
    started 404ing or the xlsx layout changed and parsing yielded nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    """The reshape must produce the long-format columns the transform reads."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        want = EXPECTED_COLUMNS.get(sid)
        if want is not None:
            assert want <= cols, f"{sid}: missing columns {want - cols}"


def test_row_counts_reasonable(spec_ids):
    """Guard against a partially-parsed workbook (only one block melted, etc.)."""
    for sid in spec_ids:
        n = len(load_raw_parquet(sid))
        floor = MIN_ROWS.get(sid, 1)
        assert n >= floor, f"{sid}: only {n} rows, expected >= {floor}"
