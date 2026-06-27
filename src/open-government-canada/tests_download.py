"""Health invariants for open-government-canada raw assets (run post-DAG, in-connector)."""

from subsets_utils import load_raw_ndjson


def test_datasets_corpus_nonempty():
    """The datasets corpus must reflect the real portal (~47k packages). A near-
    empty pull means package_search paging broke or the API shape changed."""
    rows = load_raw_ndjson("open-government-canada-datasets")
    assert len(rows) >= 30000, f"datasets: only {len(rows)} rows (expected ~47k)"
    assert all(r.get("dataset_id") for r in rows[:1000]), "datasets: null dataset_id in sample"


def test_datasets_org_coverage():
    """Datasets should span dozens of publishing organizations; a collapse to a
    handful means the `organization` field stopped coming back."""
    rows = load_raw_ndjson("open-government-canada-datasets")
    orgs = {r.get("organization") for r in rows if r.get("organization")}
    assert len(orgs) >= 50, f"datasets: only {len(orgs)} distinct organizations"


def test_organizations_nonempty():
    """The publisher directory should list well over a hundred organizations."""
    rows = load_raw_ndjson("open-government-canada-organizations")
    assert len(rows) >= 100, f"organizations: only {len(rows)} rows"
    assert all(r.get("org_id") for r in rows), "organizations: null org_id present"
