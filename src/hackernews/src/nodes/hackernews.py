"""Hacker News items connector.

Downloads the full Hacker News item corpus (stories, comments, jobs, polls,
poll options) from the official Firebase API (https://github.com/HackerNews/API,
MIT). Items are addressed by monotonically increasing integer id from 1 to
``/v0/maxitem.json`` (~48.5M as of 2026-06). There is no bulk export — one HTTP
request per item — so this is a **record-stream firehose** (implement shape 3):

  * one download spec (the ``items`` entity),
  * raw written as id-range batches (``hackernews-items-{lo}-{hi}.parquet``),
  * a watermark (next id to fetch) persisted after every closed batch.

The fetch fn loops until it reaches the live edge (``maxitem``); it imposes no
wall-clock or record budget. The supervisor caps a run by interrupting the node
when the CI budget nears — because raw+state are written per batch, the next
run resumes from the saved watermark with at most one in-flight batch refetched
(its asset id is deterministic from the watermark, so the refetch overwrites).

Per-item fetches go through a single-event-loop ``httpx.AsyncClient`` rather
than ``subsets_utils.get``: the corpus needs ~48.5M individual requests, and the
only concurrency the sync client affords is a thread pool. At firehose
concurrency that thrashes the shared sync client AND the harness's per-request
HTTP-log flush (a first cloud run failed with ``[Errno 9] Bad file descriptor``
after the shared csv handle degraded under 64 threads). asyncio keeps all I/O on
one thread — high concurrency, no shared-handle races — which is exactly how the
legacy production connector ran. The single ``maxitem`` lookup still goes through
``subsets_utils.get``.

Refreshes after the initial backfill fetch only ids newer than the watermark
(item ids are monotonic — the only incremental signal the API offers); edits to
old items are not re-pulled. The transform reads every batch and overwrites the
published Delta table.
"""

import asyncio
import json
from datetime import datetime, timezone

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    is_transient,
    load_state,
    save_raw_parquet,
    save_state,
    transient_retry,
)

BASE = "https://hacker-news.firebaseio.com/v0"

# ASCII-only User-Agent (httpx headers must be ASCII).
USER_AGENT = "subsets.io-hackernews-connector/1.0 (+https://subsets.io)"

# Item ids per raw batch. ~100k items of zstd parquet land at well under
# 100MB; 48.5M items => ~485 batch files. Constant across runs so a given
# watermark always anchors the same batch boundaries (idempotent refetch).
BATCH_SIZE = 100_000

# Max in-flight per-item requests on the single async client. The official API
# documents no rate limit and the legacy production connector sustained ~500
# concurrent against the same Firebase host.
CONCURRENCY = 150

# Per-item async-fetch retry policy (transient errors only).
_MAX_ATTEMPTS = 6

# Bump when the watermark contract changes; unknown versions reset state.
STATE_VERSION = 1

# Explicit schema is the contract for batched parquet writes. Only id and type
# are reliably present; everything else is nullable (deleted-but-present fields,
# type-specific fields like score/title/url/descendants/poll/kids).
SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("type", pa.string()),
    ("by", pa.string()),
    ("time", pa.timestamp("s")),
    ("text", pa.string()),
    ("dead", pa.bool_()),
    ("parent", pa.int64()),
    ("poll", pa.int64()),
    ("url", pa.string()),
    ("score", pa.int64()),
    ("title", pa.string()),
    ("descendants", pa.int64()),
    ("kids", pa.string()),  # JSON array of child item ids
])

@transient_retry(min_wait=1, max_wait=60)
def _max_item_id() -> int:
    resp = get(f"{BASE}/maxitem.json", timeout=(10.0, 60.0))
    resp.raise_for_status()
    return int(resp.json())


def _parse_item(item: dict) -> dict:
    t = item.get("time")
    kids = item.get("kids")
    return {
        "id": item.get("id"),
        "type": item.get("type"),
        "by": item.get("by"),
        "time": (
            datetime.fromtimestamp(t, tz=timezone.utc).replace(tzinfo=None)
            if t else None
        ),
        "text": item.get("text"),
        "dead": bool(item.get("dead", False)),
        "parent": item.get("parent"),
        "poll": item.get("poll"),
        "url": item.get("url"),
        "score": item.get("score"),
        "title": item.get("title"),
        "descendants": item.get("descendants"),
        "kids": json.dumps(kids) if kids else None,
    }


async def _afetch_item(client: httpx.AsyncClient, sem: asyncio.Semaphore,
                       item_id: int):
    """Fetch one item with bounded concurrency and transient-error retry.
    Returns the item dict, or None for deleted ids (the API returns a literal
    JSON ``null`` rather than a 404). Raises on a non-transient error or after
    exhausting retries, which fails the batch (and node); the supervisor then
    resumes from the saved watermark."""
    url = f"{BASE}/item/{item_id}.json"
    for attempt in range(_MAX_ATTEMPTS):
        try:
            async with sem:
                resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # noqa: BLE001 — reclassified immediately
            if is_transient(exc) and attempt < _MAX_ATTEMPTS - 1:
                await asyncio.sleep(min(60.0, 2.0 ** attempt))
                continue
            raise


async def _afetch_range(client, sem, lo: int, hi: int) -> list[dict]:
    """Fetch items in [lo, hi] inclusive, in sub-chunks so the number of live
    task objects stays bounded while `sem` bounds in-flight connections."""
    rows = []
    sub = max(CONCURRENCY * 8, 1000)
    for start in range(lo, hi + 1, sub):
        end = min(start + sub - 1, hi)
        items = await asyncio.gather(
            *(_afetch_item(client, sem, i) for i in range(start, end + 1))
        )
        rows.extend(_parse_item(it) for it in items if it)
    return rows


async def _run_backfill(node_id: str, watermark: int, max_id: int) -> None:
    limits = httpx.Limits(max_connections=CONCURRENCY,
                          max_keepalive_connections=CONCURRENCY)
    timeout = httpx.Timeout(60.0, connect=10.0)
    async with httpx.AsyncClient(
        timeout=timeout, limits=limits,
        headers={"User-Agent": USER_AGENT}, follow_redirects=True,
    ) as client:
        sem = asyncio.Semaphore(CONCURRENCY)
        while watermark <= max_id:
            lo = watermark
            hi = min(lo + BATCH_SIZE - 1, max_id)
            asset = f"{node_id}-{lo}-{hi}"  # batch key is pure id-range info

            rows = await _afetch_range(client, sem, lo, hi)
            if rows:
                table = pa.Table.from_pylist(rows, schema=SCHEMA)
                save_raw_parquet(table, asset)  # write raw FIRST
            else:
                print(f"  batch {lo}-{hi}: all deleted, no file written")

            watermark = hi + 1
            save_state(node_id, {  # then advance the watermark
                "schema_version": STATE_VERSION,
                "watermark": watermark,
            })


def fetch_items(node_id: str) -> None:
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark", 1)  # next item id to fetch

    max_id = _max_item_id()
    print(f"  watermark={watermark:,} max_item={max_id:,} "
          f"({max(0, max_id - watermark + 1):,} to fetch)")

    asyncio.run(_run_backfill(node_id, watermark, max_id))
    print(f"  drained to item {max_id:,}")


DOWNLOAD_SPECS = [
    NodeSpec(id="hackernews-items", fn=fetch_items, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="hackernews-items-transform",
        deps=["hackernews-items"],
        sql='''
            SELECT
                CAST(id AS BIGINT)            AS id,
                type,
                "by",
                CAST(time AS TIMESTAMP)       AS time,
                text,
                COALESCE(dead, FALSE)         AS dead,
                CAST(parent AS BIGINT)        AS parent,
                CAST(poll AS BIGINT)          AS poll,
                url,
                CAST(score AS BIGINT)         AS score,
                title,
                CAST(descendants AS BIGINT)   AS descendants,
                kids
            FROM "hackernews-items"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY time DESC) = 1
        ''',
    ),
]
