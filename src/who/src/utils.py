"""Shared HTTP/OData helpers for the WHO GHO connector.

Mechanism: GHO OData API (https://ghoapi.azureedge.net/api), no auth, Azure CDN.
"""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from subsets_utils import get, is_transient

BASE = "https://ghoapi.azureedge.net/api"


def get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0), headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def _with_query_params(url: str, params: dict[str, int]) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({k: str(v) for k, v in params.items()})
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _fetch_odata_skip_pages(url: str, page_size: int) -> list[dict]:
    rows: list[dict] = []
    skip = 0
    pages = 0
    while True:
        payload = get_json(_with_query_params(url, {"$top": page_size, "$skip": skip}))
        page_rows = payload.get("value", [])
        rows.extend(page_rows)
        pages += 1
        if len(page_rows) < page_size:
            return rows
        skip += page_size
        if pages > 10000:
            raise RuntimeError(f"pagination cap exceeded for {url}")


def fetch_odata(url: str, *, fallback_page_size: int | None = None) -> list[dict]:
    """Fetch an OData collection, following @odata.nextLink if present."""
    rows: list[dict] = []
    next_url = url
    pages = 0
    try:
        while next_url:
            payload = get_json(next_url)
            rows.extend(payload.get("value", []))
            next_url = payload.get("@odata.nextLink")
            pages += 1
            if pages > 10000:
                raise RuntimeError(f"pagination cap exceeded for {url}")
    except Exception as e:
        if fallback_page_size is None or not is_transient(e):
            raise
        return _fetch_odata_skip_pages(url, fallback_page_size)
    return rows
