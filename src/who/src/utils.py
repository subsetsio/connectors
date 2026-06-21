"""Shared HTTP/OData helpers for the WHO GHO connector.

Mechanism: GHO OData API (https://ghoapi.azureedge.net/api), no auth, Azure CDN.
"""

from subsets_utils import get, transient_retry

BASE = "https://ghoapi.azureedge.net/api"


@transient_retry(min_wait=2, max_wait=60)
def get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0), headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def fetch_odata(url: str) -> list[dict]:
    """Fetch an OData collection, following @odata.nextLink if present."""
    rows: list[dict] = []
    next_url = url
    pages = 0
    while next_url:
        payload = get_json(next_url)
        rows.extend(payload.get("value", []))
        next_url = payload.get("@odata.nextLink")
        pages += 1
        if pages > 10000:
            raise RuntimeError(f"pagination cap exceeded for {url}")
    return rows
