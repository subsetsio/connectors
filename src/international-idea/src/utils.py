"""Shared HTTP access for the International IDEA connector."""

import httpx

from subsets_utils import get, transient_retry

GSOD_API = "https://www.idea.int/gsod-indices/api"


@transient_retry()
def request(url: str, **kwargs) -> httpx.Response:
    resp = get(url, timeout=(10.0, 180.0), **kwargs)
    resp.raise_for_status()
    return resp
