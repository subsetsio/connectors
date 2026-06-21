"""Health invariants for the SILSO raw downloads — catch silent degradation
(endpoint format switch, truncated download) that file existence alone misses."""
from subsets_utils import load_raw_parquet

# Rough lower bounds on row counts per series, from the live source (well below
# observed: daily-total ~76k, monthly ~3.3k, yearly ~326, daily-hem ~12.5k,
# monthly-hem ~413). A big shortfall means a truncated/changed file.
_MIN_ROWS = {
    "silso-daily-total": 70000,
    "silso-monthly-total": 3000,
    "silso-monthly-smoothed-total": 3000,
    "silso-yearly-total": 300,
    "silso-daily-hemispheric": 11000,
    "silso-monthly-hemispheric": 380,
    "silso-monthly-smoothed-hemispheric": 380,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_row_counts_plausible(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: {n} rows, expected >= {floor} (truncated?)"


def test_year_column_sane(spec_ids):
    """Every series carries a year (or year_mid) column within a plausible range;
    a wrong separator or shifted columns would blow this up."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = "year" if "year" in table.column_names else "year_mid"
        years = table.column(col).to_pylist()
        assert min(years) >= 1700, f"{sid}: min {col} {min(years)} < 1700"
        assert max(years) <= 2100, f"{sid}: max {col} {max(years)} > 2100"
