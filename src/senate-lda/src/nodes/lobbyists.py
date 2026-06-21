"""Directory of individual lobbyists.

Page-resumed full crawl of /lobbyists/ ordered by id ascending.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_paged


def _flat_lobbyist(lo: dict) -> dict:
    reg = lo.get("registrant") or {}
    d = {k: lo.get(k) for k in (
        "id", "prefix_display", "first_name", "nickname", "middle_name",
        "last_name", "suffix_display",
    )}
    d["registrant_id"] = reg.get("id")
    d["registrant_name"] = reg.get("name")
    return d


def fetch_lobbyists(node_id: str) -> None:
    _crawl_paged(node_id, "lobbyists", _flat_lobbyist)


NODE_SPECS = [
    NodeSpec(id="senate-lda-lobbyists", fn=fetch_lobbyists, kind="download"),
    SqlNodeSpec(
        id="senate-lda-lobbyists-transform",
        deps=["senate-lda-lobbyists"],
        sql='''
            SELECT
                CAST(id AS BIGINT)            AS id,
                prefix_display,
                first_name,
                nickname,
                middle_name,
                last_name,
                suffix_display,
                CAST(registrant_id AS BIGINT) AS registrant_id,
                registrant_name
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY id, registrant_id ORDER BY id
                ) AS _rn
                FROM "senate-lda-lobbyists"
                WHERE id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
