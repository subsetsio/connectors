"""Health invariants for the UNWTO tourism raw download.

These run post-DAG, in-connector, reading raw through subsets_utils loaders.
They catch silent degradation the file-existence check misses: an empty/
truncated CSV, a dropped series, a collapsed year range, or all-null values.
"""

from subsets_utils import load_raw_parquet

ASSET = "unwto-tourism-arrivals-expenditure"


def test_raw_nonempty():
    """The SYB tourism CSV holds ~2000+ long-format rows. A near-empty table
    means the endpoint changed format, redirected, or the banner-skip broke."""
    table = load_raw_parquet(ASSET)
    assert len(table) >= 1500, f"{ASSET}: only {len(table)} rows; expected >=1500"


def test_both_series_present():
    """Both upstream series must survive parsing — losing one would silently
    blank a whole column in the published wide table."""
    series = set(load_raw_parquet(ASSET).column("series").to_pylist())
    assert series == {"arrivals", "expenditure"}, f"unexpected series set: {series}"


def test_year_span_and_values():
    """Multiple years and non-null numeric values present — guards against a
    snapshot that parsed to a single year or all-null values."""
    table = load_raw_parquet(ASSET)
    years = set(table.column("year").to_pylist())
    assert len(years) >= 3, f"only {len(years)} distinct years: {sorted(years)}"
    assert min(years) <= 2000, f"earliest year {min(years)} too late; expected <=2000"
    values = [v for v in table.column("value").to_pylist() if v is not None]
    assert len(values) >= 1000, f"only {len(values)} non-null values"


def test_country_codes_valid():
    """Country codes are positive M49 integers and country names non-empty."""
    table = load_raw_parquet(ASSET)
    codes = table.column("country_code").to_pylist()
    assert all(isinstance(c, int) and c > 0 for c in codes), "invalid country_code"
    names = table.column("country").to_pylist()
    assert all(n for n in names), "found empty country name"
