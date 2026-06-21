"""LD-1/LD-2 lobbying disclosure filings (one row per filing).

Stateful crawl of /filings/ windowed by dt_posted month.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_dated


def _flat_filing(f: dict) -> list[dict]:
    reg = f.get("registrant") or {}
    cl = f.get("client") or {}
    return [{
        "filing_uuid": f.get("filing_uuid"),
        "filing_year": f.get("filing_year"),
        "filing_type": f.get("filing_type"),
        "filing_type_display": f.get("filing_type_display"),
        "filing_period": f.get("filing_period"),
        "filing_period_display": f.get("filing_period_display"),
        "income": f.get("income"),
        "expenses": f.get("expenses"),
        "dt_posted": f.get("dt_posted"),
        "termination_date": f.get("termination_date"),
        "filing_document_url": f.get("filing_document_url"),
        "registrant_id": reg.get("id"),
        "registrant_name": reg.get("name"),
        "registrant_state": reg.get("state"),
        "registrant_country": reg.get("country"),
        "client_id": cl.get("id"),
        "client_name": cl.get("name"),
        "client_state": cl.get("state"),
        "client_country": cl.get("country"),
    }]


def fetch_filings(node_id: str) -> None:
    _crawl_dated(node_id, "filings", _flat_filing)


NODE_SPECS = [
    NodeSpec(id="senate-lda-filings", fn=fetch_filings, kind="download"),
    SqlNodeSpec(
        id="senate-lda-filings-transform",
        deps=["senate-lda-filings"],
        sql='''
            SELECT
                filing_uuid,
                CAST(filing_year AS INTEGER)        AS filing_year,
                filing_type,
                filing_type_display,
                filing_period,
                filing_period_display,
                TRY_CAST(income AS DOUBLE)          AS income,
                TRY_CAST(expenses AS DOUBLE)        AS expenses,
                TRY_CAST(dt_posted AS TIMESTAMPTZ)  AS dt_posted,
                TRY_CAST(dt_posted AS DATE)             AS posted_date,
                CAST(registrant_id AS BIGINT)       AS registrant_id,
                registrant_name,
                registrant_state,
                registrant_country,
                CAST(client_id AS BIGINT)           AS client_id,
                client_name,
                client_state,
                client_country,
                filing_document_url
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY filing_uuid ORDER BY dt_posted DESC
                ) AS _rn
                FROM "senate-lda-filings"
                WHERE filing_uuid IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
