"""US BJS / NCVS (NACJD) connector.

Source: BJS "NCVS Select" datasets via the SODA2 (Socrata) API at
https://api.ojp.gov/bjsdataset/v1/. Four stable resources, each a concatenated
1993-present longitudinal microdata table (one row per person / household /
victimization with survey weights).

Strategy: stateless full re-pull (shape 1). Each refresh pages the entire
resource via $limit/$offset and overwrites. Raw is stored as all-string parquet
(JSON delivers every value as a string; we preserve codes and sentinels like
-1/-2 verbatim) and the transform SQL casts to typed columns. No incremental
query — the source publishes one new collection year each fall; a full re-pull
picks up revisions for free.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import RESOURCE_COLUMNS, ENTITY_IDS, ID_COLUMNS, DOUBLE_COLUMNS

BASE = "https://api.ojp.gov/bjsdataset/v1"
PAGE_SIZE = 50000


def _resource_id(node_id: str) -> str:
    """Recover the SODA2 resource id from the spec id (strip 'bjs-ncvs-')."""
    return node_id[len("bjs-ncvs-"):]


@transient_retry()
def _count(resource_id: str) -> int:
    resp = get(
        f"{BASE}/{resource_id}.json",
        params={"$select": "count(*)"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return int(resp.json()[0]["count"])


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> list:
    resp = get(
        f"{BASE}/{resource_id}.json",
        params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id
    resource_id = _resource_id(node_id)
    columns = RESOURCE_COLUMNS[resource_id]
    schema = pa.schema([(c, pa.string()) for c in columns])

    total = _count(resource_id)
    # Safety ceiling: detect runaway pagination / unexpected source growth and
    # raise rather than silently spin or truncate.
    max_pages = total // PAGE_SIZE + 10

    written = 0
    with raw_parquet_writer(asset, schema) as writer:
        offset = 0
        pages = 0
        while True:
            if pages > max_pages:
                raise RuntimeError(
                    f"{asset}: exceeded safety cap of {max_pages} pages "
                    f"(total={total}); source may have grown unexpectedly"
                )
            rows = _fetch_page(resource_id, offset)
            if not rows:
                break
            data = {c: [r.get(c) for r in rows] for c in columns}
            writer.write_table(pa.Table.from_pydict(data, schema=schema))
            written += len(rows)
            offset += PAGE_SIZE
            pages += 1
            if len(rows) < PAGE_SIZE:
                break

    # The full table should match the count() taken at the start of the run.
    # Allow for late-arriving rows during paging, but a large shortfall means
    # pagination broke.
    if written < total:
        raise RuntimeError(
            f"{asset}: wrote {written} rows but count() reported {total}"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bjs-ncvs-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _cast(col: str) -> str:
    if col in ID_COLUMNS:
        return f'"{col}"'  # keep identifiers as VARCHAR (28-digit ids)
    if col in DOUBLE_COLUMNS:
        return f'CAST("{col}" AS DOUBLE) AS "{col}"'
    if col == "year":
        return f'CAST("{col}" AS INTEGER) AS "{col}"'
    return f'CAST("{col}" AS INTEGER) AS "{col}"'  # integer survey codes


def _transform_sql(spec_id: str, resource_id: str) -> str:
    cols = RESOURCE_COLUMNS[resource_id]
    projection = ",\n    ".join(_cast(c) for c in cols)
    return f'SELECT\n    {projection}\nFROM "{spec_id}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id, _resource_id(s.id)),
    )
    for s in DOWNLOAD_SPECS
]
