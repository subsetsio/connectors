"""ITC Open Data Portal connector (IATI aid-transparency data).

Source: https://open.intracen.org/api/v1/itc  (REST, no auth, JSON envelope
{status, data, success}). Corpus is ITC's own development-cooperation project
portfolio (~230 activities, timespan 2014-2029).

Fetch shape: stateless full re-pull (shape 1). The whole corpus is a few MB and
re-pulls in a couple of minutes; there is no incremental/`since` filter (the
`year` param is a slice, not a delta), so every run re-fetches in full and the
transforms overwrite. No state, no watermark.

Five download nodes, each writing flat ndjson tailored to one published table:
  itc-summary               annual aggregate financials (one row per year)
  itc-map                   recipient country/region financials per year
  itc-activities            activity catalog metadata (one row per activity)
  itc-activity-financials   per-activity annual budgets & expenses (long)
  itc-activity-transactions per-activity IATI transactions (long)
The three activity-derived nodes share one paginate+detail crawl helper.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://open.intracen.org/api/v1/itc"
MAX_PAGES = 1000  # safety ceiling; the catalog is ~23 pages today


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    # Unknown paths return a JIRA-styled HTML page at HTTP 200; a real endpoint
    # always carries the {status, data, success} envelope. Validate it.
    assert payload.get("success") is True and "data" in payload, f"bad envelope for {url}"
    return payload["data"]


def _year_range():
    span = _get_json(f"{BASE}/general-info")["timespan"]
    return list(range(int(span["min"]), int(span["max"]) + 1))


def _iter_activity_details():
    """Paginate the activities catalog (follow data.next) and yield the full
    detail document for each activity identifier."""
    url = f"{BASE}/activities"
    pages = 0
    while url:
        if pages >= MAX_PAGES:
            raise RuntimeError(f"activities pagination exceeded {MAX_PAGES} pages — source grew unexpectedly")
        page = _get_json(url)
        for row in page["results"]:
            yield _get_json(f"{BASE}/activities/{row['identifier']}")
        url = page.get("next")
        pages += 1


def fetch_summary(node_id: str) -> None:
    asset = node_id
    rows = []
    for year in _year_range():
        d = _get_json(f"{BASE}/summary", year=year)
        rows.append({
            "year": year,
            "budgets": d.get("budgets"),
            "expenses": d.get("expenses"),
            "funds": d.get("funds"),
            "commitments": d.get("commitments"),
            "activities": d.get("activities"),
            "donors": d.get("donors"),
            "countries": d.get("countries"),
        })
    save_raw_ndjson(rows, asset)


def fetch_map(node_id: str) -> None:
    asset = node_id
    rows = []
    for year in _year_range():
        areas = _get_json(f"{BASE}/map", year=year)
        for code, a in areas.items():
            rows.append({
                "year": year,
                "code": a.get("code") or code,
                "name": a.get("name"),
                "kind": a.get("kind"),
                "region_code": a.get("region_code"),
                "unit_type": a.get("unit_type"),
                "lat": a.get("lat"),
                "lon": a.get("lon"),
                "budgets": a.get("budgets"),
                "expenses": a.get("expenses"),
                "activities": a.get("activities"),
            })
    save_raw_ndjson(rows, asset)


def fetch_activities(node_id: str) -> None:
    asset = node_id
    rows = []
    for d in _iter_activity_details():
        org = d.get("reporting_org") or {}
        bu = d.get("budget_utilisation") or {}
        rows.append({
            "identifier": d.get("identifier"),
            "title": d.get("title"),
            "description": d.get("description"),
            "scope": d.get("scope"),
            "status": d.get("status"),
            "reporting_org_id": org.get("id"),
            "reporting_org_name": org.get("name"),
            "planned_start": d.get("planned_start"),
            "planned_end": d.get("planned_end"),
            "actual_start": d.get("actual_start"),
            "actual_end": d.get("actual_end"),
            "total_budget": bu.get("total_budget"),
            "total_expense": bu.get("total_expense"),
            "date_first_expense": bu.get("date_first_expense"),
            "date_last_expense": bu.get("date_last_expense"),
        })
    save_raw_ndjson(rows, asset)


def fetch_activity_financials(node_id: str) -> None:
    asset = node_id
    rows = []
    for d in _iter_activity_details():
        ident = d.get("identifier")
        budgets = d.get("budgets") or {}
        expenses = d.get("expenses") or {}
        for year in sorted(set(budgets) | set(expenses)):
            rows.append({
                "identifier": ident,
                "year": int(year),
                "budget": budgets.get(year),
                "expense": expenses.get(year),
            })
    save_raw_ndjson(rows, asset)


def fetch_activity_transactions(node_id: str) -> None:
    asset = node_id
    rows = []
    for d in _iter_activity_details():
        ident = d.get("identifier")
        for txn_type, txns in (d.get("all_transactions") or {}).items():
            for t in txns:
                rows.append({
                    "identifier": ident,
                    "transaction_type": txn_type,
                    "date": t.get("date"),
                    "value": t.get("value"),
                    "description": t.get("description"),
                    "organisation_name": t.get("organisation_name"),
                    "organisation_id": t.get("organisation_id"),
                })
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="itc-summary", fn=fetch_summary, kind="download"),
    NodeSpec(id="itc-map", fn=fetch_map, kind="download"),
    NodeSpec(id="itc-activities", fn=fetch_activities, kind="download"),
    NodeSpec(id="itc-activity-financials", fn=fetch_activity_financials, kind="download"),
    NodeSpec(id="itc-activity-transactions", fn=fetch_activity_transactions, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="itc-summary-transform",
        deps=["itc-summary"],
        key=("year",),
        temporal="year",
        sql='''
            SELECT
                CAST(year AS INTEGER)        AS year,
                CAST(budgets AS DOUBLE)      AS budgets,
                CAST(expenses AS DOUBLE)     AS expenses,
                CAST(funds AS DOUBLE)        AS funds,
                CAST(commitments AS DOUBLE)  AS commitments,
                CAST(activities AS INTEGER)  AS activities,
                CAST(donors AS INTEGER)      AS donors,
                CAST(countries AS INTEGER)   AS countries
            FROM "itc-summary"
        ''',
    ),
    SqlNodeSpec(
        id="itc-map-transform",
        deps=["itc-map"],
        key=("year", "code"),
        temporal="year",
        sql='''
            SELECT
                CAST(year AS INTEGER)     AS year,
                code,
                name,
                kind,
                region_code,
                CAST(lat AS DOUBLE)       AS latitude,
                CAST(lon AS DOUBLE)       AS longitude,
                CAST(budgets AS DOUBLE)   AS budgets,
                CAST(expenses AS DOUBLE)  AS expenses,
                CAST(activities AS INTEGER) AS activities
            FROM "itc-map"
            WHERE code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="itc-activities-transform",
        deps=["itc-activities"],
        key=("identifier",),
        temporal="date_first_expense",
        sql='''
            SELECT
                identifier,
                title,
                description,
                scope,
                status,
                reporting_org_name,
                CAST(planned_end AS DATE)        AS planned_end,
                CAST(actual_start AS DATE)       AS actual_start,
                CAST(total_budget AS DOUBLE)     AS total_budget,
                CAST(total_expense AS DOUBLE)    AS total_expense,
                CAST(date_first_expense AS DATE) AS date_first_expense,
                CAST(date_last_expense AS DATE)  AS date_last_expense
            FROM "itc-activities"
            WHERE identifier IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="itc-activity-financials-transform",
        deps=["itc-activity-financials"],
        key=("identifier", "year"),
        temporal="year",
        sql='''
            SELECT
                identifier,
                CAST(year AS INTEGER)   AS year,
                CAST(budget AS DOUBLE)  AS budget,
                CAST(expense AS DOUBLE) AS expense
            FROM "itc-activity-financials"
            WHERE identifier IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="itc-activity-transactions-transform",
        deps=["itc-activity-transactions"],
        key=(),
        temporal="date",
        sql='''
            SELECT
                identifier,
                transaction_type,
                CAST(date AS DATE)            AS date,
                CAST(value AS DOUBLE)         AS value,
                description,
                organisation_name,
                CAST(organisation_id AS BIGINT) AS organisation_id
            FROM "itc-activity-transactions"
            WHERE identifier IS NOT NULL
        ''',
    ),
]
