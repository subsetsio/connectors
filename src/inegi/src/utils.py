"""Shared INEGI BISE API access.

The public INEGI Indicator Bank REST API lives under
`/app/api/indicadores/desarrolladores/jsonxml/`. Both the CL_* catalog
fetchers and the long-format values stream go through the same HTTP client
and the same CL_* code-list reader, so those live here.

Auth: INEGI requires a token syntactically. The INDICATOR data endpoint does
not validate it; the CL_* catalog endpoints do. A public token embedded in
INEGI's own front-end JS authorises the catalog calls, so no personal key is
needed. `INEGI_TOKEN` overrides it if a curator ever supplies one.
"""

import os

import httpx

from subsets_utils import get, transient_retry

_BASE = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml"
# Public token embedded in INEGI's front-end JS; authorises the CL_* catalog
# endpoints. The INDICATOR data endpoint ignores it entirely.
_DEFAULT_TOKEN = "96fbd1bf-21e6-28e3-6e64-2b15999d2c89"


def _token() -> str:
    return os.environ.get("INEGI_TOKEN") or _DEFAULT_TOKEN


@transient_retry()
def _get(url: str) -> httpx.Response:
    """GET with transient-only retry. Returns the response WITHOUT raising on
    4xx — callers inspect the status code (the INEGI API uses 400/401 to mean
    'no data for this query', which is data, not a transport error)."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 429 or 500 <= resp.status_code < 600:
        resp.raise_for_status()  # surface as HTTPStatusError -> retried
    return resp


def _catalog_codes(cl_name: str) -> list:
    url = f"{_BASE}/{cl_name}/null/es/BISE/2.0/{_token()}?type=json"
    resp = _get(url)
    resp.raise_for_status()
    body = resp.json()
    codes = body.get("CODE", [])
    if not isinstance(codes, list):
        raise ValueError(f"{cl_name}: unexpected payload: {str(body)[:200]}")
    return codes
