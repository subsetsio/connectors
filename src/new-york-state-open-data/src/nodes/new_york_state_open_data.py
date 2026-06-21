"""New York State Open Data (data.ny.gov) — Socrata catalog connector.

One download spec per rank-accepted dataset (the entity union in
src/constants.py). Each dataset is pulled in full via the Socrata SODA JSON
endpoint (https://data.ny.gov/resource/{id}.json) with stable :id-ordered
offset pagination, and written as NDJSON — the corpus is heterogeneous (729
datasets, each with its own column list and drifty types), so NDJSON is the
right raw format and the transform re-types on read.

Shape: stateless full re-pull (shape 1). Socrata supports a SoQL $where delta
filter, but our pattern is full snapshots, so we re-fetch each dataset whole
every run and overwrite. A permanent 4xx on one dataset (deleted / access
changed) writes a TTL-bound skipped marker and returns, keeping per-entity
failures per-entity.

Each download has a thin pass-through SQL transform that publishes one Delta
table per dataset (SELECT * — Socrata field_name keys are already clean
snake_case; the transform's job here is to materialize and fail loudly on an
empty/broken raw).
"""
import time

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    load_state,
    save_raw_ndjson,
    save_state,
    transient_retry,
)
from constants import ENTITY_IDS

PREFIX = "new-york-state-open-data-"
DOMAIN = "https://data.ny.gov"
PAGE = 50000            # SODA documented max page size
MAX_PAGES = 4000        # safety backstop (~200M rows); raises, never truncates silently
SKIP_TTL = 14 * 86400


@transient_retry()
def _fetch_page(url, params):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _entity_id(node_id: str) -> str:
    return node_id[len(PREFIX):]


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = _entity_id(node_id)
    url = f"{DOMAIN}/resource/{entity_id}.json"

    state = load_state(asset)
    skipped = state.get("skipped") or {}
    if entity_id in skipped and skipped[entity_id].get("expires_at", 0) > time.time():
        # honor an unexpired skip marker
        return

    rows = []
    offset = 0
    for page_no in range(MAX_PAGES):
        params = {"$limit": PAGE, "$offset": offset, "$order": ":id"}
        try:
            batch = _fetch_page(url, params)
        except Exception as exc:  # noqa: BLE001
            status = getattr(getattr(exc, "response", None), "status_code", None)
            # Permanent client errors (except 429, which transient_retry handles):
            # dataset deleted / access changed / not a tabular resource.
            if status is not None and 400 <= status < 500 and status != 429:
                print(f"[{asset}] permanent HTTP {status} for {entity_id}: skipping")
                skipped[entity_id] = {
                    "reason": f"http_{status}",
                    "expires_at": int(time.time()) + SKIP_TTL,
                }
                save_state(asset, {"schema_version": 1, "skipped": skipped})
                return
            raise
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < PAGE:
            break
        offset += PAGE
    else:
        raise RuntimeError(
            f"[{asset}] hit MAX_PAGES={MAX_PAGES} for {entity_id} without draining; "
            "raise the cap or switch to incremental."
        )

    # Write raw before state, always.
    save_raw_ndjson(rows, asset)
    save_state(asset, {"schema_version": 1, "rows": len(rows), "skipped": skipped})


def _node_id(entity_id: str) -> str:
    return f"{PREFIX}{entity_id.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
