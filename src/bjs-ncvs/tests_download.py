from subsets_utils import load_raw_parquet

# Minimum row counts per resource, from count(*) probed Jun 2026 (data through
# collection year 2024). Set well below observed so normal annual growth never
# trips them, but a truncated pull (pagination broke after page 1) does.
MIN_ROWS = {
    "bjs-ncvs-gcuy-rt5g": 60000,    # observed ~68.9k
    "bjs-ncvs-r4j4-fdwx": 6000000,  # observed ~6.34M
    "bjs-ncvs-gkck-euys": 200000,   # observed ~247.6k
    "bjs-ncvs-ya4e-n9zp": 4000000,  # observed ~4.52M
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every resource's raw parquet should hold rows; empty means the SODA2
    endpoint changed format or paging silently failed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_row_counts_plausible(spec_ids):
    """Raw row counts should clear the per-resource floors; a count far below
    means truncated pagination, not a normal year-over-year change."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor}"


def test_year_column_present(spec_ids):
    """Every resource carries a 'year' column (the longitudinal axis); its
    absence means the schema/field order drifted upstream."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).column_names
        assert "year" in cols, f"{sid}: no 'year' column in {cols}"
