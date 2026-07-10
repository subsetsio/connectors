"""U.S. Treasury Fiscal Data connector.

Source: one public, unauthenticated REST API
(https://api.fiscaldata.treasury.gov/services/api/fiscal_service/) exposing a
single endpoint per database table. Each accepted collect entity maps 1:1 to one
such endpoint; `constants.ENDPOINTS` carries the path (the v1/v2 prefix is part
of the stable path and must be preserved).

Fetch shape: stateless full re-pull. The API does expose an incremental filter
(`filter=record_date:gte:YYYY-MM-DD`), but the whole accepted corpus is ~18M rows
across 171 tables, every table is republished in full, and Treasury restates
history routinely (the Financial Report tables and the MTS are revised for months
after first release). Re-pulling each table whole means revisions land for free
and no watermark can silently skip a restated row.

Pacing: the API documents no rate limit but enforces an undocumented IP-level
block — probing at 8-way concurrency (~3 req/s) made the server accept the TLS
handshake and then close every connection with no HTTP response, for all
endpoints at once, for well over ten minutes. Two defences: the DAG runs nodes
sequentially and each page carries a short courtesy delay, keeping us near
0.1 req/s; and an empty reply arrives as httpx.RemoteProtocolError, which
`transient_retry` classifies as transient, so a block is waited out rather than
mistaken for a dead endpoint. The backoff here is widened (8 attempts, up to
300s apart) to span a block that outlives the default policy.

Raw format: NDJSON. The 171 endpoints have 171 distinct schemas and the API
returns every value as a string, including the literal string "null" for missing
values, so a per-table parquet schema buys nothing here. NDJSON stores the
records faithfully and the model stage types them from the profiled raw.

The one exception is `v2/debt/tror`, at ~230 fields the only endpoint wider than
DuckDB's `map_inference_threshold` (200). Every reader in the stack opens NDJSON
with a bare `read_json_auto`, which silently infers one `MAP(VARCHAR, VARCHAR)`
column instead of 230 struct fields, so the table profiles, tests and transforms
all see a single opaque column. Parquet carries the schema explicitly and is
read back by name.
"""

import time

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
    transient_retry,
)

from constants import ENDPOINTS, ENTITY_IDS

# Wider than DuckDB's map_inference_threshold — see the module docstring.
PARQUET_ENTITY_IDS = {"v2-debt-tror"}

BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
SLUG_PREFIX = "us-treasury-fiscal-data-"

PAGE_SIZE = 10000  # the API's documented maximum
PAGE_DELAY_S = 0.5
# Safety ceiling, not a budget: the largest accepted table is ~3.5M rows (347
# pages). 800 pages = 8M rows, so this fires only if a table grows past twice
# anything Treasury publishes today.
MAX_PAGES = 800

# A crawl that returns less than this fraction of the row count the API itself
# advertised on page 1 has lost data to a truncated page walk. Silent partial
# loads are worse than a failed node, so it raises.
MIN_COMPLETENESS = 0.9


@transient_retry(attempts=8, min_wait=5, max_wait=300)
def _fetch_page(endpoint: str, page: int) -> dict:
    resp = get(
        BASE_URL + endpoint,
        params={"page[number]": page, "page[size]": PAGE_SIZE},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def _iter_table(endpoint: str, stats: dict):
    """Yield every row of one table, paging until the server says we are done.

    `stats` is filled in as we go so the caller can reconcile what we shipped
    against the total-count the API advertised on the first page.
    """
    page = 1
    while True:
        if page > MAX_PAGES:
            raise RuntimeError(
                f"{endpoint}: exceeded MAX_PAGES={MAX_PAGES} at page[size]={PAGE_SIZE} - "
                "the table grew past twice its expected size; raise the cap deliberately."
            )
        payload = _fetch_page(endpoint, page)
        meta = payload.get("meta") or {}
        batch = payload.get("data") or []
        if page == 1:
            stats["total_count"] = meta.get("total-count")

        stats["rows"] += len(batch)
        yield from batch

        total_pages = meta.get("total-pages")
        if total_pages is not None:
            if page >= total_pages:
                return
        elif len(batch) < PAGE_SIZE:
            return
        page += 1
        time.sleep(PAGE_DELAY_S)


def _assert_complete(asset: str, endpoint: str, stats: dict) -> None:
    expected = stats["total_count"]
    if expected and stats["rows"] < expected * MIN_COMPLETENESS:
        raise RuntimeError(
            f"{asset}: shipped {stats['rows']} of the {expected} rows the API advertised "
            f"for {endpoint} (< {MIN_COMPLETENESS:.0%}) - the page walk truncated."
        )


def fetch_one(node_id: str) -> None:
    """Page one Fiscal Data table in full and overwrite its raw NDJSON.

    The runtime passes the spec id, which is also the asset name; the collect
    entity is recovered from it by stripping the connector prefix.
    """
    asset = node_id
    endpoint = ENDPOINTS[node_id.removeprefix(SLUG_PREFIX)]

    stats = {"rows": 0, "total_count": None}
    save_raw_ndjson(_iter_table(endpoint, stats), asset)
    _assert_complete(asset, endpoint, stats)


def fetch_wide(node_id: str) -> None:
    """Same walk as `fetch_one`, landed as Parquet (see the module docstring).

    Every field stays a string, exactly as the API and the NDJSON assets carry
    it; only the schema becomes explicit. Column order follows first appearance,
    and a field absent from a row lands null.
    """
    asset = node_id
    endpoint = ENDPOINTS[node_id.removeprefix(SLUG_PREFIX)]

    stats = {"rows": 0, "total_count": None}
    rows = list(_iter_table(endpoint, stats))
    _assert_complete(asset, endpoint, stats)

    fields = list(dict.fromkeys(k for row in rows for k in row))
    table = pa.table(
        {f: pa.array([row.get(f) for row in rows], type=pa.string()) for f in fields}
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG_PREFIX}{eid}",
        fn=fetch_wide if eid in PARQUET_ENTITY_IDS else fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
