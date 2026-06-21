"""LD-203 political-contribution reports (one row per report).

Stateful crawl of /contributions/ windowed by dt_posted month.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_dated, _name


def _flat_contribution(c: dict) -> list[dict]:
    reg = c.get("registrant") or {}
    lob = c.get("lobbyist") or {}
    return [{
        "filing_uuid": c.get("filing_uuid"),
        "filing_year": c.get("filing_year"),
        "filing_type": c.get("filing_type"),
        "filing_type_display": c.get("filing_type_display"),
        "filing_period": c.get("filing_period"),
        "dt_posted": c.get("dt_posted"),
        "filer_type": c.get("filer_type"),
        "filer_type_display": c.get("filer_type_display"),
        "contact_name": c.get("contact_name"),
        "state": c.get("state"),
        "country": c.get("country"),
        "no_contributions": c.get("no_contributions"),
        "registrant_id": reg.get("id"),
        "registrant_name": reg.get("name"),
        "lobbyist_id": lob.get("id"),
        "lobbyist_name": _name(lob),
    }]


def fetch_contributions(node_id: str) -> None:
    _crawl_dated(node_id, "contributions", _flat_contribution)


NODE_SPECS = [
    NodeSpec(id="senate-lda-contributions", fn=fetch_contributions, kind="download"),
    SqlNodeSpec(
        id="senate-lda-contributions-transform",
        deps=["senate-lda-contributions"],
        sql='''
            SELECT
                filing_uuid,
                CAST(filing_year AS INTEGER)        AS filing_year,
                filing_type,
                filing_type_display,
                filing_period,
                TRY_CAST(dt_posted AS TIMESTAMPTZ)  AS dt_posted,
                TRY_CAST(dt_posted AS DATE)             AS posted_date,
                filer_type,
                filer_type_display,
                contact_name,
                state,
                country,
                no_contributions,
                CAST(registrant_id AS BIGINT)       AS registrant_id,
                registrant_name,
                CAST(lobbyist_id AS BIGINT)         AS lobbyist_id,
                lobbyist_name
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY filing_uuid ORDER BY dt_posted DESC
                ) AS _rn
                FROM "senate-lda-contributions"
                WHERE filing_uuid IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
