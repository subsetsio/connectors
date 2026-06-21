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

# www.bruegel.org sits behind Cloudflare, which 403s the library's default
# User-Agent from datacenter IPs. A realistic browser header set clears it
# (verified: a bare default UA gets 403, these headers get 200). ASCII-only.
_BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.9",
}


def _curl_fetch(url: str, headers: dict | None, binary: bool):
    """Cloudflare bypass. bruegel.org's Cloudflare serves us fine from a normal
    machine but 403s the cloud runner's datacenter IP/TLS fingerprint regardless
    of User-Agent (verified: a real browser UA still 403s from CI). curl_cffi
    impersonates Chrome's TLS (JA3) handshake, which clears it. Used ONLY as the
    fallback when the logged subsets_utils path returns 403."""
    from curl_cffi import requests as cr
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    last = None
    for attempt in range(5):
        try:
            r = cr.get(url, impersonate="chrome", headers=h, timeout=180,
                       allow_redirects=True)
            if r.status_code == 200:
                return r.content if binary else r.text
            last = f"HTTP {r.status_code}"
        except Exception as e:  # curl_cffi transport error — retry with backoff
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 * (attempt + 1))
    raise AssertionError(f"curl_cffi fallback failed for {url}: {last}")


@transient_retry()
def get_bytes(url: str, headers: dict | None = None) -> bytes:
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = get(url, timeout=(10.0, 180.0), headers=h)
        resp.raise_for_status()
        return resp.content
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return _curl_fetch(url, headers, binary=True)
        raise


@transient_retry()
def get_text(url: str, headers: dict | None = None) -> str:
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    try:
        resp = get(url, timeout=(10.0, 120.0), headers=h)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return _curl_fetch(url, headers, binary=False)
        raise


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
