"""data.gov.in — Open Government Data Platform India (redistributor).

Catalog connector: one download node per rank-accepted resource_id, all fetched
the same way via the REST `resource` endpoint (research mechanism `rest_resource`):

    https://api.data.gov.in/resource/{resource_id}?api-key=KEY&format=json&offset=&limit=

Each resource is one tabular dataset with its own column schema; records are flat,
typed dicts. Schemas differ across resources, so raw is written as NDJSON and the
transform is a thin `SELECT *` that publishes the table as-is.

Fetch shape: stateless full re-pull (shape 1). Resources are small-to-medium
admin/statistical tables; we re-fetch the whole resource each run and overwrite.
There is no per-record incremental filter on the data endpoint (research), so a
watermark would buy nothing.

Auth: `api-key` is a QUERY parameter (not a header). A registered key is read from
DATA_GOV_IN_API_KEY when present; otherwise the public sample key published by
data.gov.in is used. The API is rate-limited even for sequential corpus pulls, so
requests are paced and 429s get a source-specific longer backoff.
"""

import os
import time

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    delete_raw_file,
    get,
    load_state,
    raw_asset_exists,
    save_raw_ndjson,
    save_state,
)
from constants import ENTITY_IDS

SLUG = "data-gov-in"
_PREFIX = f"{SLUG}-"
_BASE = "https://api.data.gov.in/resource/"
_SAMPLE_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
_PAGE = 1000
# Safety ceiling: 5M rows per resource. These are administrative tables, not
# firehoses; blowing past this means the source changed shape — raise, don't
# silently truncate.
_MAX_PAGES = 5000
_RAW_EXT = "ndjson.zst"
_MAINTAIN_MAX_AGE_DAYS = 7
_PACE_S = float(os.environ.get("DATA_GOV_IN_REQUEST_PACE_S", "1.5"))
_RATE_LIMIT_ATTEMPTS = 8
_STATE_VERSION = 1
_LEG_SECONDS = int(os.environ.get("DATA_GOV_IN_LEG_SECONDS", str(4 * 60 * 60)))


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or _SAMPLE_KEY


def _fetch_page(resource_id: str, offset: int) -> dict:
    params = {
        "api-key": _api_key(),
        "format": "json",
        "offset": offset,
        "limit": _PAGE,
    }
    for attempt in range(1, _RATE_LIMIT_ATTEMPTS + 1):
        time.sleep(_PACE_S)
        resp = get(_BASE + resource_id, params=params, timeout=(10.0, 120.0))
        if resp.status_code != 429:
            resp.raise_for_status()
            return resp.json()
        if attempt == _RATE_LIMIT_ATTEMPTS:
            resp.raise_for_status()
        wait = min(600.0, 60.0 * attempt)
        print(f"{resource_id}: HTTP 429 at offset {offset}; retrying in {wait:.0f}s")
        time.sleep(wait)
    raise AssertionError("unreachable")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    resource_id = node_id[len(_PREFIX):]
    run_id = os.environ.get("RUN_ID", "unknown")
    state = load_state(asset)
    same_run = (
        state.get("schema_version") == _STATE_VERSION
        and state.get("run_id") == run_id
    )
    if not same_run:
        delete_raw_file(asset, _RAW_EXT)
        state = {
            "schema_version": _STATE_VERSION,
            "run_id": run_id,
            "next_offset": 0,
            "total": None,
            "complete": False,
        }
        save_state(asset, state)

    offset = int(state.get("next_offset") or 0)
    total = state.get("total")
    total = int(total) if total is not None else None
    pages = offset // _PAGE
    deadline = time.monotonic() + _LEG_SECONDS
    while True:
        payload = _fetch_page(resource_id, offset)
        if total is None:
            total = int(payload.get("total") or 0)
        batch = payload.get("records") or []
        save_raw_ndjson(batch, asset, fragment=f"{offset:012d}")
        offset += len(batch)
        pages += 1
        state.update({
            "next_offset": offset,
            "total": total,
            "complete": offset >= total or not batch,
        })
        save_state(asset, state)
        if offset >= total or not batch:
            break
        if pages >= _MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded {_MAX_PAGES} pages (total={total}) — "
                "resource is larger than expected; investigate before raising the cap"
            )
        if time.monotonic() >= deadline:
            print(
                f"{resource_id}: leg budget spent at offset {offset}/{total}; "
                "committing fragments and continuing next link"
            )
            return True

    print(f"{resource_id}: complete, {total or 0} rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

def _is_fresh(asset_id: str) -> bool:
    state = load_state(asset_id)
    return (
        state.get("schema_version") == _STATE_VERSION
        and state.get("complete") is True
        and raw_asset_exists(asset_id, _RAW_EXT, max_age_days=_MAINTAIN_MAX_AGE_DAYS)
    )


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Weekly full refresh; data.gov.in resource endpoint has no reliable "
            "per-record cursor, so raw committed within the 7-day cadence is fresh. "
            "The state complete flag prevents continuation fragments from being "
            "mistaken for a complete asset."
        ),
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
