"""Health-invariant tests for the l2beat connector raw assets.

These run post-DAG, in-connector, via subsets_utils loaders — so they catch
silent degradation (rate-limit wipeout, format drift, empty payloads) that
mere file-existence checks miss.
"""

from subsets_utils import load_raw_parquet


def test_projects_catalog_populated(spec_ids):
    """The projects catalog should list ~116 tracked projects. A sharp drop
    means the summary payload shape changed."""
    if "l2beat-projects" not in spec_ids:
        return
    t = load_raw_parquet("l2beat-projects")
    assert t.num_rows >= 80, f"projects catalog has {t.num_rows} rows; expected ~116"
    slugs = set(t.column("slug").to_pylist())
    assert "arbitrum" in slugs, "flagship project 'arbitrum' missing from catalog"


def test_tvs_coverage(spec_ids):
    """TVS series must cover most projects with real daily history. If the
    Cloudflare rate limit wiped the crawl, distinct-project count collapses."""
    if "l2beat-tvs" not in spec_ids:
        return
    t = load_raw_parquet("l2beat-tvs")
    assert t.num_rows > 10000, f"tvs has only {t.num_rows} rows; crawl likely throttled out"
    projects = set(t.column("project_slug").to_pylist())
    # ~116 projects + aggregate; allow some skips but flag a gutted crawl.
    assert len(projects) >= 90, f"tvs covers only {len(projects)} projects; expected ~117"


def test_activity_coverage(spec_ids):
    """Activity series must cover a broad set of projects with daily history."""
    if "l2beat-activity" not in spec_ids:
        return
    t = load_raw_parquet("l2beat-activity")
    assert t.num_rows > 5000, f"activity has only {t.num_rows} rows; crawl likely throttled out"
    projects = set(t.column("project_slug").to_pylist())
    assert len(projects) >= 70, f"activity covers only {len(projects)} projects; expected many"


def test_tvs_values_present(spec_ids):
    """Guard against an all-null TVS column (would signal a column-mapping break)."""
    if "l2beat-tvs" not in spec_ids:
        return
    t = load_raw_parquet("l2beat-tvs")
    import pyarrow.compute as pc

    nonnull = pc.sum(pc.is_valid(t.column("canonical"))).as_py()
    assert nonnull > 0, "tvs 'canonical' column is entirely null"


def test_projects_current_tvs_populated(spec_ids):
    """Most projects should carry a current TVS snapshot (from summary
    breakdown.total). All-null means the `tvs` field shape changed."""
    if "l2beat-projects" not in spec_ids:
        return
    import pyarrow.compute as pc

    t = load_raw_parquet("l2beat-projects")
    nonnull = pc.sum(pc.is_valid(t.column("current_tvs_usd"))).as_py()
    assert nonnull >= 30, f"only {nonnull} projects have current_tvs_usd; field shape may have changed"
