"""Shared HTTP plumbing for the NFIB SBET connector.

Source: the DreamFactory stored-proc API at api.nfib-sbet.org (the only
machine-readable surface; www.nfib.com publishes only the SBET report PDF).

Request quirks (verified by probing): the proc body MUST be
application/x-www-form-urlencoded in jQuery $.param() nested form and EVERY
request MUST carry the header 'X-DreamFactory-Application-Name: sbet'. A JSON
body or a missing header returns 'Malformed request' / HTTP 500. National totals
come from empty industry/employee/statev. Each call returns the entire monthly
history (since 1986-01) in one response — no pagination.
"""

import tenacity
import httpx

from subsets_utils import post

_BASE = "https://api.nfib-sbet.org/rest/sbetdb"
_HEADERS = {
    "X-DreamFactory-Application-Name": "sbet",
    "Content-Type": "application/x-www-form-urlencoded",
}

# Span the whole corpus every refresh (no incremental query exists). maxYear is
# deliberately ahead of "now" so the current year is always covered; the source
# simply returns the months that exist.
_MIN_YEAR, _MAX_YEAR = 1986, 2035


@tenacity.retry(
    retry=tenacity.retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError)),
    wait=tenacity.wait_exponential(multiplier=2, max=60),
    stop=tenacity.stop_after_attempt(5),
    reraise=True,
)
def _proc(name, params):
    """POST a stored proc with jQuery-$.param()-style form encoding. Raises on
    transient transport/5xx errors (retried) and on a non-list payload."""
    pairs = [("app_name", "sbet")]
    for i, (n, v) in enumerate(params):
        pairs += [(f"params[{i}][name]", n),
                  (f"params[{i}][param_type]", "IN"),
                  (f"params[{i}][value]", v)]
    body = "&".join(f"{k}={v}" for k, v in pairs)
    r = post(f"{_BASE}/_proc/{name}", headers=_HEADERS, data=body, timeout=120)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list):
        raise ValueError(f"{name}: expected a JSON list, got {type(data).__name__}: {r.text[:200]}")
    return data
