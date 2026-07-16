"""Shared HTTP + paging helpers for the data.gov CKAN connector.

The catalog is served keyless and unthrottled at catalog-old.data.gov (the
api.gsa.gov gateway requires an api.data.gov key we don't have). `_action`
wraps the CKAN action API with transient retry and success-flag checking;
`_crawl_packages` pages the full package corpus once, writing typed parquet
fragments so transform/profile reads avoid JSON schema inference. Shared by
the datasets and resources download nodes (both crawl the same package
payload).
"""

from __future__ import annotations

import math
import os
import time

import pyarrow as pa

from subsets_utils import get, list_raw_fragments, load_state, save_raw_parquet, save_state, transient_retry

BASE = "https://catalog-old.data.gov/api/3"
PAGE_SIZE = 1000          # CKAN/Solr caps rows at 1000 (verified)
SORT = "metadata_created asc"  # stable-ish order for start/rows deep paging
MAX_PAGES = 2000          # safety ceiling (~403 expected); raises if exceeded
EXT = "parquet"
STATE_VERSION = 1

# Leave enough wall-clock for the supervisor to commit manifest entries, upload
# logs, and dispatch a continuation before the GitHub hard cap. The runner's
# DAG_TIME_BUDGET can span an entire chained job, so cap individual catalog
# crawl legs explicitly instead of spending a large fraction of that value.
DEFAULT_TIME_BUDGET_S = 20_700.0
MAX_PACKAGE_LEG_S = 4_800.0
LEG_FRACTION = 0.20
DEFAULT_PAGES_PER_LEG = 80
DEFAULT_PAGES_PER_FRAGMENT = 10

DATASET_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("title", pa.string()),
    ("notes", pa.string()),
    ("organization", pa.string()),
    ("owner_org", pa.string()),
    ("license_id", pa.string()),
    ("license_title", pa.string()),
    ("metadata_created", pa.string()),
    ("metadata_modified", pa.string()),
    ("num_resources", pa.int64()),
    ("num_tags", pa.int64()),
    ("type", pa.string()),
    ("state", pa.string()),
    ("maintainer", pa.string()),
    ("author", pa.string()),
    ("version", pa.string()),
    ("url", pa.string()),
    ("tags", pa.string()),
    ("groups", pa.string()),
])

RESOURCE_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("package_id", pa.string()),
    ("dataset_name", pa.string()),
    ("organization", pa.string()),
    ("name", pa.string()),
    ("description", pa.string()),
    ("format", pa.string()),
    ("mimetype", pa.string()),
    ("size", pa.int64()),
    ("created", pa.string()),
    ("last_modified", pa.string()),
    ("state", pa.string()),
    ("resource_type", pa.string()),
    ("url_type", pa.string()),
    ("url", pa.string()),
])


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
    return min(budget * LEG_FRACTION, MAX_PACKAGE_LEG_S)


def _pages_per_leg() -> int:
    try:
        pages = int(os.environ.get("DATA_GOV_PACKAGE_PAGES_PER_LEG", ""))
    except ValueError:
        pages = DEFAULT_PAGES_PER_LEG
    return max(1, pages or DEFAULT_PAGES_PER_LEG)


def _pages_per_fragment() -> int:
    try:
        pages = int(os.environ.get("DATA_GOV_PACKAGE_PAGES_PER_FRAGMENT", ""))
    except ValueError:
        pages = DEFAULT_PAGES_PER_FRAGMENT
    return max(1, pages or DEFAULT_PAGES_PER_FRAGMENT)


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


def _fragment(start_page: int, end_page: int) -> str:
    if start_page == end_page:
        return f"{start_page:05d}"
    return f"{start_page:05d}-{end_page:05d}"


def _fragment_pages(fragment: str, total_pages: int) -> set[int]:
    try:
        if "-" in fragment:
            start, end = fragment.split("-", 1)
            return set(range(int(start), min(int(end), total_pages - 1) + 1))
        page = int(fragment)
        return {page} if page < total_pages else set()
    except ValueError:
        return set()


def as_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def as_str(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def _crawl_packages(node_id: str, row_builder, schema: pa.Schema) -> bool | None:
    """Page the full package corpus, writing one parquet batch per fragment.

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

    committed_pages = set()
    for fragment in committed:
        committed_pages.update(_fragment_pages(fragment, total_pages))

    if state.get("total_pages") == total_pages and len(committed_pages) >= total_pages:
        print(f"  -> {node_id}: already drained this run ({total_pages} pages)")
        return None

    deadline = time.monotonic() + _leg_seconds()
    max_pages_this_leg = _pages_per_leg()
    pages_per_fragment = _pages_per_fragment()
    rows_this_leg = 0
    pages_this_leg = 0

    for batch_start in range(0, total_pages, pages_per_fragment):
        batch_end = min(batch_start + pages_per_fragment, total_pages) - 1
        fragment = _fragment(batch_start, batch_end)
        if fragment in committed:
            continue

        batch_pages = [page for page in range(batch_start, batch_end + 1) if page not in committed_pages]
        if not batch_pages:
            continue

        if pages_this_leg >= max_pages_this_leg:
            print(
                f"  -> {node_id}: page leg cap reached at page {batch_start} "
                f"({pages_this_leg:,} pages, {rows_this_leg:,} rows this leg); "
                "committing and continuing"
            )
            return True

        if rows_this_leg and time.monotonic() >= deadline:
            print(
                f"  -> {node_id}: leg budget spent at page {batch_start} "
                f"({rows_this_leg:,} rows this leg); committing and continuing"
            )
            return True

        batch: list[dict] = []
        for page in batch_pages:
            if pages_this_leg >= max_pages_this_leg:
                break
            start = page * PAGE_SIZE
            results = first["results"] if page == 0 else _action(
                "package_search", rows=PAGE_SIZE, start=start, sort=SORT
            )["results"]
            if not results:
                _finish(node_id, run_id, count, page)
                return None

            for pkg in results:
                batch.extend(row_builder(pkg))
            pages_this_leg += 1

        if batch:
            save_raw_parquet(pa.Table.from_pylist(batch, schema=schema), node_id, fragment=fragment)
            rows_this_leg += len(batch)

    _finish(node_id, run_id, count, total_pages)
    print(f"  -> {node_id}: drained, {rows_this_leg:,} rows this leg")
    return None
