"""California EDD connector — labor-market statistics published on data.ca.gov.

Mechanism: the statewide CKAN portal (https://data.ca.gov/api/3) under the
organization `california-employment-development-department`. Each rank-active
collect entity is one CKAN package; a package holds one or more CSV resources
(some split by year-range era, e.g. CES 1990-2001 / 2002-2013 / 2014-2026) that
share a single schema.

Fetch shape: stateless full re-pull (shape 1). Each refresh re-fetches every
CSV resource of the package and writes one streamed `ndjson.gz` asset (rows as
JSON objects keyed by the source's CSV headers, string values). The corpus is
low single-digit GB total and re-fetches in minutes, so there is no watermark /
cursor / incremental branch — revisions and late corrections are picked up for
free. NDJSON (not parquet) because column types are left as strings at the raw
layer and typed in the SQL transform, which keeps era-split files concatenating
cleanly regardless of minor drift.

Transform: one SqlNodeSpec per package, a thin parse-and-type pass — rename the
spaced/parenthesised CSV headers to snake_case and TRY_CAST the numeric/date
columns. Numeric casts strip thousands separators before casting.
"""

from __future__ import annotations

import csv
import io
import json


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

BASE = "https://data.ca.gov/api/3"
PREFIX = "california-edd-"

# Entity union — the rank-active CKAN package ids (copied from
# data/sources/california-edd/work/entity_union.json).
from constants import ENTITY_IDS


# --------------------------------------------------------------------------- #
# HTTP with honest retry semantics
# --------------------------------------------------------------------------- #


@transient_retry()
def _api(action: str, **params):
    resp = get(f"{BASE}/action/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN {action} returned success=false: {data.get('error')}")
    return data["result"]


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# Download — one generic fetch per package
# --------------------------------------------------------------------------- #

def _csv_resource_urls(pkg_id: str) -> list[str]:
    """Resolve full-CSV download URLs for a package's CSV resources.

    Prefer the CKAN DataStore dump endpoint on data.ca.gov: it serves the full
    table for any datastore-active resource regardless of where the resource is
    physically hosted (a few EDD resources point at data.edd.ca.gov, a separate
    Socrata host), and it normalises away the UTF-8 BOM some source CSVs carry.
    The dump adds a sequential `_id` column, which the transforms simply ignore.
    Fall back to the resource's own URL only when it isn't datastore-active.
    """
    resources = _api("package_show", id=pkg_id).get("resources", [])
    urls = []
    for r in resources:
        if (r.get("format") or "").strip().upper() != "CSV":
            continue
        if r.get("datastore_active") and r.get("id"):
            urls.append(f"https://data.ca.gov/datastore/dump/{r['id']}")
        elif r.get("url"):
            urls.append(r["url"])
    return urls


def _iter_csv_rows(url: str):
    """Yield one dict per CSV row, keyed by the source header, string values
    (empty strings normalised to None). The whole CSV text is held in memory
    for one resource at a time; output is streamed, so peak memory is bounded
    by the single largest resource."""
    # Some EDD CSVs carry a UTF-8 BOM on the first header (str.strip() does not
    # remove U+FEFF), so drop a leading BOM and normalise it out of every key.
    text = _fetch_text(url).lstrip("﻿")
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        yield {
            k.lstrip("﻿").strip(): (v if v not in ("", None) else None)
            for k, v in row.items()
            if k is not None
        }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pkg_id = node_id[len(PREFIX):]
    urls = _csv_resource_urls(pkg_id)
    if not urls:
        raise RuntimeError(f"{node_id}: package {pkg_id} exposes no CSV resources")

    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for url in urls:
            for row in _iter_csv_rows(url):
                out.write(json.dumps(row, separators=(",", ":")))
                out.write("\n")
                total += 1

    if total == 0:
        raise RuntimeError(f"{node_id}: downloaded 0 rows across {len(urls)} resource(s)")
    print(f"  {node_id}: wrote {total:,} rows from {len(urls)} CSV resource(s)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transform — one typed Delta table per package
# --------------------------------------------------------------------------- #
# Per-package column specs: (kind, source_header, output_alias).
#   txt      -> keep as VARCHAR
#   int      -> TRY_CAST AS INTEGER
#   num      -> strip thousands separators, TRY_CAST AS DOUBLE
#   date_ts  -> TRY_CAST AS TIMESTAMP, then ::DATE
#   date_mdy -> try_strptime '%m/%d/%Y', then ::DATE

_COLUMN_SPECS: dict[str, list[tuple[str, str, str]]] = {
    # Unemployment Insurance Weekly Claims Data for California
    "0dfd4f0b-a3e3-4a66-8e49-ad119ec41564": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Filed week ended", "filed_week_ended"),
        ("num", "Initial Claims", "initial_claims"),
        ("txt", "Reflecting Week Ended", "reflecting_week_ended"),
        ("num", "Continued Claims", "continued_claims"),
        ("num", "Covered Employment", "covered_employment"),
        ("num", "Insured Unemployment Rate", "insured_unemployment_rate"),
    ],
    # Labor Force Participation Rate: US and California
    "1d0bec3e-c865-4c32-ad9d-3bbf1f5d7db6": [
        ("txt", "Date", "date"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("num", "California Labor Force Participation Rate", "ca_lfpr"),
        ("num", "US Labor Force Participation Rate", "us_lfpr"),
    ],
    # Current Employment Statistics (CES)
    "2a5f872d-f7fe-49f2-9581-8f1b17ce5b90": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("date_mdy", "Date", "date"),
        ("txt", "Series Code", "series_code"),
        ("txt", "Industry Title", "industry_title"),
        ("txt", "Seasonally Adjusted (Y/N)", "seasonally_adjusted"),
        ("num", "Current Employment", "current_employment"),
        ("int", "Benchmark", "benchmark"),
    ],
    # Quarterly Census of Employment and Wages (QCEW)
    "3f08b68e-1d1a-4ba4-a07d-1ec3392ed191": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("int", "Year", "year"),
        ("txt", "Quarter", "quarter"),
        ("txt", "Ownership", "ownership"),
        ("txt", "NAICS Level", "naics_level"),
        ("txt", "NAICS Code", "naics_code"),
        ("txt", "Industry Name", "industry_name"),
        ("num", "Establishments", "establishments"),
        ("num", "Average Monthly Employment", "average_monthly_employment"),
        ("num", "1st Month Emp", "first_month_emp"),
        ("num", "2nd Month Emp", "second_month_emp"),
        ("num", "3rd Month Emp", "third_month_emp"),
        ("num", "Total Wages (All Workers)", "total_wages"),
        ("num", "Average Weekly Wages", "average_weekly_wages"),
    ],
    # Paid Family Leave (PFL) - Monthly Data
    "3f530a9c-782f-4f34-bf51-9edaa448e0db": [
        ("txt", "Date", "date"),
        ("txt", "Month", "month"),
        ("int", "Year", "year"),
        ("num", "Total PFL First Claims Filed", "total_first_claims_filed"),
        ("num", "Bonding Claims Filed", "bonding_claims_filed"),
        ("num", "Care Claims Filed", "care_claims_filed"),
        ("num", "Total PFL First Claims Paid", "total_first_claims_paid"),
        ("num", "Bonding Claims Paid", "bonding_claims_paid"),
        ("num", "Care Claims Paid", "care_claims_paid"),
        ("num", "PFL Average Weekly Benefit Amount (AWBA)", "avg_weekly_benefit_amount"),
        ("num", "Weeks Compensated", "weeks_compensated"),
        ("num", "Average Duration", "average_duration"),
        ("num", "Total Benefits Authorized", "total_benefits_authorized"),
    ],
    # Disability Insurance (DI) - Monthly Data
    "4150784a-282a-4862-92bf-c3cf2e8fa722": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Date", "date"),
        ("txt", "Month", "month"),
        ("int", "Year", "year"),
        ("num", "Initial Claims Filed", "initial_claims_filed"),
        ("num", "Initial Claims Paid", "initial_claims_paid"),
        ("num", "Average Weekly Benefit Amount (AWBA)", "avg_weekly_benefit_amount"),
        ("num", "Weeks Compensated", "weeks_compensated"),
        ("num", "Average Duration", "average_duration"),
        ("num", "Total Benefits Authorized", "total_benefits_authorized"),
        ("num", "DI Fund Balance", "di_fund_balance"),
    ],
    # Civilian Unemployment Rate for US and California
    "4275ba49-3a31-4200-852d-faf5b857bb4c": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("date_ts", "Date", "date"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("num", "Seasonally Adjusted", "seasonally_adjusted"),
        ("num", "Not Seasonally Adjusted", "not_seasonally_adjusted"),
    ],
    # Labor Force Participation Rate By Age Groups
    "4362f500-87c8-4842-834a-bbc14fe9a771": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Date", "date"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("num", "Age 16-19", "age_16_19"),
        ("num", "Age 20-24", "age_20_24"),
        ("num", "Age 25-34", "age_25_34"),
        ("num", "Age 35-44", "age_35_44"),
        ("num", "Age 45-54", "age_45_54"),
        ("num", "Age 55-64", "age_55_64"),
        ("num", "Age 65+", "age_65_plus"),
    ],
    # Local Area Unemployment Statistics (LAUS)
    "59218446-5760-4683-b52e-f6210021840a": [
        ("txt", "Area Name", "area_name"),
        ("txt", "Area Type", "area_type"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("txt", "Date_Numeric", "date_numeric"),
        ("txt", "Seasonally Adjusted(Y/N)", "seasonally_adjusted"),
        ("txt", "Status", "status"),
        ("num", "Labor Force", "labor_force"),
        ("num", "Employment", "employment"),
        ("num", "Unemployment", "unemployment"),
        ("num", "Unemployment Rate", "unemployment_rate"),
        ("txt", "Benchmark", "benchmark"),
    ],
    # Occupational Employment and Wage Statistics (OEWS)
    "6411456b-594b-4b73-af57-ce8dd401f2e2": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("int", "Year", "year"),
        ("txt", "Quarter", "quarter"),
        ("txt", "Industry Name", "industry_name"),
        ("txt", "Standard Occupational Classification", "soc_code"),
        ("txt", "Occupational Title", "occupational_title"),
        ("txt", "Wage Type", "wage_type"),
        ("num", "Number of Employed", "number_of_employed"),
        ("num", "Mean Wage", "mean_wage"),
        ("num", "10th Percentile Wage", "pct10_wage"),
        ("num", "25th Percentile Wage", "pct25_wage"),
        ("num", "50th Percentile (Median) Wage", "median_wage"),
        ("num", "75th Percentile Wage", "pct75_wage"),
        ("num", "90th Percentile Wage", "pct90_wage"),
        ("num", "Mean Relative Standard Error for Wage", "mean_rse_wage"),
    ],
    # Long-Term Occupational Employment Projections
    "715d1324-ac02-4b11-b922-86bafa6eb80f": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Period", "period"),
        ("int", "SOC Level", "soc_level"),
        ("txt", "Standard Occupational Classification (SOC)", "soc_code"),
        ("txt", "Occupational Title", "occupational_title"),
        ("num", "Base Year Employment Estimate", "base_year_employment"),
        ("num", "Projected Year Employment Estimate", "projected_year_employment"),
        ("num", "Numeric Change", "numeric_change"),
        ("num", "Percentage Change", "percentage_change"),
        ("num", "Exits", "exits"),
        ("num", "Transfers", "transfers"),
        ("num", "Total Job Openings", "total_job_openings"),
        ("num", "Median Hourly Wage", "median_hourly_wage"),
        ("num", "Median Annual Wage", "median_annual_wage"),
        ("txt", "Entry Level Education", "entry_level_education"),
        ("txt", "Work Experience", "work_experience"),
        ("txt", "Job Training", "job_training"),
    ],
    # Local Area Unemployment Statistics (LAUS), Annual Average
    "74b655ae-6158-41ab-81ef-a02984a17cc1": [
        ("txt", "Area Name", "area_name"),
        ("txt", "Area Type", "area_type"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("txt", "Seasonally Adjusted(Y/N)", "seasonally_adjusted"),
        ("txt", "Status", "status"),
        ("num", "Labor Force", "labor_force"),
        ("num", "Employment", "employment"),
        ("num", "Unemployment", "unemployment"),
        ("num", "Unemployment Rate", "unemployment_rate"),
    ],
    # Unemployment Rate by Age Groups
    "b16c1546-03e1-4bc2-95d2-863f68b54530": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Date", "date"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("num", "Age 16-19", "age_16_19"),
        ("num", "Age 20-24", "age_20_24"),
        ("num", "Age 25-34", "age_25_34"),
        ("num", "Age 35-44", "age_35_44"),
        ("num", "Age 45-54", "age_45_54"),
        ("num", "Age 55-64", "age_55_64"),
        ("num", "Age 65+", "age_65_plus"),
    ],
    # Long-Term Industry Employment Projections
    "b1ac39b1-33cc-4577-b584-6259406ce835": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Period", "period"),
        ("txt", "NAICS Level", "naics_level"),
        ("txt", "NAICS Code", "naics_code"),
        ("txt", "Industry Title", "industry_title"),
        ("num", "Base Year Employment Estimate", "base_year_employment"),
        ("num", "Projected Year Employment Estimate", "projected_year_employment"),
        ("num", "Numeric Change", "numeric_change"),
        ("num", "Percentage Change", "percentage_change"),
    ],
    # Current Employment Statistics (CES), Annual Average
    # (published columns mirror the LAUS labor-force layout)
    "c9416284-cabe-46a3-bdbc-d00ab5ab58f7": [
        ("txt", "Area Name", "area_name"),
        ("txt", "Area Type", "area_type"),
        ("int", "Year", "year"),
        ("txt", "Month", "month"),
        ("txt", "Seasonally Adjusted(Y/N)", "seasonally_adjusted"),
        ("txt", "Status", "status"),
        ("num", "Labor Force", "labor_force"),
        ("num", "Employment", "employment"),
        ("num", "Unemployment", "unemployment"),
        ("num", "Unemployment Rate", "unemployment_rate"),
    ],
    # Unemployment Insurance Program Monthly Claims Data for California
    "f9d2aa1a-5f94-468d-b5ef-26b3b9418694": [
        ("txt", "Area Type", "area_type"),
        ("txt", "Area Name", "area_name"),
        ("txt", "Date", "date"),
        ("num", "Initial Claims", "initial_claims"),
        ("num", "First Payments", "first_payments"),
        ("num", "Weeks Claimed", "weeks_claimed"),
        ("num", "Weeks Compensated", "weeks_compensated"),
        ("num", "Average Weekly Benefit*", "average_weekly_benefit"),
        ("num", "Benefits Paid", "benefits_paid"),
        ("num", "Final Payments", "final_payments"),
    ],
}


def _column_expr(kind: str, col: str, alias: str) -> str:
    if kind == "txt":
        return f'"{col}" AS {alias}'
    if kind == "int":
        return f'TRY_CAST("{col}" AS INTEGER) AS {alias}'
    if kind == "num":
        # Strip currency symbols, thousands separators, %, and stray whitespace
        # (e.g. DI fund balance arrives as '$2,751,911,155.83 '); keep digits,
        # decimal point and sign, then cast.
        return (
            f"TRY_CAST(NULLIF(regexp_replace(CAST(\"{col}\" AS VARCHAR), "
            f"'[^0-9.-]', '', 'g'), '') AS DOUBLE) AS {alias}"
        )
    if kind == "date_ts":
        return f'TRY_CAST("{col}" AS TIMESTAMP)::DATE AS {alias}'
    if kind == "date_mdy":
        return f"try_strptime(\"{col}\", '%m/%d/%Y')::DATE AS {alias}"
    raise ValueError(f"unknown column kind {kind!r}")


def _build_sql(spec_id: str) -> str:
    eid = spec_id[len(PREFIX):]
    cols = _COLUMN_SPECS[eid]
    select = ",\n    ".join(_column_expr(kind, col, alias) for kind, col, alias in cols)
    return f'SELECT\n    {select}\nFROM "{spec_id}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_build_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
