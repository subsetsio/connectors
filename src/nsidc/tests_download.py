"""Health invariants for the NSIDC Sea Ice Index raw assets.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses — a truncated download, a format flip, one hemisphere missing.
"""

from subsets_utils import load_raw_parquet

DAILY = "nsidc-sea-ice-extent-daily"
MONTHLY = "nsidc-sea-ice-extent-monthly"
CLIMATOLOGY = "nsidc-sea-ice-extent-daily-climatology"

_HEMIS = {"Arctic", "Antarctic"}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_daily_shape():
    t = load_raw_parquet(DAILY)
    # ~16k rows/hemisphere from 1978-present; well over 20k combined.
    assert len(t) >= 20000, f"{DAILY}: only {len(t)} rows, expected >=20000"
    hemis = set(t.column("hemisphere").to_pylist())
    assert hemis == _HEMIS, f"{DAILY}: hemispheres {hemis}, expected {_HEMIS}"
    # Extent must carry real (non-null) values, in the physical 0-25 range.
    extents = [v for v in t.column("extent_million_km2").to_pylist() if v is not None]
    assert len(extents) >= 20000, f"{DAILY}: too few non-null extents ({len(extents)})"
    assert min(extents) >= 0 and max(extents) <= 25, (
        f"{DAILY}: extent out of range [{min(extents)}, {max(extents)}]"
    )
    years = {int(d[:4]) for d in t.column("date").to_pylist()}
    assert min(years) <= 1979, f"{DAILY}: earliest year {min(years)}, expected <=1979"


def test_monthly_shape():
    t = load_raw_parquet(MONTHLY)
    assert len(t) >= 1000, f"{MONTHLY}: only {len(t)} rows, expected >=1000"
    hemis = set(t.column("hemisphere").to_pylist())
    assert hemis == _HEMIS, f"{MONTHLY}: hemispheres {hemis}, expected {_HEMIS}"
    months = {d[5:7] for d in t.column("date").to_pylist()}
    expected_months = {f"{m:02d}" for m in range(1, 13)}
    assert months == expected_months, f"{MONTHLY}: months {months}, expected all 12"
    extents = [v for v in t.column("extent_million_km2").to_pylist() if v is not None]
    assert extents and min(extents) >= 0 and max(extents) <= 25, (
        f"{MONTHLY}: extent out of range"
    )


def test_climatology_shape():
    t = load_raw_parquet(CLIMATOLOGY)
    # 366 day-of-year rows × 2 hemispheres.
    assert len(t) == 732, f"{CLIMATOLOGY}: {len(t)} rows, expected 732"
    doys = t.column("day_of_year").to_pylist()
    assert min(doys) == 1 and max(doys) == 366, (
        f"{CLIMATOLOGY}: day_of_year range [{min(doys)}, {max(doys)}], expected [1, 366]"
    )
    hemis = set(t.column("hemisphere").to_pylist())
    assert hemis == _HEMIS, f"{CLIMATOLOGY}: hemispheres {hemis}, expected {_HEMIS}"
    # Percentile ordering sanity on a sample row.
    p10 = t.column("pctl_10_million_km2").to_pylist()
    p90 = t.column("pctl_90_million_km2").to_pylist()
    assert all(a <= b for a, b in zip(p10, p90) if a is not None and b is not None), (
        f"{CLIMATOLOGY}: found pctl_10 > pctl_90"
    )
