"""Shared HTTP client for the IBGE connector nodes.

The IBGE agregados v3 API (servicodados) is intermittently unreachable from
cloud egress IPs and silently drops the library's default datacenter
User-Agent. Both node modules (aggregates + municipios) hit the same host, so
the browser-like headers, retry policy, and JSON helper live here once.
"""

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import get


class _Transient(Exception):
    """Retryable upstream condition (5xx / overload)."""


# IBGE's servers silently drop the library's default datacenter User-Agent from
# cloud egress IPs (works from a browser-like client; the first cloud run timed
# out on every request). Present as a normal browser and accept Brazilian JSON.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


# servicodados is intermittently unreachable from cloud egress IPs — whole
# stretches of requests connect-timeout, then recover. Retry generously so a
# transient blip is absorbed *inside* one node (which keeps the orchestrator's
# consecutive-failure halt from tripping on a run-start outage). Short connect
# timeout so a dropped connection fails fast and leaves room for more attempts;
# generous read timeout because a few aggregates return large series.
_TIMEOUT = httpx.Timeout(connect=15.0, read=60.0, write=60.0, pool=15.0)


@retry(
    retry=retry_if_exception_type((_Transient, httpx.TransportError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=2, max=30),
    stop=stop_after_attempt(6),
    reraise=True,
)
def get_json(url: str):
    resp = get(url, timeout=_TIMEOUT, headers=_HEADERS)
    if resp.status_code >= 500:
        raise _Transient(f"{resp.status_code} for {url}")
    resp.raise_for_status()
    return resp.json()
