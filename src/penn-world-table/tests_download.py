"""Health-invariant tests for Penn World Table raw assets — run post-DAG.

Catch silent degradation that file-existence misses: a Dataverse manifest
change that drops a table, a Stata layout change that empties rows, or the key
country/year columns disappearing. Row floors are set well below the observed
PWT 11.0 sizes so normal growth (new years per release) never trips them while a
real shrink does.
"""
from subsets_utils import load_raw_parquet

# Observed PWT 11.0 row counts -> floors set comfortably below.
_MIN_ROWS = {
    "penn-world-table-main": 10_000,                  # ~13,690
    "penn-world-table-na-data": 9_000,               # ~13,114
    "penn-world-table-capital-detail": 9_000,        # ~13,320
    "penn-world-table-labor-detail": 9_000,          # ~13,114
    "penn-world-table-trade-detail": 9_000,          # ~13,690
    "penn-world-table-sh-bilateral-cor-data": 200_000,  # ~393,970
}

_BILATERAL = "penn-world-table-sh-bilateral-cor-data"


def test_all_raw_assets_present_and_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows < floor {floor}"


def test_key_columns_present(spec_ids):
    """Panels are keyed (countrycode, year); the bilateral table is keyed
    (countrycode1, countrycode2, year). If these vanish the parse broke."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if sid == _BILATERAL:
            assert {"countrycode1", "countrycode2", "year"} <= cols, \
                f"{sid}: missing bilateral key cols, got {sorted(cols)}"
        else:
            assert {"countrycode", "year"} <= cols, \
                f"{sid}: missing panel key cols, got {sorted(cols)}"


def test_main_has_headline_variables(spec_ids):
    """The flagship panel must carry the core PWT measures."""
    if "penn-world-table-main" not in spec_ids:
        return
    cols = set(load_raw_parquet("penn-world-table-main").column_names)
    assert {"rgdpe", "rgdpo", "pop", "emp"} <= cols, \
        f"main missing headline variables, got {sorted(cols)}"


def test_year_in_plausible_range(spec_ids):
    """PWT spans 1950-present; guard against a corrupt parse shifting the axis."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        years = load_raw_parquet(sid)["year"]
        ymin = pc.min(years).as_py()
        ymax = pc.max(years).as_py()
        assert ymin is not None and int(ymin) >= 1950, f"{sid}: min year {ymin} < 1950"
        assert int(ymax) <= 2100, f"{sid}: implausible max year {ymax}"
