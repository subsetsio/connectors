"""India Ministry of Commerce — data.gov.in (OGD Platform) catalog connector.

Mechanism `datagovin_resource`: one stable resource_id per dataset on the Open
Government Data Platform, fetched via the REST `resource` endpoint:

    https://api.data.gov.in/resource/{resource_id}?api-key=KEY&format=json&offset=&limit=

Each rank-accepted resource (org 'Ministry of Commerce and Industry') is one
heterogeneous tabular dataset with its own flat, typed column schema (records are
keyed by the field `id`). Because schemas differ across resources, raw is written
as NDJSON and the transform is a thin `SELECT *` that publishes the table as-is.

Fetch shape: stateless full re-pull (shape 1). Resources are small-to-medium
administrative/statistical tables (low tens of thousands of rows at most); we
re-fetch the whole resource each run and overwrite. The data endpoint exposes no
incremental filter (research `download_handoff`), so a watermark would buy
nothing.

Auth: `api-key` is a QUERY parameter (not a header). A registered key is read from
DATA_GOV_IN_API_KEY when present; otherwise the public sample key published by
data.gov.in is used. The API 429s/times out under heavy concurrency but is fine
sequentially — the DAG runs downloads sequentially and `transient_retry` backs
off on 429/5xx.
"""

import os

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS

SLUG = "india-ministry-of-commerce"
_PREFIX = f"{SLUG}-"
_BASE = "https://api.data.gov.in/resource/"
_SAMPLE_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
_PAGE = 1000
# Safety ceiling on request count. The data endpoint advances by however many
# records the server actually returns per call (a registered DATA_GOV_IN_API_KEY
# honours limit=1000; the public sample key silently caps at 10/call), so this
# bounds runaway loops, not a fixed row total. ~5M rows at 1000/call.
_MAX_PAGES = 5000


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or _SAMPLE_KEY


@transient_retry()  # 6 attempts, exp backoff — handles 429/5xx/transient network
def _fetch_page(resource_id: str, offset: int) -> dict:
    resp = get(
        _BASE + resource_id,
        params={
            "api-key": _api_key(),
            "format": "json",
            "offset": offset,
            "limit": _PAGE,
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    resource_id = node_id[len(_PREFIX):]
    rows: list[dict] = []
    offset = 0
    total: int | None = None
    pages = 0
    while True:
        page = _fetch_page(resource_id, offset)
        if total is None:
            total = int(page.get("total", 0))
        records = page.get("records") or []
        if not records:
            break
        rows.extend(records)
        # Advance by what the server actually returned, NOT a fixed page size:
        # the endpoint may return fewer than the requested limit (the public
        # sample key caps at 10/call), and a fixed += _PAGE would skip the gap.
        offset += len(records)
        pages += 1
        if total is not None and offset >= total:
            break
        if pages > _MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded {_MAX_PAGES} pages (offset={offset}, total={total}); "
                "source grew past expectations — raise the ceiling deliberately"
            )
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Each resource has its own column schema; publish it through unchanged. The
# transform is the correctness gate (0 rows fails the node).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
