"""Health invariants for the CRU country-values raw asset."""

from subsets_utils import load_raw_parquet

EXPECTED_VARS = {"cld", "dtr", "frs", "pet", "pre", "tmn", "tmx", "tmp", "vap", "wet"}
EXPECTED_PERIODS = {
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
    "MAM", "JJA", "SON", "DJF", "ANN",
}


def test_raw_nonempty(spec_ids):
    """A full CY crawl yields millions of long-format rows; a tiny table means
    the directory enumeration broke after one variable/country."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert len(t) > 1_000_000, f"{sid}: only {len(t)} rows (expected >1M)"


def test_all_variables_present(spec_ids):
    """All 10 CRU variables must appear; a missing one means a dir 404'd silently."""
    t = load_raw_parquet("cru-country-values")
    got = set(t.column("variable").to_pylist())
    assert got == EXPECTED_VARS, f"variable set drifted: {sorted(got)}"


def test_periods_and_year_range(spec_ids):
    """Periods must be the 17 known labels and years span the 1901-2024 record."""
    t = load_raw_parquet("cru-country-values")
    periods = set(t.column("period").to_pylist())
    assert periods <= EXPECTED_PERIODS, f"unexpected periods: {periods - EXPECTED_PERIODS}"
    assert periods == EXPECTED_PERIODS, f"missing periods: {EXPECTED_PERIODS - periods}"
    years = t.column("year").to_pylist()
    assert min(years) <= 1901 and max(years) >= 2020, f"year span off: {min(years)}-{max(years)}"


def test_country_coverage(spec_ids):
    """Should cover a few hundred countries/territories, not a handful."""
    t = load_raw_parquet("cru-country-values")
    n = len(set(t.column("country").to_pylist()))
    assert n >= 200, f"only {n} distinct countries (expected >=200)"


def test_values_plausible(spec_ids):
    """No missing-value sentinels should survive parsing."""
    t = load_raw_parquet("cru-country-values")
    vals = t.column("value").to_pylist()
    assert all(v != -999.0 for v in vals), "missing-value sentinel -999.0 leaked into output"
