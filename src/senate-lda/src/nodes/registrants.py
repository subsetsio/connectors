"""Directory of registered lobbying firms.

Page-resumed full crawl of /registrants/ ordered by id ascending.
"""

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _crawl_paged


def _flat_registrant(r: dict) -> dict:
    return {k: r.get(k) for k in (
        "id", "house_registrant_id", "name", "description", "city", "state",
        "state_display", "country", "country_display", "ppb_country",
        "contact_name", "dt_updated",
    )}


def fetch_registrants(node_id: str) -> None:
    _crawl_paged(node_id, "registrants", _flat_registrant)


NODE_SPECS = [
    NodeSpec(id="senate-lda-registrants", fn=fetch_registrants, kind="download"),
    SqlNodeSpec(
        id="senate-lda-registrants-transform",
        deps=["senate-lda-registrants"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                  AS id,
                CAST(house_registrant_id AS BIGINT) AS house_registrant_id,
                name,
                description,
                city,
                state,
                state_display,
                country,
                country_display,
                ppb_country,
                contact_name,
                TRY_CAST(dt_updated AS TIMESTAMPTZ) AS dt_updated
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY id ORDER BY dt_updated DESC
                ) AS _rn
                FROM "senate-lda-registrants"
                WHERE id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
