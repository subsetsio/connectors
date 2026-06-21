"""Ministry of Finance (India) — Open Government Data (OGD) Platform connector.

Mechanism: the data.gov.in REST API (api.data.gov.in). Each rank-accepted
resource is one small tabular dataset with its OWN column schema, fetched from
`/resource/{resource_id}`. Because the per-resource schemas are heterogeneous
(every table has different columns, and values arrive as a mix of numbers and
strings), raw is written as NDJSON and the transform is a thin `SELECT *`
pass that republishes the source table verbatim — one published Delta table per
resource.

Fetch shape: stateless full re-pull (shape 1). Each resource is a handful to a
few hundred rows; we re-fetch the whole table every run and overwrite. No
watermark/cursor — revisions are picked up for free.

Pagination gotcha: the `/resource` endpoint caps each response at a small page
(10 rows with the shared public key) regardless of the requested `limit`, but
`offset` paging works and `total` is pinned on every response. We page by
offset using the ACTUAL returned count until we have collected `total` rows.

Auth/UA gotcha: api.data.gov.in silently STALLS the default urllib/httpx
User-Agent (the connection hangs until timeout); we send an explicit ASCII
browser-style User-Agent and it responds instantly. The `api-key` query param
is required — a registered key may be supplied via DATA_GOV_IN_API_KEY, else we
fall back to the documented public sample key.
"""

import os

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    is_transient,
    save_raw_ndjson,
)
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from constants import ENTITY_IDS

SLUG = "ministry-of-finance"
BASE = "https://api.data.gov.in"
SAMPLE_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
# Explicit ASCII User-Agent — the server hangs on the default urllib/httpx UA.
USER_AGENT = "Mozilla/5.0 (compatible; subsets-bot/1.0)"
# Requested page size. A registered key honors large pages (whole table in one
# request); the shared public sample key silently caps each response at ~10 rows
# regardless. We request the max and adapt to whatever the server returns, so a
# registered key collapses a 400-row resource from ~40 requests to 1 — which is
# what keeps us under the rate budget at 46x concurrency.
PAGE = 1000
MAX_PAGES = 100_000  # safety ceiling; raises rather than looping forever.


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or SAMPLE_KEY


# All 46 download specs run as concurrent subprocesses hitting the same host
# with the same (shared, throttled) key, so 429s are common. The standard
# jitter-free `wait_exponential` makes every process back off in lockstep and
# collide on the same retry instants; full-jitter `wait_random_exponential`
# desynchronizes the herd, and the extra attempts give the throttle time to
# clear. Same `is_transient` classification as `transient_retry` (retries
# 429/5xx/transport), just a herd-friendly wait policy.
_rate_aware_retry = retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(12),
    wait=wait_random_exponential(multiplier=2, max=240),
    reraise=True,
)


@_rate_aware_retry
def _fetch_page(resource_id: str, offset: int) -> dict:
    resp = get(
        f"{BASE}/resource/{resource_id}",
        params={
            "api-key": _api_key(),
            "format": "json",
            "limit": PAGE,
            "offset": offset,
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _entity_id(node_id: str) -> str:
    return node_id[len(SLUG) + 1 :]  # strip "ministry-of-finance-"


def fetch_one(node_id: str) -> None:
    asset = node_id
    configure_http(headers={"User-Agent": USER_AGENT})  # ASCII-only UA.
    resource_id = _entity_id(node_id)

    rows: list[dict] = []
    offset = 0
    total = None
    for _ in range(MAX_PAGES):
        payload = _fetch_page(resource_id, offset)
        if isinstance(payload, dict) and payload.get("error"):
            raise RuntimeError(f"{asset}: API error for {resource_id}: {payload['error']}")
        if total is None:
            total = int(payload.get("total") or 0)
        page = payload.get("records") or []
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        if total and len(rows) >= total:
            break
    else:
        raise RuntimeError(f"{asset}: exceeded MAX_PAGES paging {resource_id} (total={total})")

    # Every row carries the resource id so the published table is self-describing
    # and joinable back to the catalog.
    for r in rows:
        r["resource_id"] = resource_id

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per resource. Schemas are heterogeneous, so each
# transform is a thin verbatim republish of its single source table.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
