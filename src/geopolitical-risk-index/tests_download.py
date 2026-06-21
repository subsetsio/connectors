"""Health invariants for the Geopolitical Risk Index raw assets.

These run post-DAG, in-connector, against the parquet the download nodes wrote.
They catch silent degradation a file-exists check misses: a format switch that
empties a frame, a truncated download, or the country reshape collapsing.
"""
from subsets_utils import load_raw_parquet


def test_monthly_nonempty_and_long_history():
    t = load_raw_parquet("geopolitical-risk-index-gpr-monthly")
    assert len(t) >= 1000, f"monthly: only {len(t)} rows (expected >1000 months since 1900)"
    cols = set(t.column_names)
    for c in ("month", "gpr", "gprt", "gpra", "gprh"):
        assert c in cols, f"monthly: missing expected column {c}"
    # No country columns should leak into the global table.
    assert not [c for c in cols if c.startswith("gprc_") or c.startswith("gprhc_")], \
        "monthly: country columns leaked into the global table"


def test_country_monthly_long_shape():
    t = load_raw_parquet("geopolitical-risk-index-gpr-country-monthly")
    cols = set(t.column_names)
    assert cols == {"month", "country", "gprc", "gprhc"}, f"country: unexpected columns {cols}"
    countries = set(t.column("country").to_pylist())
    assert len(countries) >= 40, f"country: only {len(countries)} distinct countries (expected ~44)"
    assert "USA" in countries and "CHN" in countries, "country: expected ISO3 codes missing"


def test_daily_nonempty_recent():
    t = load_raw_parquet("geopolitical-risk-index-gpr-daily")
    assert len(t) >= 10000, f"daily: only {len(t)} rows (expected >10000 days since 1985)"
    cols = set(t.column_names)
    for c in ("date", "gprd", "gprd_act", "gprd_threat", "event"):
        assert c in cols, f"daily: missing expected column {c}"
    import pyarrow.compute as pc
    nonnull = pc.sum(pc.is_valid(t.column("gprd"))).as_py()
    assert nonnull > 0, "daily: gprd is entirely null"
