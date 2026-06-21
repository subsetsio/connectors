"""Shared HTTP + firehose machinery for the National Highways (WebTRIS) connector.

Holds the things used by 2+ node files: the WebTRIS base URL, the transient-retry
GET wrapper, site enumeration, and the chunked-crawl driver that walks the active
site set in fixed-size batches with a resumable cursor. No NodeSpec definitions
live here.
"""

from __future__ import annotations

import httpx

from subsets_utils import (
    get,
    load_state,
    save_state,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://webtris.highwaysengland.co.uk/api/v1.0"
STATE_VERSION = 1

# How many sites per NDJSON batch file, and how many batches to process per
# invocation before checkpointing via a needs_continuation return. Kept modest
# so each dispatch finishes comfortably inside a CI step and progress is saved
# often.
CHUNK_SITES = 100
CHUNKS_PER_RUN = 15

# Ascending ladder of candidate start years for annual/monthly. The earliest
# candidate that returns a valid response is used (maximising history) — the
# WebTRIS API rejects a start_date earlier than a site's first data.
_START_LADDER = (2015, 2017, 2019, 2021, 2023)


# --------------------------------------------------------------------------- #
# HTTP                                                                         #
# --------------------------------------------------------------------------- #


@transient_retry()
def _get(url: str):
    """GET with backoff on transient transport/5xx/429 errors.

    Returns the parsed JSON object, or None when there's no usable data.
    WebTRIS signals "invalid request" (e.g. a start_date earlier than a site's
    first data) as an HTTP 400 with a bare-string body, and "no data yet" as a
    200 with an empty body — both are permanent for these params, so they
    surface here as a clean None for the caller (the start-year ladder / the
    per-site skip) to handle. 429/5xx are retried by the decorator.
    """
    resp = get(url, timeout=(10.0, 180.0))
    code = resp.status_code
    if code == 429 or 500 <= code < 600:
        resp.raise_for_status()  # -> HTTPStatusError -> retried as transient
    if 400 <= code < 500:
        return None  # invalid params / not found / no data for this query
    if not resp.text.strip():
        return None
    try:
        data = resp.json()
    except (ValueError, httpx.DecodingError):
        return None
    return data if isinstance(data, dict) else None


# --------------------------------------------------------------------------- #
# Site enumeration + chunking                                                 #
# --------------------------------------------------------------------------- #
def _all_sites() -> list[dict]:
    data = _get(f"{BASE}/sites")
    if not data or "sites" not in data:
        raise RuntimeError("WebTRIS /sites returned no site list")
    return data["sites"]


def _active_site_ids() -> list[str]:
    """Active site ids, sorted by numeric id for a stable chunking order."""
    ids = [s["Id"] for s in _all_sites() if s.get("Status") == "Active"]
    return sorted(ids, key=lambda x: int(x))


def _chunks(seq: list, size: int):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def _crawl_chunks(node_id: str, fetch_chunk) -> bool:
    """Drive the firehose for one report family.

    Walks the active sites in fixed chunks, writing one NDJSON batch per chunk
    via `fetch_chunk(site_ids) -> list[dict]`. Resumes from a saved cursor and
    returns True (needs_continuation) while chunks remain after this slice.
    """
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "next_chunk": 0}

    site_ids = _active_site_ids()
    all_chunks = list(_chunks(site_ids, CHUNK_SITES))
    start = int(state.get("next_chunk", 0))

    processed = 0
    idx = start
    while idx < len(all_chunks) and processed < CHUNKS_PER_RUN:
        chunk = all_chunks[idx]
        rows = fetch_chunk(chunk)
        batch_key = f"{chunk[0]}-{chunk[-1]}"
        if rows:
            # Write raw BEFORE advancing state — a crash loses at most this
            # batch, never silently records phantom completion.
            save_raw_ndjson(rows, f"{node_id}-{batch_key}")
        idx += 1
        processed += 1
        save_state(node_id, {"schema_version": STATE_VERSION, "next_chunk": idx})

    if idx >= len(all_chunks):
        # Fully drained — reset the cursor so the next scheduled refresh
        # re-crawls from the top (picking up revisions / the rolling window).
        save_state(node_id, {"schema_version": STATE_VERSION, "next_chunk": 0})
        return False
    return True  # more chunks remain → re-dispatch
