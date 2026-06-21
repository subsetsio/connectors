"""Health invariants for USAspending raw assets, run post-DAG in-connector."""
from subsets_utils import load_raw_parquet

_MONTHLY = "usaspending-monthly-spending-by-award-type"


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet must hold rows. An empty payload usually means
    the endpoint changed shape or a filter silently stopped matching."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_dimension_tables_multi_year(spec_ids):
    """Annual dimension tables must span several completed fiscal years; if we
    got a single year the submission_periods discovery probably broke."""
    for sid in spec_ids:
        if sid == _MONTHLY:
            continue
        table = load_raw_parquet(sid)
        years = set(table.column("fiscal_year").to_pylist())
        assert len(years) >= 5, f"{sid}: only {len(years)} fiscal years: {sorted(years)}"


def test_monthly_history_and_award_split(spec_ids):
    """Monthly series must reach back to the FY2008 floor and carry real
    award-type splits (not an all-zero column)."""
    if _MONTHLY not in spec_ids:
        return
    table = load_raw_parquet(_MONTHLY)
    assert len(table) >= 180, f"{_MONTHLY}: only {len(table)} months; expected >=180"
    dates = sorted(table.column("date").to_pylist())
    assert dates[0] <= "2009-01-01", f"{_MONTHLY}: earliest month {dates[0]} too recent"
    contract = table.column("contract_obligations").to_pylist()
    assert any(v not in (None, 0.0) for v in contract), \
        f"{_MONTHLY}: contract_obligations all zero/null — award split missing"
