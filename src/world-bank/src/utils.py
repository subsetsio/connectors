"""Shared HTTP + parse helpers for the World Bank connector (Indicators API,
https://api.worldbank.org/v2).

Every JSON response is a two-element array [pagination_meta, data]; we index
[0]/[1]. This module holds the transport (retry-wrapped fetch, pagination walk)
and the small parse helpers shared across the country/indicator/value node
files. It contains NO NodeSpec definitions.
"""
import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import get

BASE = "https://api.worldbank.org/v2"

_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


class _IndicatorUnavailable(Exception):
    """The data endpoint returned a single-element `message` envelope (HTTP 200)
    instead of `[meta, rows]` — the indicator was deleted/archived or is not
    queryable via the data API. Per-indicator signal: skip it, don't crash."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # The World Bank API emits spurious `400 Bad Request` under sustained
        # load instead of a proper 429 — observed mid-sweep on a URL that
        # succeeds on retry. Treat 400 as transient so a throttle hiccup doesn't
        # kill the whole node; a genuinely malformed request still fails after
        # the retry budget is exhausted (and, per-indicator, is then skipped).
        return code in (400, 429) or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(path: str, params: dict):
    """Fetch a v2 endpoint and return (meta, rows). Rows is [] when the API
    returns an empty/null data array (e.g. an indicator with no observations)."""
    p = dict(params)
    p["format"] = "json"
    resp = get(f"{BASE}/{path}", params=p, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if isinstance(payload, list) and len(payload) >= 2:
        meta, rows = payload[0], payload[1]
        return meta, (rows or [])
    # World Bank signals an unqueryable indicator with a single-element envelope
    # carrying a `message` array (still HTTP 200). Surface it as a typed skip
    # signal so the per-indicator caller can drop it rather than crash the node.
    if (
        isinstance(payload, list)
        and len(payload) == 1
        and isinstance(payload[0], dict)
        and "message" in payload[0]
    ):
        raise _IndicatorUnavailable(str(payload[0]["message"])[:200])
    raise ValueError(f"unexpected response shape for {path}: {str(payload)[:200]}")


def _fetch_all_pages(path: str, params: dict, per_page: int = 20000):
    """Walk all pages of a v2 endpoint. A generous per_page returns the whole
    result in one page for nearly every endpoint, but we honour `pages` as a
    fallback. `pages` is pinned from the first response."""
    page = 1
    out = []
    while True:
        meta, rows = _get_json(path, {**params, "per_page": per_page, "page": page})
        out.extend(rows)
        pages = int(meta.get("pages") or 1)
        if page >= pages:
            break
        page += 1
        if page > pages + 5:  # safety ceiling — source grew past expectation
            raise RuntimeError(f"{path}: pagination exceeded reported pages={pages}")
    return out


def _nested(rec: dict, key: str, field: str) -> str:
    v = rec.get(key)
    if isinstance(v, dict):
        return (v.get(field) or "").strip()
    return ""


def _to_float(s):
    if s is None or s == "":
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _indicator_rows():
    """Full indicator metadata catalog, normalised to flat dict rows. Shared by
    the `indicators` node (published as-is) and the `values` node (used as the
    id-sorted sweep catalog)."""
    records = _fetch_all_pages("indicator", {}, per_page=20000)
    rows = []
    for r in records:
        topics = r.get("topics") or []
        topic_ids = ";".join(str(t.get("id", "")).strip() for t in topics if isinstance(t, dict))
        topic_names = ";".join(str(t.get("value", "")).strip() for t in topics if isinstance(t, dict))
        rows.append({
            "id": r.get("id"),
            "name": (r.get("name") or "").strip(),
            "unit": (r.get("unit") or "").strip(),
            "source_id": _nested(r, "source", "id"),
            "source_name": _nested(r, "source", "value"),
            "source_note": (r.get("sourceNote") or "").strip(),
            "source_organization": (r.get("sourceOrganization") or "").strip(),
            "topic_ids": topic_ids,
            "topic_names": topic_names,
        })
    return rows
