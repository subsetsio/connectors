"""Shared HTTP helpers for the Crossref connector — REST API
(https://api.crossref.org/).

Holds only the polite-pool config, the rate-limited JSON fetch with transient
retry, the cursor-pager, and the list-field unwrapper — code shared by the
registries and works subset modules. No NodeSpecs live here.
"""

from __future__ import annotations

from ratelimit import limits, sleep_and_retry

from subsets_utils import get, transient_retry

# --- constants --------------------------------------------------------------

BASE_URL = "https://api.crossref.org"
MAILTO = "ops@subsets.io"            # polite-pool identifier
PAGE_SIZE = 1000                     # Crossref max rows per page


# Documented soft limit is ~10 req/s (x-rate-limit headers); use ~80%. The
# limiter is per-process, so concurrent sibling specs may briefly exceed this on
# the shared host — 429s are absorbed by the retry/backoff below.
@sleep_and_retry
@limits(calls=8, period=1)
def _throttle() -> None:
    return None


# --- HTTP -------------------------------------------------------------------


@transient_retry()
def _get_json(path: str, params: dict) -> dict:
    _throttle()
    merged = {"mailto": MAILTO, **params}
    resp = get(f"{BASE_URL}/{path}", params=merged, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _iter_pages(path: str, params: dict, max_pages: int):
    """Cursor-page a Crossref list endpoint, yielding each page's items list.

    Terminates on an empty page or an absent next-cursor. The page cap is a
    safety ceiling: hitting it means the source grew past expectations, so we
    raise rather than silently stop short.
    """
    cursor = "*"
    for page_no in range(max_pages):
        page = _get_json(path, {**params, "rows": PAGE_SIZE, "cursor": cursor})
        message = page["message"]
        items = message.get("items") or []
        if not items:
            return
        yield items
        cursor = message.get("next-cursor")
        if not cursor:
            return
    raise RuntimeError(
        f"{path}: exceeded {max_pages} pages (params={params}) — source larger "
        "than expected; raise the page ceiling deliberately"
    )


# --- flatteners (shared) ----------------------------------------------------


def _first(value):
    """First element of a list-valued field, else None (Crossref wraps many
    scalar-ish fields — title, container-title, ISSN — in arrays)."""
    if isinstance(value, list):
        return value[0] if value else None
    return value
