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


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
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
            rows.append({(k.strip() if k else k): v for k, v in row.items()})
    if not rows:
        raise AssertionError(f"{node_id}: 0 rows parsed from {paths}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download") for sid in SOURCES
]

# --- transforms: one published Delta table per subset, typed parse from raw ndjson ---

_JPI_INDEX = "indeed_job_postings_index"

# subnational job-postings index tables: (spec_id, raw geo column, published geo column)
_SUBNATIONAL = [
    ("indeed-hiring-lab-metro-job-postings-ca", '"Metro"', "metro"),
    ("indeed-hiring-lab-state-job-postings-us", '"state"', "state"),
    ("indeed-hiring-lab-provincial-postings-ca", '"province"', "province"),
    ("indeed-hiring-lab-city-postings-gb", '"cities"', "city"),
    ("indeed-hiring-lab-regional-gb", '"region"', "region"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="indeed-hiring-lab-aggregate-job-postings-transform",
        deps=["indeed-hiring-lab-aggregate-job-postings"],
        sql=f'''
            SELECT
                TRY_CAST("date" AS DATE)                          AS date,
                "jobcountry"                                      AS jobcountry,
                TRY_CAST("indeed_job_postings_index_SA" AS DOUBLE)  AS index_sa,
                TRY_CAST("indeed_job_postings_index_NSA" AS DOUBLE) AS index_nsa,
                "variable"                                        AS variable
            FROM "indeed-hiring-lab-aggregate-job-postings"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-job-postings-by-sector-transform",
        deps=["indeed-hiring-lab-job-postings-by-sector"],
        sql=f'''
            SELECT
                TRY_CAST("date" AS DATE)                       AS date,
                "jobcountry"                                   AS jobcountry,
                TRY_CAST("{_JPI_INDEX}" AS DOUBLE)             AS index,
                "variable"                                     AS variable,
                "display_name"                                 AS sector
            FROM "indeed-hiring-lab-job-postings-by-sector"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-metro-job-postings-us-transform",
        deps=["indeed-hiring-lab-metro-job-postings-us"],
        sql=f'''
            SELECT
                TRY_CAST("date" AS DATE)               AS date,
                "metro"                                AS metro,
                TRY_CAST("cbsa_code" AS INTEGER)       AS cbsa_code,
                TRY_CAST("{_JPI_INDEX}" AS DOUBLE)     AS index
            FROM "indeed-hiring-lab-metro-job-postings-us"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-ai-posting-transform",
        deps=["indeed-hiring-lab-ai-posting"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                  AS date,
                "jobcountry"                              AS jobcountry,
                TRY_CAST("AI_share_postings" AS DOUBLE)   AS ai_share_postings
            FROM "indeed-hiring-lab-ai-posting"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-remote-postings-transform",
        deps=["indeed-hiring-lab-remote-postings"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                      AS date,
                "jobcountry"                                  AS jobcountry,
                TRY_CAST("remote_share_postings" AS DOUBLE)   AS remote_share_postings
            FROM "indeed-hiring-lab-remote-postings"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-remote-postings-sector-transform",
        deps=["indeed-hiring-lab-remote-postings-sector"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                      AS date,
                "jobcountry"                                  AS jobcountry,
                "normtitlecategory_consistent"               AS sector,
                TRY_CAST("remote_share_postings" AS DOUBLE)   AS remote_share_postings
            FROM "indeed-hiring-lab-remote-postings-sector"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-remote-searches-transform",
        deps=["indeed-hiring-lab-remote-searches"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                      AS date,
                "jobcountry"                                  AS jobcountry,
                TRY_CAST("remote_share_searches" AS DOUBLE)   AS remote_share_searches
            FROM "indeed-hiring-lab-remote-searches"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-pay-transparency-country-transform",
        deps=["indeed-hiring-lab-pay-transparency-country"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                          AS date,
                "country_code"                                    AS country_code,
                "country"                                         AS country,
                TRY_CAST("pay_transparency_pct" AS DOUBLE)        AS pay_transparency_pct,
                TRY_CAST("pay_transparency_pct_3ma" AS DOUBLE)    AS pay_transparency_pct_3ma
            FROM "indeed-hiring-lab-pay-transparency-country"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-pay-transparency-sector-transform",
        deps=["indeed-hiring-lab-pay-transparency-sector"],
        sql='''
            SELECT
                TRY_CAST("date" AS DATE)                          AS date,
                "country_code"                                    AS country_code,
                "country"                                         AS country,
                "sector"                                          AS sector,
                TRY_CAST("pay_transparency_pct" AS DOUBLE)        AS pay_transparency_pct,
                TRY_CAST("pay_transparency_pct_3ma" AS DOUBLE)    AS pay_transparency_pct_3ma
            FROM "indeed-hiring-lab-pay-transparency-sector"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-posted-wage-growth-by-country-transform",
        deps=["indeed-hiring-lab-posted-wage-growth-by-country"],
        sql='''
            SELECT
                "jobcountry"                                              AS jobcountry,
                "country"                                                 AS country,
                CAST(try_strptime("month", '%b-%y') AS DATE)              AS month,
                TRY_CAST("n_obs" AS BIGINT)                               AS n_obs,
                TRY_CAST("posted_wage_growth_yoy" AS DOUBLE)              AS posted_wage_growth_yoy,
                TRY_CAST("posted_wage_growth_yoy_3moavg" AS DOUBLE)       AS posted_wage_growth_yoy_3moavg
            FROM "indeed-hiring-lab-posted-wage-growth-by-country"
            WHERE try_strptime("month", '%b-%y') IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indeed-hiring-lab-posted-wage-growth-by-sector-transform",
        deps=["indeed-hiring-lab-posted-wage-growth-by-sector"],
        sql='''
            SELECT
                "jobcountry"                                              AS jobcountry,
                "country"                                                 AS country,
                "sector"                                                  AS sector,
                CAST(try_strptime("month", '%b-%y') AS DATE)              AS month,
                TRY_CAST("n_obs" AS BIGINT)                               AS n_obs,
                TRY_CAST("posted_wage_growth_yoy" AS DOUBLE)              AS posted_wage_growth_yoy,
                TRY_CAST("posted_wage_growth_yoy_3moavg" AS DOUBLE)       AS posted_wage_growth_yoy_3moavg
            FROM "indeed-hiring-lab-posted-wage-growth-by-sector"
            WHERE try_strptime("month", '%b-%y') IS NOT NULL
        ''',
    ),
] + [
    SqlNodeSpec(
        id=f"{sid}-transform",
        deps=[sid],
        sql=f'''
            SELECT
                TRY_CAST("date" AS DATE)               AS date,
                {geo_raw}                              AS {geo_out},
                TRY_CAST("{_JPI_INDEX}" AS DOUBLE)     AS index
            FROM "{sid}"
            WHERE TRY_CAST("date" AS DATE) IS NOT NULL
        ''',
    )
    for sid, geo_raw, geo_out in _SUBNATIONAL
]
