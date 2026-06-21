"""Shared HTTP + park-directory helpers for the park-attendance connector.

Both node files (parks, attendance) pull the same queue-times.com park
directory; the HTTP client (with transient backoff) and the directory loader
live here so neither node file duplicates them.
"""
import httpx

from subsets_utils import get, transient_retry

PARKS_URL = "https://queue-times.com/parks.json"


@transient_retry(min_wait=2, max_wait=60)
def _get(url: str) -> httpx.Response:
    """GET with backoff on transient errors. A 404 is returned as-is (a park
    with no attendance page) — the caller decides to skip; 4xx/5xx other than
    404 raise (5xx via the retry predicate, other 4xx straight up)."""
    resp = get(url, timeout=(10.0, 60.0))
    if resp.status_code == 404:
        return resp
    resp.raise_for_status()
    return resp


def _load_parks() -> list[dict]:
    """Flatten queue-times.com/parks.json into a flat list of park dicts, each
    carrying its operator company name."""
    groups = _get(PARKS_URL).json()
    parks: list[dict] = []
    for group in groups:
        company = group.get("name")
        for park in group.get("parks", []):
            parks.append({**park, "company": company})
    if not parks:
        raise ValueError("parks.json returned no parks")
    return parks
