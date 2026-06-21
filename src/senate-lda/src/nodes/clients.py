"""Directory of clients represented.

Page-resumed full crawl of /clients/ ordered by id ascending.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_paged


def _flat_client(c: dict) -> dict:
    reg = c.get("registrant") or {}
    d = {k: c.get(k) for k in (
        "id", "client_id", "name", "general_description", "state",
        "state_display", "country", "country_display", "ppb_state",
        "ppb_country", "effective_date", "client_self_select",
    )}
    d["registrant_id"] = reg.get("id")
    d["registrant_name"] = reg.get("name")
    return d


def fetch_clients(node_id: str) -> None:
    _crawl_paged(node_id, "clients", _flat_client)


NODE_SPECS = [
    NodeSpec(id="senate-lda-clients", fn=fetch_clients, kind="download"),
    SqlNodeSpec(
        id="senate-lda-clients-transform",
        deps=["senate-lda-clients"],
        sql='''
            SELECT
                CAST(id AS BIGINT)        AS id,
                CAST(client_id AS BIGINT) AS client_id,
                name,
                general_description,
                state,
                state_display,
                country,
                country_display,
                ppb_state,
                ppb_country,
                TRY_CAST(effective_date AS DATE) AS effective_date,
                client_self_select,
                CAST(registrant_id AS BIGINT) AS registrant_id,
                registrant_name
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY id ORDER BY effective_date DESC
                ) AS _rn
                FROM "senate-lda-clients"
                WHERE id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
