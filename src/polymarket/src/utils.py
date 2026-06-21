"""Shared HTTP + parse helpers for the Polymarket connector.

Both Gamma keyset endpoints (markets, events) and the CLOB prices-history crawl
share one unauthenticated JSON GET with transient retry. The Gamma catalog is
walked with /<resource>/keyset, feeding each response's `next_cursor` back as
`after_cursor`; page size is capped at 100.
"""
import json

from subsets_utils import get, transient_retry

GAMMA_BASE = "https://gamma-api.polymarket.com"

PAGE_SIZE = 100
MAX_PAGES = 20000  # safety ceiling (~2M rows at 100/page); raises if exceeded


@transient_retry()
def _get_json(url: str, params: dict):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _date(iso_str):
    """Trim an ISO timestamp to YYYY-MM-DD, or None."""
    if not iso_str:
        return None
    return iso_str[:10] if len(iso_str) >= 10 else None


def _f(value):
    """Coerce to float, tolerating numeric strings and None/''."""
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _i(value):
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _keyset_pages(resource: str, extra_params: dict | None = None):
    """Yield successive lists of records from a Gamma keyset endpoint."""
    url = f"{GAMMA_BASE}/{resource}/keyset"
    cursor = None
    for page in range(MAX_PAGES):
        params = {"limit": PAGE_SIZE}
        if extra_params:
            params.update(extra_params)
        if cursor:
            params["after_cursor"] = cursor
        payload = _get_json(url, params)
        rows = payload.get(resource, [])
        if not rows:
            return
        yield rows
        cursor = payload.get("next_cursor")
        if not cursor:
            return
    raise RuntimeError(
        f"{resource}: hit MAX_PAGES={MAX_PAGES} safety ceiling without exhausting "
        "the keyset cursor — corpus grew past expectations, raise MAX_PAGES."
    )
