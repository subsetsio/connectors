"""Health-invariant tests for the NASA GISTEMP raw assets.

These run post-DAG, in-connector, reading raw via the same loader the download
nodes used. They catch silent degradation that file-existence misses: a format
switch upstream, a truncated download, anomalies in implausible units.
"""
from subsets_utils import load_raw_parquet

REGIONS = {"Global", "Northern Hemisphere", "Southern Hemisphere"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. GISTEMP starts in 1880, so
    even the annual table has >140 rows × 3 regions — anything tiny means the
    CSV header changed or the download truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_annual_coverage():
    """Annual table spans 1880-present across all three regions."""
    t = load_raw_parquet("nasa-gistemp-annual").to_pydict()
    years = t["year"]
    assert min(years) <= 1880, f"annual min year {min(years)} > 1880 — series start lost"
    assert max(years) >= 2024, f"annual max year {max(years)} < 2024 — stale download"
    assert set(t["region"]) == REGIONS, f"annual regions {set(t['region'])} != {REGIONS}"


def test_anomalies_in_celsius_range():
    """Anomalies are decimal degrees C vs 1951-1980 (roughly -3..+4). A value
    magnitude <0.05 everywhere would mean someone re-introduced the /100 bug;
    a magnitude >20 would mean raw integers leaked through."""
    for sid in ("nasa-gistemp-monthly", "nasa-gistemp-annual", "nasa-gistemp-zonal-annual"):
        vals = load_raw_parquet(sid).to_pydict()["anomaly_c"]
        assert vals, f"{sid}: no anomaly values"
        mx = max(abs(v) for v in vals)
        assert 0.1 < mx < 20.0, f"{sid}: max |anomaly| {mx} outside plausible degC range"


def test_monthly_keys_unique():
    """(month, region) is the natural key — no duplicates from the melt."""
    t = load_raw_parquet("nasa-gistemp-monthly").to_pydict()
    keys = list(zip(t["month"], t["region"]))
    assert len(keys) == len(set(keys)), "monthly has duplicate (month, region) keys"
