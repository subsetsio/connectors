"""Shared infrastructure for the Bruegel connector node modules.

Bruegel-hosted datasets resolve a point-in-time download URL by scraping the
dataset page (Cloudflare-fronted, with a Wayback fallback), then fetch and
reshape the artefact. The HTTP client, link resolution, and value-cleaning
helpers here are shared across every per-dataset node module; the per-dataset
fetch/parse/schema logic lives in the individual files under nodes/.
"""
import datetime
import re
import time

import httpx
import pandas as pd

from subsets_utils import get, post, save_raw_ndjson, transient_retry

BASE = "https://www.bruegel.org"

_FILE_RE = re.compile(
    r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip|7z))"',
    re.I,
)

# ---------------------------------------------------------------------------
# HTTP with retry/backoff on transient failures
# ---------------------------------------------------------------------------

# www.bruegel.org sits behind Cloudflare. From a normal machine a realistic
# browser header set is enough, but from the cloud runner's datacenter IP the
# www zone applies a stricter bot/WAF rule that 403s plain requests AND tarpits
# (hangs) others — verified from a real CI run: the logged httpx client (no TLS
# impersonation) *timed out*, and curl_cffi reached the file but got 403 because
# it sent no Referer and carried no Cloudflare clearance cookie. The fix below:
# (1) one warmed curl_cffi Session impersonating Chrome — the homepage GET banks
# whatever cf_* cookie Cloudflare hands out, then every fetch reuses it; (2) a
# same-origin Referer on every request (the file paths under /sites|/system are
# protected by a referer/hotlink WAF rule); (3) the curl path triggers on
# *timeouts and connect errors too*, not just HTTP 403, so the tarpitted page
# fetches fall through to it instead of retry-then-die. ASCII-only headers.
_BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": BASE + "/datasets",
}

_IMPERSONATE = "chrome124"
_curl_session = None


def _get_curl_session():
    """Lazily build a curl_cffi Session warmed against the Bruegel homepage so it
    banks any Cloudflare clearance cookie before the first real fetch. Warm-up
    failures are non-fatal — a session with browser-class TLS + the banked
    cookies is still our best shot at the www-zone WAF."""
    global _curl_session
    if _curl_session is not None:
        return _curl_session
    from curl_cffi import requests as cr
    s = cr.Session(impersonate=_IMPERSONATE, timeout=120)
    s.headers.update(_BROWSER_HEADERS)
    for warm in (BASE + "/", BASE + "/datasets"):
        try:
            s.get(warm, allow_redirects=True)
        except Exception:
            pass
    _curl_session = s
    return s


def _curl_fetch(url: str, headers: dict | None, binary: bool):
    """Fetch via the warmed curl_cffi Session (Chrome TLS + Cloudflare cookies +
    Referer). Retries non-200 and transport errors with short backoff so it stays
    inside the per-node budget instead of the old 30s-of-sleeps chain."""
    s = _get_curl_session()
    h = {"Referer": BASE + "/"}
    if headers:
        h.update(headers)
    last = None
    for attempt in range(4):
        try:
            r = s.get(url, headers=h, timeout=120, allow_redirects=True)
            if r.status_code == 200:
                return r.content if binary else r.text
            last = f"HTTP {r.status_code}"
        except Exception as e:  # curl_cffi transport error — retry with backoff
            last = f"{type(e).__name__}: {e}"
        time.sleep(1.5 * (attempt + 1))
    raise AssertionError(f"curl_cffi fetch failed for {url}: {last}")


# Failures that mean "the logged client couldn't get through" — fall to curl.
_CURL_FALLBACK_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
)


def get_bytes(url: str, headers: dict | None = None) -> bytes:
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = get(url, timeout=(10.0, 60.0), headers=h)
        resp.raise_for_status()
        return resp.content
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (403, 429) or e.response.status_code >= 500:
            return _curl_fetch(url, headers, binary=True)
        raise
    except _CURL_FALLBACK_EXC:
        return _curl_fetch(url, headers, binary=True)


def get_text(url: str, headers: dict | None = None) -> str:
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = get(url, timeout=(10.0, 60.0), headers=h)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (403, 429) or e.response.status_code >= 500:
            return _curl_fetch(url, headers, binary=False)
        raise
    except _CURL_FALLBACK_EXC:
        return _curl_fetch(url, headers, binary=False)


@transient_retry()
def post_json(url: str, body: dict):
    resp = post(url, json=body, headers={"Content-Type": "application/json"},
                timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _links_from_html(html: str) -> list[str]:
    out: list[str] = []
    for m in _FILE_RE.finditer(html):
        u = m.group(1)
        if not u.startswith("http"):
            u = BASE + u
        if u not in out:
            out.append(u)
    return out


@transient_retry()
def _wayback_html(page_url: str) -> str:
    """Fetch the latest archived copy of a dataset page from the Wayback Machine.
    archive.org is not Cloudflare-fronted, so it's reachable from the cloud runner
    even when bruegel.org 403s the runner's IP. The archived page yields a dated
    file URL; Bruegel keeps dated files live, so we then fetch that file directly
    (static assets are edge-cached and not behind the dynamic-page WAF)."""
    cdx = get("https://web.archive.org/cdx/search/cdx",
              params={"url": page_url, "output": "json", "limit": "-5",
                      "filter": "statuscode:200", "fl": "timestamp"},
              timeout=(10.0, 60.0), headers=_BROWSER_HEADERS)
    cdx.raise_for_status()
    rows = cdx.json()
    if len(rows) < 2:
        raise AssertionError(f"no Wayback snapshot for {page_url}")
    ts = rows[-1][0]
    snap = get(f"https://web.archive.org/web/{ts}id_/{page_url}",
               timeout=(10.0, 120.0), headers=_BROWSER_HEADERS)
    snap.raise_for_status()
    return snap.text


def resolve_links(page_path: str) -> list[str]:
    """Resolve a dataset's download link(s). Try the live page first (via the
    logged client, then curl_cffi); if Cloudflare blocks the runner entirely,
    fall back to the Wayback-archived page for the (dated) file URL."""
    page_url = BASE + page_path
    try:
        out = _links_from_html(get_text(page_url))
    except Exception:
        out = []
    if not out:
        out = _links_from_html(_wayback_html(page_url))
    if not out:
        raise AssertionError(f"no download link found for {page_path}")
    return out


# ---------------------------------------------------------------------------
# Value cleaning → JSON-safe natives
# ---------------------------------------------------------------------------
def clean(v):
    if v is None:
        return None
    if isinstance(v, float):
        if pd.isna(v) or v in (float("inf"), float("-inf")):
            return None
        return v
    try:
        import numpy as np
        if isinstance(v, np.floating):
            fv = float(v)
            return None if (pd.isna(fv)) else fv
        if isinstance(v, np.integer):
            return int(v)
    except Exception:
        pass
    if isinstance(v, pd.Timestamp):
        return v.date().isoformat()
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()[:10]
    if pd.isna(v):
        return None
    return v


def records(df: pd.DataFrame) -> list[dict]:
    return [{k: clean(val) for k, val in rec.items()} for rec in df.to_dict("records")]


def xlsx_link(links: list[str]) -> str:
    cand = [u for u in links if u.lower().endswith((".xlsx", ".xls"))]
    return (cand or links)[0]


def run_download(node_id: str, page_path: str | None, parser) -> None:
    """Resolve links (for Bruegel-hosted datasets), run the per-dataset parser,
    and write the tidy rows as raw NDJSON. External-source datasets pass
    page_path=None and ignore the (empty) links list."""
    links = resolve_links(page_path) if page_path else []
    rows = parser(links)
    if not rows:
        raise AssertionError(f"{node_id}: parser produced 0 rows")
    save_raw_ndjson(rows, node_id)
