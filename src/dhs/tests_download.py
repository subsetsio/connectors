"""Health-invariant tests for the DHS OHSS Yearbook connector.

Run post-DAG, in-connector. They catch silent degradation that mere file
existence misses: a renamed/missing sheet, a header-detection regression that
drops most rows, or a parse that yields labels but no numeric values.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "topic", "table_label", "title", "section",
    "category", "breakdown", "value", "value_note",
}


def test_every_asset_has_data(spec_ids):
    """Every downloaded table must yield a non-trivial tidy long table with the
    expected schema and at least some parsed numeric values. A table that comes
    back tiny or all-null means header detection or value parsing broke."""
    dhs_ids = [s for s in spec_ids if s.startswith("dhs-")]
    assert dhs_ids, f"no dhs- specs ran: {spec_ids}"
    for sid in dhs_ids:
        t = load_raw_parquet(sid)
        assert set(t.column_names) == EXPECTED_COLUMNS, (
            f"{sid}: columns {t.column_names} != {sorted(EXPECTED_COLUMNS)}"
        )
        assert t.num_rows >= 10, f"{sid}: only {t.num_rows} rows"
        numeric = sum(1 for v in t.column("value").to_pylist() if v is not None)
        assert numeric >= t.num_rows // 2, (
            f"{sid}: only {numeric}/{t.num_rows} rows have a numeric value"
        )


def test_lpr_table1_full_year_history(spec_ids):
    """LPR Table 1 is the flagship long series: one row per fiscal year from
    1820 to the current year (~200+). A short result means the repeated
    Year/Number block layout stopped being unstacked."""
    sid = "dhs-lawful-permanent-residents-table-1"
    assert sid in spec_ids, f"{sid} not among ran specs"
    t = load_raw_parquet(sid)
    years = [c for c in t.column("category").to_pylist() if c and c[:4].isdigit()]
    assert len(years) >= 190, f"{sid}: only {len(years)} year rows; expected >=190"
    yrs = [int(c[:4]) for c in years]
    assert min(yrs) <= 1820, f"{sid}: earliest year {min(yrs)} > 1820"
    assert max(yrs) >= 2023, f"{sid}: latest year {max(yrs)} < 2023"


def test_country_breakdown_tables_have_years(spec_ids):
    """The by-country tables (LPR Table 2, Refugees Table 14, Naturalizations
    Table 22) are melted long: their breakdown column must carry fiscal-year
    values and dozens of country categories. Guards against a melt regression
    that collapses the year columns."""
    for sid, min_cats in [
        ("dhs-lawful-permanent-residents-table-2", 100),
        ("dhs-refugees-table-14", 50),
        ("dhs-naturalizations-table-22", 100),
    ]:
        assert sid in spec_ids, f"{sid} not among ran specs"
        t = load_raw_parquet(sid)
        breakdowns = set(t.column("breakdown").to_pylist())
        year_cols = {b for b in breakdowns if b and b.isdigit() and b.startswith("20")}
        assert len(year_cols) >= 5, f"{sid}: only year breakdowns {sorted(year_cols)}"
        cats = {c for c in t.column("category").to_pylist() if c}
        assert len(cats) >= min_cats, f"{sid}: only {len(cats)} categories"
