"""Shared HTTP + paging helpers for the data.gov CKAN connector.

The catalog is served keyless and unthrottled at catalog-old.data.gov (the
api.gsa.gov gateway requires an api.data.gov key we don't have). `_action`
wraps the CKAN action API with transient retry and success-flag checking;
`_crawl_packages` pages the full package corpus once, writing one ndjson batch
per page so peak memory stays at a single page. Shared by the datasets and
resources download nodes (both crawl the same package payload).
"""

from __future__ import annotations

import math
import os
import time

from subsets_utils import get, list_raw_fragments, load_state, save_raw_ndjson, save_state, transient_retry

BASE = "https://catalog-old.data.gov/api/3"
PAGE_SIZE = 1000          # CKAN/Solr caps rows at 1000 (verified)
SORT = "metadata_created asc"  # stable-ish order for start/rows deep paging
MAX_PAGES = 2000          # safety ceiling (~403 expected); raises if exceeded
EXT = "ndjson.zst"
STATE_VERSION = 1

# Leave enough wall-clock for the supervisor to commit manifest entries, upload
# logs, and dispatch a continuation before the GitHub hard cap.
DEFAULT_TIME_BUDGET_S = 20_700.0
LEG_FRACTION = 0.30


@transient_retry(attempts=8, min_wait=8, max_wait=180)
def _action(action: str, **params) -> dict:
    resp = get(f"{BASE}/action/{action}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success", False):
        raise RuntimeError(f"CKAN action {action} returned success=false: {str(body)[:200]}")
    return body["result"]


def _leg_seconds() -> float:
    try:
        budget = float(os.environ.get("DAG_TIME_BUDGET", "")) or DEFAULT_TIME_BUDGET_S
    except ValueError:
        budget = DEFAULT_TIME_BUDGET_S
    return budget * LEG_FRACTION


def _run_state(asset: str, run_id: str) -> dict:
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        return {}
    if state.get("run_id") != run_id:
        return {}
    return state


def _finish(asset: str, run_id: str, count: int, total_pages: int) -> None:
    save_state(
        asset,
        {
            "schema_version": STATE_VERSION,
            "run_id": run_id,
            "count": count,
            "total_pages": total_pages,
        },
    )


def _fragment(page: int) -> str:
    return f"{page:05d}"


def _crawl_packages(node_id: str, row_builder) -> bool | None:
    """Page the full package corpus, writing one ndjson batch per page.

    row_builder(pkg) -> list[dict] (resources) or [dict] (datasets).

    Returns True when the current leg spent its budget before the corpus was
    drained. The runtime treats that as a clean continuation: fragments written
    so far are committed, and the next leg resumes from the raw manifest.
    """
    run_id = os.environ.get("RUN_ID", "unknown")
    state = _run_state(node_id, run_id)
    committed = {
        frag
        for frag, meta in list_raw_fragments(node_id, EXT).items()
        if meta.get("run_id") == run_id
    }

    first = _action("package_search", rows=PAGE_SIZE, start=0, sort=SORT)
    count = first["count"]
    total_pages = math.ceil(count / PAGE_SIZE)
    if total_pages > MAX_PAGES:
        raise RuntimeError(
            f"{node_id}: total_pages={total_pages} exceeds MAX_PAGES={MAX_PAGES} "
            f"(count={count})"
        )

    if state.get("total_pages") == total_pages and len(committed) >= total_pages:
        print(f"  -> {node_id}: already drained this run ({total_pages} pages)")
        return None

    deadline = time.monotonic() + _leg_seconds()
    rows_this_leg = 0

    for page in range(total_pages):
        fragment = _fragment(page)
        if fragment in committed:
            continue

        if rows_this_leg and time.monotonic() >= deadline:
            print(
                f"  -> {node_id}: leg budget spent at page {page} "
                f"({rows_this_leg:,} rows this leg); committing and continuing"
            )
            return True

        start = page * PAGE_SIZE
        results = first["results"] if page == 0 else _action(
            "package_search", rows=PAGE_SIZE, start=start, sort=SORT
        )["results"]
        if not results:
            _finish(node_id, run_id, count, page)
            return None

        batch: list[dict] = []
        for pkg in results:
            batch.extend(row_builder(pkg))
        if batch:
            save_raw_ndjson(batch, node_id, fragment=fragment)
            rows_this_leg += len(batch)

    _finish(node_id, run_id, count, total_pages)
    print(f"  -> {node_id}: drained, {rows_this_leg:,} rows this leg")
    return None
