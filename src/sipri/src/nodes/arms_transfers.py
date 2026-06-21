"""SIPRI arms transfers — REST register from the public arms-transfers backend
(atbackend.sipri.org/api/p), paginated, saved as NDJSON (several optional fields
drift). Stateless full re-pull: the corpus is small and SIPRI revises prior years
on every annual release, so there is no usable incremental filter.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, post, save_raw_ndjson, transient_retry

AT_BASE = "https://atbackend.sipri.org/api/p"
AT_PAGE_SIZE = 10000          # verified working; server caps above this
AT_MAX_PAGES = 50             # safety ceiling (~30k rows / 10k = 3 pages today)


@transient_retry()
def _post_json(path: str, body: dict):
    resp = post(AT_BASE + path, json=body, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_arms_transfers(node_id: str) -> None:
    asset = node_id
    rows = []
    # pageNo is 0-indexed on this backend (page 0 is the first page).
    for page in range(0, AT_MAX_PAGES):
        batch = _post_json(
            "/trades/search",
            {"filters": [], "logic": "and", "pageNo": page, "pageSize": AT_PAGE_SIZE, "sorts": {}},
        )
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < AT_PAGE_SIZE:
            break
    else:
        raise RuntimeError(f"arms-transfers pagination hit safety cap of {AT_MAX_PAGES} pages")
    if not rows:
        raise RuntimeError("arms-transfers search returned 0 rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sipri-arms-transfers", fn=fetch_arms_transfers, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sipri-arms-transfers-transform",
        deps=["sipri-arms-transfers"],
        sql='''
            SELECT
                CAST("id" AS BIGINT)        AS id,
                CAST("tradeId" AS BIGINT)   AS trade_id,
                "buyer"                     AS buyer,
                "seller"                    AS seller,
                "category"                  AS category,
                "subCategory"               AS sub_category,
                "desg"                      AS weapon_designation,
                "desc"                      AS weapon_description,
                CAST("orderYr" AS INTEGER)  AS order_year,
                CAST("deliveryYr" AS INTEGER) AS delivery_year,
                CAST("units" AS DOUBLE)     AS units,
                "status"                    AS status,
                "transferType"              AS transfer_type,
                CAST("orderYrEst" AS BOOLEAN)  AS order_year_estimated,
                CAST("unitsEst" AS BOOLEAN)    AS units_estimated,
                CAST("statusEst" AS BOOLEAN)   AS status_estimated
            FROM "sipri-arms-transfers"
            WHERE "id" IS NOT NULL
        ''',
    ),
]
