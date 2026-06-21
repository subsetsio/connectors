"""Health-invariant tests for the npm connector raw assets."""
from subsets_utils import load_raw_parquet


def test_popular_packages(spec_ids):
    """The popular-package enumeration must return a substantial, name-unique
    set; a tiny result means search pagination broke or wrapped early."""
    t = load_raw_parquet("npm-popular-packages")
    assert t.num_rows >= 1500, f"popular-packages only {t.num_rows} rows"
    names = t.column("name").to_pylist()
    assert all(names), "popular-packages has empty names"
    assert len(set(names)) == len(names), "popular-packages has duplicate names"


def test_daily_downloads(spec_ids):
    """Daily downloads should hold many (package, date) rows; non-negative."""
    t = load_raw_parquet("npm-daily-downloads")
    assert t.num_rows >= 50000, f"daily-downloads only {t.num_rows} rows"
    assert min(t.column("downloads").to_pylist()) >= 0, "negative download count"


def test_package_versions(spec_ids):
    """Version timeline should explode to far more rows than packages."""
    t = load_raw_parquet("npm-package-versions")
    assert t.num_rows >= 20000, f"package-versions only {t.num_rows} rows"
    pkgs = set(t.column("package").to_pylist())
    assert len(pkgs) >= 1000, f"only {len(pkgs)} distinct packages in versions"


def test_security_advisories(spec_ids):
    """Advisories across all published versions of popular packages should be a
    substantial, multi-severity set; a tiny/constant result means we regressed
    to latest-version-only matching."""
    t = load_raw_parquet("npm-security-advisories")
    assert t.num_rows >= 500, f"security-advisories only {t.num_rows} rows"
    sev = set(t.column("severity").to_pylist())
    assert sev <= {"low", "moderate", "high", "critical", "info"}, f"odd severities: {sev}"
    assert len(sev) >= 2, f"severity not varied: {sev}"


def test_registry_stats(spec_ids):
    """Registry stats holds at least today's snapshot with a sane doc_count."""
    t = load_raw_parquet("npm-registry-stats")
    assert t.num_rows >= 1, "registry-stats has 0 rows"
    assert max(t.column("doc_count").to_pylist()) > 3_000_000, "doc_count implausibly low"
