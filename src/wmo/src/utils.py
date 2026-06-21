"""Shared infrastructure for the WMO / WHOS connector node files.

HTTP client + retry policy, WHOS base URLs/token, provider enumeration
(OAI-PMH), the metadata `member` paginator, and datetime parsing. Both
`nodes/stations.py` and `nodes/values.py` import from here. This module holds
NO NodeSpec definitions.

Auth: every WHOS URL carries a token in its path. We use the token embedded in
the official WHOS portal config (https://whos.geodab.eu/gs-service/whos/config.json),
which is effectively public. If calls start returning 403, re-read that config.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import get

# Public token from the official WHOS portal config.
_TOKEN = "whos-d40a452b-b865-4fbe-8165-43a96ebf1b3d"
_VIEW = "whos"
_BASE = f"https://whos.geodab.eu/gs-service/services/essi/token/{_TOKEN}/view/{_VIEW}"
_TS_URL = _BASE + "/timeseries-api/timeseries"
_WOF_URL = _BASE + "/cuahsi_1_1.asmx/GetValues"
_SITEINFO_URL = _BASE + "/cuahsi_1_1.asmx/GetSiteInfo"
_OAI_URL = _BASE + "/oaipmh"

META_PAGE = 200              # series per metadata page

_OAI_NS = {"o": "http://www.openarchives.org/OAI/2.0/"}

_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    # The WHOS broker returns persistent HTTP 500s ("Exception writing response")
    # for certain series/windows — retrying never helps, so don't burn the budget
    # on them. Only network blips and gateway/overload codes are retried;
    # persistent 500s bubble up and are skipped per-series/per-provider.
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (429, 502, 503, 504)
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=4, max=15),
    reraise=True,
)
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 45.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=4, max=15),
    reraise=True,
)
def _get_bytes(url: str, params: dict) -> bytes:
    resp = get(url, params=params, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.content


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=4, max=15),
    reraise=True,
)
def _get_text(url: str, params: dict) -> str:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _list_providers() -> list[str]:
    """Every WHOS data provider (OAI-PMH set), sorted for a deterministic crawl
    order so the stateless snapshot is reproducible."""
    specs: list[str] = []
    seen: set[str] = set()
    params = {"verb": "ListSets"}
    while True:
        root = ET.fromstring(_get_bytes(_OAI_URL, params))
        for s in root.iterfind(".//o:ListSets/o:set", _OAI_NS):
            spec = (s.findtext("o:setSpec", default="", namespaces=_OAI_NS) or "").strip()
            if spec and spec not in seen:
                seen.add(spec)
                specs.append(spec)
        token = (root.findtext(".//o:resumptionToken", default="", namespaces=_OAI_NS) or "").strip()
        if not token:
            break
        params = {"verb": "ListSets", "resumptionToken": token}
    return sorted(specs)


def _parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _to_naive_utc(value):
    dt = _parse_dt(value)
    if dt is None:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _members(provider, offset, limit):
    data = _get_json(_TS_URL, {
        "provider": provider,
        "offset": offset,
        "limit": limit,
        "includeData": "false",
    })
    return data.get("member") or []
