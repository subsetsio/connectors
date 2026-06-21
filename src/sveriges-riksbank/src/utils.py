"""Shared HTTP + catalog helpers for the Sveriges Riksbank SWEA connector.

Mechanism: SWEA v1 REST API (https://api.riksbank.se/swea/v1), keyless, no auth.

Rate limit (keyless, per-IP) is strict and undocumented: empirically ~5
requests per ~60s window, with a `Retry-After` header (up to ~59s) on 429.
We therefore (a) fetch by group to minimise request count, (b) pace proactively
at ~4 req/min, and (c) retry honouring `Retry-After`. Register at
developer.api.riksbank.se for a higher quota if this is ever too slow.
"""

import httpx
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
)

from subsets_utils import get, is_transient

BASE = "https://api.riksbank.se/swea/v1"


def _wait(retry_state) -> float:
    """Honour the server's Retry-After on 429; otherwise exponential backoff."""
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        ra = exc.response.headers.get("Retry-After")
        if ra and ra.strip().isdigit():
            return min(int(ra) + 1, 90)
        return 60.0
    return min(4.0 * (2 ** max(retry_state.attempt_number - 1, 0)), 120.0)


@sleep_and_retry
@limits(calls=4, period=60)
def _rate_limited_get(url: str):
    """Proactively pace to ~4 req/min to stay under the per-IP quota."""
    return get(url, timeout=(10.0, 120.0))


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(8),
    wait=_wait,
    reraise=True,
)
def get_json(url: str):
    resp = _rate_limited_get(url)
    resp.raise_for_status()
    return resp.json()


def fetch_series_catalog() -> list[dict]:
    """The full /Series catalog: one record per time series."""
    data = get_json(f"{BASE}/Series")
    if not isinstance(data, list) or not data:
        raise AssertionError(f"/Series returned no records (type={type(data).__name__})")
    return data
