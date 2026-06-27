"""Maritime and Port Authority of Singapore (MPA) connector.

MPA publishes its statistics as individual CSV datasets on data.gov.sg. Each is
fetched in full via the CKAN-style datastore_search endpoint keyed by the
data.gov.sg datasetId (= resource_id). This is a catalog connector: one generic
fetch_one() pulls any dataset, and one transform per dataset casts the source's
all-text columns to a typed Delta table.

Fetch shape: STATELESS FULL RE-PULL. Tables are small (tens to ~6k rows), there
is no incremental filter on datastore_search, and full re-pull picks up the
monthly revisions for free. Raw is saved faithfully (source's text values) as
NDJSON; the transform owns typing.
"""

import pyarrow as pa  # noqa: F401  (kept for parity; not required here)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import SCHEMAS, ENTITY_IDS

SLUG = "maritime-and-port-authority-of-singapore"
DATASTORE = "https://data.gov.sg/api/action/datastore_search"
PAGE = 20000  # observed server accepts large limits; biggest table is ~6k rows


def _entity_id(node_id: str) -> str:
    """Recover the data.gov.sg datasetId from the node id.

    Spec ids lower-case the entity id and swap '_' -> '-' (e.g. 'd_da03...'
    -> 'd-da03...'); datasetIds have exactly one underscore (the 'd_' prefix),
    so restoring it is unambiguous.
    """
    suffix = node_id[len(SLUG) + 1:]          # strip 'maritime-..-singapore-'
    return "d_" + suffix[len("d-"):]          # 'd-xxxx' -> 'd_xxxx'


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> dict:
    resp = get(
        DATASTORE,
        params={"resource_id": resource_id, "limit": PAGE, "offset": offset},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"datastore_search returned success=false for {resource_id}")
    return body["result"]


def fetch_one(node_id: str) -> None:
    asset = node_id
    resource_id = _entity_id(node_id)

    rows = []
    offset = 0
    total = None
    while True:
        result = _fetch_page(resource_id, offset)
        if total is None:
            total = result.get("total", 0)
        batch = result.get("records", [])
        if not batch:
            break
        for rec in batch:
            rec.pop("_id", None)  # drop the synthetic datastore row id
            rows.append(rec)
        offset += len(batch)
        if offset >= total:
            break

    if not rows:
        raise RuntimeError(f"{asset}: datastore_search returned 0 rows for {resource_id}")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(view: str, schema: dict) -> str:
    period = schema["period"]
    select = []
    if period == "year":
        select.append('CAST(NULLIF(TRIM(CAST("year" AS VARCHAR)), \'\') AS INTEGER) AS "year"')
    else:  # month: keep the source 'YYYY-MM' text, verified non-empty
        select.append('TRIM(CAST("month" AS VARCHAR)) AS "month"')
    for col in schema["categories"]:
        select.append(f'CAST("{col}" AS VARCHAR) AS "{col}"')
    for col in schema["values"]:
        select.append(f'CAST(NULLIF(TRIM(CAST("{col}" AS VARCHAR)), \'\') AS DOUBLE) AS "{col}"')
    cols = ",\n            ".join(select)
    return (
        f"SELECT\n            {cols}\n"
        f'        FROM "{view}"\n'
        f'        WHERE NULLIF(TRIM(CAST("{period}" AS VARCHAR)), \'\') IS NOT NULL'
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_transform_sql(spec.id, SCHEMAS[_entity_id(spec.id)]),
    )
    for spec in DOWNLOAD_SPECS
]
