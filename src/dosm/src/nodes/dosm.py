"""DOSM (Department of Statistics Malaysia) — OpenDOSM data catalogue.

Catalog connector. Every OpenDOSM dataset is published as a single, full,
stable parquet table on storage.dosm.gov.my / storage.data.gov.my (one file =
one complete table, no pagination, no auth). The download for each subset is a
stateless full re-pull of that file: fetch the bytes, read the parquet, and
re-write it to our raw layer. Tables are small (KB–low MB) so re-pulling the
whole corpus every refresh is cheap; there is no incremental query surface
(no since/cursor on the static files), so stateless full re-pull is correct.

The per-dataset parquet URLs are persistent and live in `src/constants.py`
(ENTITY_URLS), copied from the rank-accepted entity union. The transform layer
publishes each raw table as-is (the source parquet is already clean, typed
statistical data) — a thin SELECT pass that fails loudly on an empty payload.
"""

import io

import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_URLS


@transient_retry()  # 6 attempts, exponential backoff over transient net errors / 429 / 5xx
def _fetch_parquet_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()  # inside the retry so 5xx is retried
    return resp.content


def fetch_one(node_id: str) -> None:
    """Fetch one OpenDOSM dataset's full parquet table and persist it.

    The runtime passes the spec id; it is also the asset name to write.
    """
    asset = node_id
    url = ENTITY_URLS[node_id]  # KeyError here = a spec id with no mapped URL (a bug)
    raw = _fetch_parquet_bytes(url)
    # The source already ships a typed parquet — its embedded schema IS the
    # explicit contract for this single per-asset write (not a batched append).
    table = pq.read_table(io.BytesIO(raw))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download")
    for sid in ENTITY_URLS
]
