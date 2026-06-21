"""Shared HTTP transport for Berkeley Earth subsets.

Both published subsets pull from the same stable HTTPS hosts (no auth). This
module holds the retried request layer and the shared S3 base URL; it defines
no NodeSpecs and is skipped by load_nodes() because its name starts with `_`.
"""
from __future__ import annotations

import httpx

from subsets_utils import get, transient_retry

# Global text + gridded NetCDF products live on this bucket; both subsets use it.
BASE_S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/"


@transient_retry()
def _request(url: str):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def fetch_text(url: str) -> str | None:
    """Return the text body, or None for a permanent 404 (region/variant absent)."""
    try:
        return _request(url).text
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            print(f"[skip] 404 {url}")
            return None
        raise


def fetch_bytes(url: str) -> bytes:
    return _request(url).content
