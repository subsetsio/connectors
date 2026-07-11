"""Indeed Hiring Lab connector.

Source: the github.com/hiring-lab org, which publishes its data products as CSV
files across 5 repos (job_postings_tracker [branch master], indeed-wage-tracker,
ai-tracker, remote-tracker, pay-transparency [branch main]). Each catalog entity
maps to one or more CSVs that share a schema; per-country files (the national
job-postings index, the by-sector index) carry an in-file `jobcountry` column so
they union cleanly into one long-format table.

Fetch shape: stateless full re-pull. Every CSV is small (KB-to-low-MB) and the
whole corpus re-fetches in seconds, so there is no watermark/cursor/state — we
re-download every file each run and overwrite the raw asset. Revisions and late
corrections are picked up for free. Raw is saved as NDJSON (all values as strings
from the CSV) and the SQL transform does the typed parse/cast.
"""

import csv
import io
from datetime import datetime


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

# spec_id -> (repo, branch, [paths])  — paths sharing one schema union into one asset.
SOURCES = {
    "indeed-hiring-lab-aggregate-job-postings": (
        "job_postings_tracker", "master",
        [f"{c}/aggregate_job_postings_{c}.csv"
         for c in ("AU", "CA", "DE", "EA", "ES", "FR", "GB", "IE", "IT", "NL", "US")],
    ),
    "indeed-hiring-lab-job-postings-by-sector": (
        "job_postings_tracker", "master",
        [f"{c}/job_postings_by_sector_{c}.csv"
         for c in ("AU", "CA", "DE", "FR", "GB", "US")],
    ),
    "indeed-hiring-lab-metro-job-postings-us": (
        "job_postings_tracker", "master", ["US/metro_job_postings_us.csv"],
    ),
    "indeed-hiring-lab-metro-job-postings-ca": (
        "job_postings_tracker", "master", ["CA/metro_job_postings_CA.csv"],
    ),
    "indeed-hiring-lab-state-job-postings-us": (
        "job_postings_tracker", "master", ["US/state_job_postings_us.csv"],
    ),
    "indeed-hiring-lab-sector-job-title-examples": (
        "job_postings_tracker", "master", ["sector-job-title-examples.csv"],
    ),
    "indeed-hiring-lab-provincial-postings-ca": (
        "job_postings_tracker", "master", ["CA/provincial_postings_ca.csv"],
    ),
    "indeed-hiring-lab-city-postings-gb": (
        "job_postings_tracker", "master", ["GB/city_postings_gb.csv"],
    ),
    "indeed-hiring-lab-regional-gb": (
        "job_postings_tracker", "master", ["GB/regional_gb.csv"],
    ),
    "indeed-hiring-lab-posted-wage-growth-by-country": (
        "indeed-wage-tracker", "main", ["posted-wage-growth-by-country.csv"],
    ),
    "indeed-hiring-lab-posted-wage-growth-by-sector": (
        "indeed-wage-tracker", "main", ["posted-wage-growth-by-sector.csv"],
    ),
    "indeed-hiring-lab-ai-posting": (
        "ai-tracker", "main", ["AI_posting.csv"],
    ),
    "indeed-hiring-lab-remote-postings": (
        "remote-tracker", "main", ["remote_postings.csv"],
    ),
    "indeed-hiring-lab-remote-postings-sector": (
        "remote-tracker", "main", ["remote_postings_sector.csv"],
    ),
    "indeed-hiring-lab-remote-searches": (
        "remote-tracker", "main", ["remote_searches.csv"],
    ),
    "indeed-hiring-lab-pay-transparency-country": (
        "pay-transparency", "main", ["pay-transparency-country.csv"],
    ),
    "indeed-hiring-lab-pay-transparency-sector": (
        "pay-transparency", "main", ["pay-transparency-sector.csv"],
    ),
}


@transient_retry()
def _fetch_csv(repo: str, branch: str, path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/hiring-lab/{repo}/{branch}/{path}"
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    repo, branch, paths = SOURCES[node_id]
    rows = []
    for path in paths:
        text = _fetch_csv(repo, branch, path).decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            # keep raw string values; the transform does typed casting
            clean_row = {(k.strip() if k else k): v for k, v in row.items()}
            if clean_row.get("month"):
                clean_row["month_date"] = datetime.strptime(clean_row["month"], "%b-%y").date().isoformat()
            rows.append(clean_row)
    if not rows:
        raise AssertionError(f"{node_id}: 0 rows parsed from {paths}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download") for sid in SOURCES
]
