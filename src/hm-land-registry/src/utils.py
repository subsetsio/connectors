"""Shared HTTP helper for the HM Land Registry connector node modules."""

from __future__ import annotations

import httpx

from subsets_utils import get, transient_retry


@transient_retry()
def request(url: str, **kwargs) -> httpx.Response:
    """GET with retry on transient failures; 4xx (e.g. a missing year file)
    raises immediately for the caller to classify."""
    resp = get(url, **kwargs)
    resp.raise_for_status()
    return resp
