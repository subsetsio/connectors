"""Shared HTTP/session helpers for the RBI (Reserve Bank of India) DBIE connector.

Auth: per-request session, not an API key. Prime the F5 cookie by GETting the
SPA, POST security_generateSessionToken (channelkey:key1) to get a session id
from the response 'authorization' header, then send that id on every data call
(channelkey:key1; the bundled JS says key2 but key2 returns 4311). Responses
are HTML-entity-encoded JSON served as text/plain.
"""

import html
import json

from subsets_utils import get, post, transient_retry

_GATEWAY = "https://data.rbi.org.in/CIMS_Gateway_DBIE/GATEWAY/SERVICES"
_PORTAL = "https://data.rbi.org.in/DBIE/"
_BASE_HEADERS = {
    "Content-Type": "application/json",
    "datatype": "application/json",
    "channelkey": "key1",
    "Origin": "https://data.rbi.org.in",
    "Referer": _PORTAL,
}


def _clean(s):
    """Strip the non-breaking spaces and trailing padding RBI pads strings with."""
    if s is None:
        return None
    return s.replace(" ", " ").strip()


@transient_retry()
def _open_session() -> dict:
    """Prime the F5 cookie and mint a session id; return headers with it set.

    Cookies persist on the shared subsets_utils httpx client within this
    process, so the subsequent data POSTs reuse the primed cookie jar.
    """
    r0 = get(_PORTAL, timeout=(10.0, 60.0))
    r0.raise_for_status()
    r1 = post(
        f"{_GATEWAY}/security_generateSessionToken",
        headers=_BASE_HEADERS,
        content=b'{"body":{}}',
        timeout=(10.0, 60.0),
    )
    r1.raise_for_status()
    sid = r1.headers.get("authorization")
    if not sid:
        raise RuntimeError("no session id returned by security_generateSessionToken")
    headers = dict(_BASE_HEADERS)
    headers["authorization"] = sid
    return headers


@transient_retry()
def _call(endpoint: str, body: dict, headers: dict) -> dict:
    """POST one gateway endpoint and return the decoded JSON body envelope's body."""
    r = post(
        f"{_GATEWAY}/{endpoint}",
        headers=headers,
        content=json.dumps({"body": body}).encode("utf-8"),
        timeout=(10.0, 120.0),
    )
    r.raise_for_status()
    # HTML-entity-encoded JSON served as text/plain (ISO-8859-1); round-trip
    # through utf-8/replace to absorb any lone surrogates from malformed entities.
    text = html.unescape(r.text).encode("utf-8", "replace").decode("utf-8")
    payload = json.loads(text)
    status = payload.get("header", {}).get("status")
    if status != "success":
        raise RuntimeError(
            f"{endpoint} returned status={status}: {payload.get('header', {}).get('errorMessage')}"
        )
    return payload.get("body", {})
