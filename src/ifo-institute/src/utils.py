"""Shared HTTP + parsing helpers for the ifo Institute connector.

The site has no JSON/REST API; we fetch published XLSX file objects under
``/sites/default/files/`` and parse their human-oriented sheets in Python.

Access hazard: the site's *dynamic HTML* (the index page) sits behind a Fastly
"Client Challenge" bot-protection that hard-blocks datacenter IPs (a cloud run
gets a 3 KB JS interstitial instead of the page). The *static file objects* are
CDN-cached assets and are fetched directly — we deliberately do NOT scrape the
index. Any non-XLSX (non-``PK``) 200 body is treated as a challenge → transient
→ retried with backoff; a 404/403 just means that file isn't published yet.
"""

import datetime as dt
import re

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import get

INDEX_URL = "https://www.ifo.de/en/ifo-time-series"
BASE = "https://www.ifo.de"
FILES = BASE + "/sites/default/files/"

# Browser-like identity — the bare default UA trips the bot challenge faster.
# Fuller header set so the request looks like a real navigation. ASCII-only
# (httpx rejects non-ASCII header values).
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": INDEX_URL,
    "Upgrade-Insecure-Requests": "1",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
}
THROTTLE_S = 3.0  # polite gap between requests to the same host


# --------------------------------------------------------------------------- #
# HTTP — retried, with bot-challenge detection
# --------------------------------------------------------------------------- #
class _Transient(Exception):
    """A retryable condition (network blip, 429/5xx, or a bot-challenge body)."""


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
    if isinstance(exc, (_Transient,) + _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=5, max=120),
    reraise=True,
)
def get_xlsx(url: str) -> tuple[int, bytes | None]:
    """GET a static xlsx object.

    Returns ``(200, content)`` on success, or ``(status, None)`` for 403/404 —
    the ``secure/timeseries`` path returns 403 (not 404) for an object that
    isn't published yet, so both mean "not present, try another month". A
    non-XLSX 200 body is a Fastly challenge interstitial → transient → retried
    with backoff. 5xx/429 and network errors are also transient.
    """
    resp = get(url, timeout=(15.0, 120.0))
    if resp.status_code in (403, 404):
        return resp.status_code, None
    resp.raise_for_status()
    content = resp.content
    if content[:2] != b"PK":
        raise _Transient(
            f"non-xlsx body for {url} "
            f"({len(content)}B, {resp.headers.get('content-type')}) — bot challenge?"
        )
    return 200, content


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #
def parse_month(v) -> dt.date | None:
    """Coerce a cell to the first-of-month date, or None if not a date."""
    if v is None:
        return None
    if isinstance(v, dt.datetime):
        return dt.date(v.year, v.month, 1)
    if isinstance(v, dt.date):
        return dt.date(v.year, v.month, 1)
    s = str(v).strip()
    if not s:
        return None
    m = re.match(r"^(\d{1,2})/(\d{4})$", s)  # "01/2005"
    if m:
        return dt.date(int(m.group(2)), int(m.group(1)), 1)
    for fmt in ("%B %Y", "%b %Y"):  # "January 2005"
        try:
            d = dt.datetime.strptime(s, fmt)
            return dt.date(d.year, d.month, 1)
        except ValueError:
            pass
    return None


def to_float(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s or s in {"-", ".", "n/a", "NA", "na"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def sheet_rows(ws) -> list[list]:
    return [list(r) for r in ws.iter_rows(values_only=True)]
