"""New York State Open Data (data.ny.gov) — Socrata catalog connector.

One download spec per rank-accepted dataset (the entity union in
src/constants.py). Each dataset is pulled in full via the Socrata **bulk CSV
export** (https://data.ny.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD),
which streams the entire table in one server-side request. The bytes are
streamed straight to the raw store with bounded memory — never buffered in a
Python list — because the corpus includes multi-hundred-million-row tables
(e.g. the 266M-row Lobbyist Bi-Monthly Reports) that would OOM a buffering
fetch and that deep SODA offset pagination cannot drain in reasonable time.

Shape: stateless full re-pull (shape 1). Socrata supports a SoQL $where delta
filter, but our pattern is full snapshots, so we re-fetch each dataset whole
every run and overwrite. Raw is written as CSV (uncompressed, so the DuckDB
transform can parallelize the scan of the large ones); the bulk export's
header row carries the dataset's display column names.

Each download has a thin pass-through SQL transform that publishes one Delta
table per dataset (SELECT * — materialize and fail loudly on a broken raw).
"""
import time

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    load_state,
    raw_writer,
    save_state,
    transient_retry,
)
from constants import ENTITY_IDS

PREFIX = "new-york-state-open-data-"
DOMAIN = "https://data.ny.gov"
CHUNK = 1 << 20          # 1 MiB stream chunks
SKIP_TTL = 14 * 86400
# Generous read timeout: the export of a 100M+ row table can take a while to
# start streaming, and each chunk must arrive within this window.
TIMEOUT = httpx.Timeout(600.0, connect=15.0)


def _entity_id(node_id: str) -> str:
    return node_id[len(PREFIX):]


@transient_retry()
def _stream_csv(asset: str, url: str) -> None:
    """Stream the bulk CSV export to the raw store. Re-entrant: each attempt
    truncates and rewrites, so a mid-stream transient failure retries cleanly."""
    client = get_client()
    with client.stream(
        "GET", url, params={"accessType": "DOWNLOAD"}, timeout=TIMEOUT
    ) as resp:
        resp.raise_for_status()
        with raw_writer(asset, "csv", mode="wb") as out:
            for chunk in resp.iter_bytes(chunk_size=CHUNK):
                out.write(chunk)


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = _entity_id(node_id)

    state = load_state(asset)
    skipped = state.get("skipped") or {}
    if entity_id in skipped and skipped[entity_id].get("expires_at", 0) > time.time():
        return

    url = f"{DOMAIN}/api/views/{entity_id}/rows.csv"
    try:
        _stream_csv(asset, url)
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        # Permanent client errors (except 429, which transient_retry handles):
        # dataset deleted / access changed. Mark skipped (TTL) and return so one
        # bad entity doesn't take down the run.
        if 400 <= status < 500 and status != 429:
            print(f"[{asset}] permanent HTTP {status} for {entity_id}: skipping")
            skipped[entity_id] = {
                "reason": f"http_{status}",
                "expires_at": int(time.time()) + SKIP_TTL,
            }
            save_state(asset, {"schema_version": 1, "skipped": skipped})
            return
        raise

    save_state(asset, {"schema_version": 1, "skipped": skipped})


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
