"""Shared HTTP plumbing for the CFPB node files.

CFPB's static file hosts sit behind Akamai, which rejects some non-browser
agents, so every fetch goes through a single retrying GET that first installs a
browser-shaped User-Agent. This module holds only that shared transport — no
NodeSpec definitions live here.
"""

from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import configure_http, get

# A descriptive but browser-shaped UA — CFPB's static file hosts sit behind
# Akamai, which rejects some non-browser agents. ASCII only (httpx header rule).
_USER_AGENT = "Mozilla/5.0 (compatible; subsets.io-connector/1.0; +https://subsets.io)"
_ua_configured = False


def _ensure_ua() -> None:
    """Set the connector UA once per process (each spec runs in its own spawn)."""
    global _ua_configured
    if not _ua_configured:
        configure_http(headers={"User-Agent": _USER_AGENT})
        _ua_configured = True


class _Transient(Exception):
    """Raised for retryable HTTP responses (5xx / 429) so tenacity backs off."""


@retry(
    retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException, _Transient)),
    wait=wait_exponential(multiplier=2, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
def _http_get(url: str, *, timeout: float = 60, **kwargs) -> httpx.Response:
    """GET with retry on transient transport/5xx/429 errors. 4xx is returned
    as-is for the caller to interpret (e.g. an expected 404)."""
    _ensure_ua()
    resp = get(url, timeout=timeout, **kwargs)
    if resp.status_code == 429 or resp.status_code >= 500:
        raise _Transient(f"{resp.status_code} for {url}")
    return resp
