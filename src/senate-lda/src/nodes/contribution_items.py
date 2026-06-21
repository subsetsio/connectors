"""Individual contributions exploded from each LD-203 report.

Re-crawls /contributions/ (windowed by dt_posted month), one row per item.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_dated


def _explode_items(c: dict) -> list[dict]:
    out = []
    for it in (c.get("contribution_items") or []):
        out.append({
            "filing_uuid": c.get("filing_uuid"),
            "filing_year": c.get("filing_year"),
            "contribution_type": it.get("contribution_type"),
            "contribution_type_display": it.get("contribution_type_display"),
            "contributor_name": it.get("contributor_name"),
            "payee_name": it.get("payee_name"),
            "honoree_name": it.get("honoree_name"),
            "amount": it.get("amount"),
            "contribution_date": it.get("date"),
        })
    return out


def fetch_contribution_items(node_id: str) -> None:
    _crawl_dated(node_id, "contributions", _explode_items)


NODE_SPECS = [
    NodeSpec(id="senate-lda-contribution-items", fn=fetch_contribution_items, kind="download"),
    SqlNodeSpec(
        id="senate-lda-contribution-items-transform",
        deps=["senate-lda-contribution-items"],
        sql='''
            SELECT
                filing_uuid,
                CAST(filing_year AS INTEGER)            AS filing_year,
                contribution_type,
                contribution_type_display,
                contributor_name,
                payee_name,
                honoree_name,
                TRY_CAST(amount AS DOUBLE)              AS amount,
                TRY_CAST(contribution_date AS DATE)     AS contribution_date
            FROM "senate-lda-contribution-items"
            WHERE filing_uuid IS NOT NULL
        ''',
    ),
]
