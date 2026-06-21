"""Health invariants for Indeed Hiring Lab raw assets (NDJSON, all-string rows)."""

from subsets_utils import load_raw_ndjson

# spec_id -> a column that must be present and non-empty on at least one row
_KEY_COLUMN = {
    "indeed-hiring-lab-aggregate-job-postings": "indeed_job_postings_index_SA",
    "indeed-hiring-lab-job-postings-by-sector": "indeed_job_postings_index",
    "indeed-hiring-lab-metro-job-postings-us": "metro",
    "indeed-hiring-lab-metro-job-postings-ca": "Metro",
    "indeed-hiring-lab-state-job-postings-us": "state",
    "indeed-hiring-lab-provincial-postings-ca": "province",
    "indeed-hiring-lab-city-postings-gb": "cities",
    "indeed-hiring-lab-regional-gb": "region",
    "indeed-hiring-lab-posted-wage-growth-by-country": "posted_wage_growth_yoy",
    "indeed-hiring-lab-posted-wage-growth-by-sector": "sector",
    "indeed-hiring-lab-ai-posting": "AI_share_postings",
    "indeed-hiring-lab-remote-postings": "remote_share_postings",
    "indeed-hiring-lab-remote-postings-sector": "normtitlecategory_consistent",
    "indeed-hiring-lab-remote-searches": "remote_share_searches",
    "indeed-hiring-lab-pay-transparency-country": "pay_transparency_pct",
    "indeed-hiring-lab-pay-transparency-sector": "sector",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows; empty means the raw CSV moved or
    the endpoint changed format silently."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_expected_columns_present(spec_ids):
    """Each asset's signature column must exist and be populated on some row —
    catches a header rename or a truncated/garbled download."""
    for sid in spec_ids:
        col = _KEY_COLUMN.get(sid)
        if col is None:
            continue
        rows = load_raw_ndjson(sid)
        assert col in rows[0], f"{sid}: expected column '{col}' missing (got {sorted(rows[0])})"
        assert any((r.get(col) or "").strip() for r in rows), \
            f"{sid}: column '{col}' is empty across all {len(rows)} rows"


def test_country_index_spans_many_countries(spec_ids):
    """The national index must union ~11 countries; if the multi-file fetch
    silently dropped files we'd see one country."""
    sid = "indeed-hiring-lab-aggregate-job-postings"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    countries = {r.get("jobcountry") for r in rows}
    assert len(countries) >= 7, f"{sid}: only {len(countries)} countries ({countries}); multi-file union likely broke"
