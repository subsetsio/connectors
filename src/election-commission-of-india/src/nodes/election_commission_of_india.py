"""Election Commission of India — 2024 Lok Sabha General Election tables.

Source: data.gov.in Open Government Data (OGD) Platform, organization
"Election Commission of India". Six tabular resources are pulled, one
download NodeSpec each, via the OGD REST API
(https://api.data.gov.in/resource/{index_name}).

Fetch shape: stateless full re-pull. Each resource is tens-to-hundreds of
rows, so we re-fetch the whole table every run and overwrite — no watermark,
no incremental (the API exposes no `since`/cursor filter; resources are
republished wholesale, not appended). Auth is an `api-key` query param; the
public OGD sample key is the default, overridable via DATA_GOV_IN_API_KEY.
The sample key caps each page at 10 records, so we paginate by offset until
the `total` reported on the first page is reached.

Raw is saved as NDJSON with every value stringified, because the OGD API
returns mixed JSON types within a column (e.g. 0 and "0"); the transform SQL
re-types each column with TRY_CAST, which is the single source of truth for
column types.
"""

import os

from ratelimit import limits, sleep_and_retry
from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

SLUG = "election-commission-of-india"
BASE = "https://api.data.gov.in/resource/"
DEMO_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
PAGE = 100          # demo key silently caps to 10; a registered key honours larger
MAX_PAGES = 1000    # safety ceiling — raises (never silently returns) on hit


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY", DEMO_KEY)


def _dl_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# The shared public OGD sample key is rate-limited; pace requests (per-process)
# and lean on transient_retry's backoff to ride out any 429s. A registered
# DATA_GOV_IN_API_KEY lifts both the page cap and the rate limit.
@sleep_and_retry
@limits(calls=60, period=60)
def _throttle() -> None:
    return None


@transient_retry(attempts=8, min_wait=5, max_wait=120)
def _fetch_page(resource_id: str, offset: int) -> dict:
    _throttle()
    resp = get(
        BASE + resource_id,
        params={
            "format": "json",
            "limit": str(PAGE),
            "offset": str(offset),
            "api-key": _api_key(),
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id                         # the spec id IS the asset name
    resource_id = node_id[len(SLUG) + 1:]   # strip "election-commission-of-india-"
    rows: list = []
    offset = 0
    total = None
    pages = 0
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} (offset={offset}, total={total})"
            )
        d = _fetch_page(resource_id, offset)
        if total is None:
            total = int(d.get("total") or 0)
        recs = d.get("records") or []
        if not recs:
            break
        rows.extend(recs)
        pages += 1
        offset += len(recs)
        if total and offset >= total:
            break
    # Stringify every value: the OGD API mixes int/float/str within a column,
    # so a uniform VARCHAR raw lets the transform own typing via TRY_CAST.
    norm = [{k: (None if v is None else str(v)) for k, v in r.items()} for r in rows]
    save_raw_ndjson(norm, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_dl_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

