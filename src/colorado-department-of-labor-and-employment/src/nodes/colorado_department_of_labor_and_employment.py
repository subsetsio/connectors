"""Colorado Department of Labor and Employment (CDLE) connector.

Source: the Colorado Information Marketplace (data.colorado.gov), a standard
Socrata open-data portal. We publish the CDLE-attributed labor-market tables
(unemployment, wages, employment counts, hours, income, CPI, projections).

Shape: stateless full re-pull. Each table is a single flat Socrata resource of
modest size (a few thousand to ~330k rows); we page the SODA 2.1 JSON endpoint
in full every refresh and overwrite. No watermark/cursor — revisions and late
corrections are picked up for free.

SODA returns every value as a JSON string and OMITS null fields per row, so the
key set drifts row-to-row within one dataset (a sparse column appears only on
the rows that have it). We therefore normalize each dataset to the union of its
keys and write parquet with an explicit all-string schema — a stable contract
that the transform can SELECT * cleanly. (Writing raw NDJSON instead lets
DuckDB's JSON reader infer the schema from a sample and then fail on a later row
carrying a key the sample never saw.)
"""

import json

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
from constants import ENTITY_IDS

SLUG = "colorado-department-of-labor-and-employment"
RESOURCE_URL = "https://data.colorado.gov/resource/{rid}.json"
PAGE_SIZE = 50000
# Safety ceiling: largest CDLE table seen is ~330k rows. If we ever page past
# this many rows the source has grown unexpectedly (or pagination is looping) —
# raise rather than silently truncate.
MAX_PAGES_ABS = 200


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _fetch_page(rid: str, offset: int) -> list:
    resp = get(
        RESOURCE_URL.format(rid=rid),
        params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _resource_id(node_id: str) -> str:
    """Recover the Socrata 4x4 id from the spec id (strip the slug prefix)."""
    return node_id[len(SLUG) + 1:]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rid = _resource_id(node_id)

    rows = []
    offset = 0
    for page_no in range(MAX_PAGES_ABS + 1):
        page = _fetch_page(rid, offset)
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break  # short page = last page
        offset += PAGE_SIZE
    else:
        raise RuntimeError(
            f"{asset}: exceeded MAX_PAGES_ABS={MAX_PAGES_ABS} pages "
            f"(>{MAX_PAGES_ABS * PAGE_SIZE} rows) for resource {rid} — "
            f"source grew unexpectedly or pagination is looping"
        )

    # All values are JSON strings; columns differ per dataset → NDJSON.
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. SODA delivers every column as a string
# and each of the nine resources has its own column list, so the transform is a
# straight pass-through view — typing and reshaping happen in the downstream
# platform. A SELECT * that returns 0 rows fails the node (the correctness gate).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
