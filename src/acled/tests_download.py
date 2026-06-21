"""Health-invariant tests for ACLED raw assets — run post-DAG, in-connector.

Catch silent degradation that file-existence misses: empty payloads, a sheet
layout change that drops all rows, or a measure losing its fatalities column.
"""
from subsets_utils import load_raw_parquet

# Minimum plausible row counts. National = ~240 countries x ~350 months for the
# long series; subnational = ~1M admin2-month rows. Set well below observed so a
# real shrink trips the test without false alarms on normal weekly growth.
_MIN_ROWS = {
    "acled-political-violence-events-and-fatalities": 20_000,
    "acled-civilian-targeting-events-and-fatalities": 20_000,
    "acled-demonstration-events": 20_000,
    "acled-political-violence-subnational": 200_000,
    "acled-civilian-targeting-subnational": 200_000,
    "acled-demonstration-events-subnational": 200_000,
}

_SUBNATIONAL = {sid for sid in _MIN_ROWS if sid.endswith("subnational")}
_HAS_FATALITIES = {
    sid for sid in _MIN_ROWS if not sid.startswith("acled-demonstration")
}


def test_all_raw_assets_present_and_nonempty(spec_ids):
    """Every download spec must produce a non-trivially-sized raw parquet."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows < expected floor {floor}"


def test_expected_columns(spec_ids):
    """Schema didn't silently drift — month/year/events always present, admin
    columns only on subnational, fatalities only on the violence measures."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"country", "month", "year", "events"} <= cols, f"{sid}: missing core cols, got {cols}"
        if sid in _SUBNATIONAL:
            assert {"admin1", "admin2", "iso3"} <= cols, f"{sid}: subnational missing admin cols, got {cols}"
        if sid in _HAS_FATALITIES:
            assert "fatalities" in cols, f"{sid}: expected fatalities column, got {cols}"
        else:
            assert "fatalities" not in cols, f"{sid}: demonstration must not carry fatalities, got {cols}"


def test_counts_nonnegative_and_year_in_range(spec_ids):
    """Events/fatalities are counts (>=0); years fall in ACLED's coverage window."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert pc.min(table["events"]).as_py() >= 0, f"{sid}: negative event count"
        yrs = table["year"]
        assert pc.min(yrs).as_py() >= 1997, f"{sid}: year before 1997"
        assert pc.max(yrs).as_py() <= 2100, f"{sid}: implausible future year"
