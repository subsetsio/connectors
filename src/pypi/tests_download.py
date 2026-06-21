"""Health invariants for the PyPI raw assets — catch silent degradation that
file existence alone misses (empty payloads, format drift, capped fetches)."""
from subsets_utils import load_raw_parquet


def test_popular_packages_shape(spec_ids):
    """The popular_packages snapshot must be densely populated: thousands of
    ranked packages, each with a positive 30-day download count."""
    sid = "pypi-popular-packages"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 4000, f"{sid}: only {t.num_rows} packages (expected ~5000)"
    names = t.column("package").to_pylist()
    assert all(names), f"{sid}: some package names are empty"
    assert len(set(names)) == len(names), f"{sid}: duplicate package names"
    dls = [int(x) for x in t.column("download_count_30d").to_pylist() if x is not None]
    assert dls and min(dls) > 0, f"{sid}: non-positive download counts present"


def test_download_trends_shape(spec_ids):
    """The download_trends panel must hold the daily series for many packages,
    both mirror categories, across a multi-month window."""
    sid = "pypi-download-trends"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 50000, f"{sid}: only {t.num_rows} rows (expected hundreds of thousands)"
    cats = set(t.column("category").to_pylist())
    assert cats == {"with_mirrors", "without_mirrors"}, f"{sid}: unexpected categories {cats}"
    packages = set(t.column("package").to_pylist())
    assert len(packages) >= 500, f"{sid}: only {len(packages)} packages with stats"
    days = set(t.column("date").to_pylist())
    assert len(days) >= 90, f"{sid}: only {len(days)} distinct days (window too short)"
