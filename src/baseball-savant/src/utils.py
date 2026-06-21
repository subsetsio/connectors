"""Shared HTTP helpers for the Baseball Savant connector.

Underscore-prefixed so `load_nodes()` (orchestrator.py) skips it during spec
discovery: this module holds the GET-with-retry + CSV-fetch helpers used by both
the leaderboard family (`leaderboards.py`) and the pitch-by-pitch firehose
(`statcast.py`). HTTP/shared constants only — no NodeSpec definitions live here.
"""

from datetime import date

import httpx

from subsets_utils import get, transient_retry

SLUG = "baseball-savant"

# The Statcast tracking era began in 2015 (documented source constant). The upper
# bound is discovered dynamically so it never goes stale; seasons with no data for
# a given board simply come back empty and are skipped.
STATCAST_ERA_START_YEAR = 2015
STATCAST_ERA_START = date(STATCAST_ERA_START_YEAR, 3, 1)  # spring training onset


@transient_retry()
def _get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _fetch_csv_text(url: str):
    """GET a CSV; return text, or None if the response is a permanent 4xx or
    not actually a CSV (Savant returns a 404 HTML error page for bad params)."""
    try:
        resp = _get(url)
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if 400 <= code < 500 and code != 429:
            print(f"[{SLUG}] skip non-2xx {code}: {url}")
            return None
        raise
    ct = resp.headers.get("Content-Type", "").lower()
    if "csv" not in ct and "application/download" not in ct:
        print(f"[{SLUG}] skip non-csv content-type '{ct}': {url}")
        return None
    return resp.text
