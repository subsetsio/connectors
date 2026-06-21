"""Shared transport for the USGS node files (water OGC + FDSN earthquakes).

Both surfaces are cursor-paged crawls over an HTTP service that throttles with
HTTP 429 and intermittent 5xx under sustained load. The retrying transport
helpers below pace the crawl to whatever the service allows; the loop guard is
shared across both crawlers.
"""
from __future__ import annotations

from subsets_utils import get, transient_retry

# Pure infinite-loop guard — bounded collections terminate well below this and
# windowed/time-bounded crawls are time-bounded. A hit means the cursor never
# advanced.
MAX_PAGES = 200_000


# stop=10 / max=180 (rather than the usual 6 / 120) to ride through the water
# service's 429 throttling and intermittent 500s on long crawls — ~13 min of
# backoff per page before a page is declared persistently failed.
@transient_retry(attempts=10, max_wait=180)
def get_json(url: str, params: dict | None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry(attempts=8)
def get_text(url: str, params: dict | None) -> str:
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text
