"""FTC bulk CSV datasets — the parametric flat single-table CSV family.

Stateless full re-pull each refresh. Every dataset is a single small CSV
(KB to low-MB) fetched whole; there is no incremental filter on the static
files, so we re-fetch the full corpus every run and overwrite. File slugs are
stable but carry an incrementing numeric suffix on revision (e.g. _2, _3), so we
resolve the current filename from the data-sets landing page at fetch time
rather than hardcoding it.
"""

import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _full_url, _get_bytes, _parse_csv

DATASETS_PAGE = BASE + "/policy-notices/open-government/data-sets"

# entity_id -> stable filename slug prefix on the data-sets page
# (without the version suffix or .csv extension).
DATASET_SLUGS = {
    "ftc_civil_penalty_actions": "ftc_civil_penalty_actions",
    "ftc_merger_enforcement_actions": "ftc_merger_enforcement_actions",
    "ftc_nonmerger_enforcement_actions": "ftc_nonmerger_enforcement_actions",
    "hsr_merger_transactions_by_month": "hsr_merger_transactions_by_month",
    "hsr_transactions_filings_second_requests_by_fy": "hsr_transactions_filings_second_requests_by_fy",
}


def _find_dataset_url(slug_prefix: str) -> str:
    html = _get_bytes(DATASETS_PAGE).decode("utf-8", "replace")
    hrefs = re.findall(r'href="([^"]*attachments/data-sets/[^"]+\.csv)"', html)
    pat = re.compile(rf"/{re.escape(slug_prefix)}(?:_\d+)?\.csv$")
    for h in hrefs:
        if "dictionary" in h:
            continue
        if pat.search(h):
            return _full_url(h)
    raise RuntimeError(f"no data-sets CSV link matching slug {slug_prefix!r}")


def fetch_dataset(node_id: str) -> None:
    """Fetch one flat single-table CSV dataset, resolving the current versioned
    filename from the landing page."""
    asset = node_id
    entity_id = node_id[len("ftc-"):].replace("-", "_")
    slug_prefix = DATASET_SLUGS[entity_id]
    url = _find_dataset_url(slug_prefix)
    rows = _parse_csv(_get_bytes(url))
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 rows from {url}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ftc-ftc-civil-penalty-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-merger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-nonmerger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-merger-transactions-by-month", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-transactions-filings-second-requests-by-fy", fn=fetch_dataset, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ftc-ftc-civil-penalty-actions-transform",
        deps=["ftc-ftc-civil-penalty-actions"],
        sql='''
            SELECT
                TRY_CAST(MatterEnforcementFY AS INTEGER)              AS enforcement_fy,
                TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
                MatterName                                           AS matter_name,
                MatterNumber                                         AS matter_number,
                MatterEnforcementType                                AS enforcement_type,
                MatterType                                           AS matter_type,
                NULLIF(trim(Matterhyperlink, '#'), '')               AS url
            FROM "ftc-ftc-civil-penalty-actions"
            WHERE MatterName IS NOT NULL AND MatterName <> ''
        ''',
    ),
    SqlNodeSpec(
        id="ftc-ftc-merger-enforcement-actions-transform",
        deps=["ftc-ftc-merger-enforcement-actions"],
        sql='''
            SELECT
                TRY_CAST(MatterEnforcementFY AS INTEGER)              AS enforcement_fy,
                TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
                MatterNumber                                         AS matter_number,
                MatterName                                           AS matter_name,
                MatterIndustry                                       AS matter_industry,
                "Matter Enforcement Type"                            AS enforcement_type,
                NULLIF(trim(Matterhyperlink, '#'), '')               AS url
            FROM "ftc-ftc-merger-enforcement-actions"
            WHERE MatterName IS NOT NULL AND MatterName <> ''
        ''',
    ),
    SqlNodeSpec(
        id="ftc-ftc-nonmerger-enforcement-actions-transform",
        deps=["ftc-ftc-nonmerger-enforcement-actions"],
        sql='''
            SELECT
                TRY_CAST(MatterEnforcementFY AS INTEGER)              AS enforcement_fy,
                TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
                MatterNumber                                         AS matter_number,
                MatterName                                           AS matter_name,
                MatterEnforcementType                                AS enforcement_type,
                MatterIndustry                                       AS matter_industry,
                NULLIF(trim(Matterhyperlink, '#'), '')               AS url
            FROM "ftc-ftc-nonmerger-enforcement-actions"
            WHERE MatterName IS NOT NULL AND MatterName <> ''
        ''',
    ),
    SqlNodeSpec(
        id="ftc-hsr-merger-transactions-by-month-transform",
        deps=["ftc-hsr-merger-transactions-by-month"],
        sql='''
            SELECT * FROM (
                SELECT
                    TRY_CAST(FYTransaction AS INTEGER)       AS fiscal_year,
                    TRY_CAST(MonthTransaction AS INTEGER)    AS month,
                    TRY_CAST(TransactionReceived AS INTEGER) AS transactions_received
                FROM "ftc-hsr-merger-transactions-by-month"
            )
            WHERE fiscal_year IS NOT NULL AND transactions_received IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="ftc-hsr-transactions-filings-second-requests-by-fy-transform",
        deps=["ftc-hsr-transactions-filings-second-requests-by-fy"],
        sql='''
            SELECT * FROM (
                SELECT
                    TRY_CAST(FY AS INTEGER)                              AS fiscal_year,
                    TRY_CAST(TransactionsReported AS INTEGER)            AS transactions_reported,
                    TRY_CAST(FilingsReceived AS INTEGER)                 AS filings_received,
                    TRY_CAST(AdjustedTransactions AS INTEGER)            AS adjusted_transactions,
                    TRY_CAST(SecondRequestTotal AS INTEGER)              AS second_request_total,
                    TRY_CAST(SecondRequestFTC AS INTEGER)                AS second_request_ftc,
                    TRY_CAST(SecondRequestPercentFTC AS DOUBLE)          AS second_request_percent_ftc,
                    TRY_CAST(SecondRequestDOJ AS INTEGER)                AS second_request_doj,
                    TRY_CAST(SecondRequestPercentDOJ AS DOUBLE)          AS second_request_percent_doj,
                    TRY_CAST(EarlyTerminationTransactions AS INTEGER)    AS early_termination_transactions,
                    TRY_CAST(EarlyTerminationTransactionsGranted AS INTEGER)    AS early_termination_granted,
                    TRY_CAST(EarlyTerminationTransactionsNotGranted AS INTEGER) AS early_termination_not_granted
                FROM "ftc-hsr-transactions-filings-second-requests-by-fy"
            )
            WHERE fiscal_year IS NOT NULL
        ''',
    ),
]
