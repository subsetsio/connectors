"""Issue-area lobbying activities exploded from each /filings/ record.

Re-crawls /filings/ (windowed by dt_posted month), one row per activity.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_dated, _name


def _explode_activities(f: dict) -> list[dict]:
    reg = f.get("registrant") or {}
    cl = f.get("client") or {}
    out = []
    for a in (f.get("lobbying_activities") or []):
        names = [n for n in (_name(e.get("lobbyist") or {}) for e in (a.get("lobbyists") or [])) if n]
        govs = [g.get("name") for g in (a.get("government_entities") or []) if g.get("name")]
        out.append({
            "filing_uuid": f.get("filing_uuid"),
            "filing_year": f.get("filing_year"),
            "registrant_name": reg.get("name"),
            "client_name": cl.get("name"),
            "issue_code": a.get("general_issue_code"),
            "issue_area": a.get("general_issue_code_display"),
            "description": a.get("description"),
            "lobbyist_names": names or None,
            "government_entities": govs or None,
        })
    return out


def fetch_lobbying_activities(node_id: str) -> None:
    _crawl_dated(node_id, "filings", _explode_activities)


NODE_SPECS = [
    NodeSpec(id="senate-lda-lobbying-activities", fn=fetch_lobbying_activities, kind="download"),
    SqlNodeSpec(
        id="senate-lda-lobbying-activities-transform",
        deps=["senate-lda-lobbying-activities"],
        sql='''
            SELECT DISTINCT
                filing_uuid,
                CAST(filing_year AS INTEGER) AS filing_year,
                registrant_name,
                client_name,
                issue_code,
                issue_area,
                description,
                lobbyist_names,
                government_entities
            FROM "senate-lda-lobbying-activities"
            WHERE filing_uuid IS NOT NULL AND issue_code IS NOT NULL
        ''',
    ),
]
