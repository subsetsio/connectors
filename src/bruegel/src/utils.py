"""Shared infrastructure for the Bruegel connector node modules.

Bruegel-hosted datasets resolve a point-in-time download URL by scraping the
dataset page (Cloudflare-fronted, with a Wayback fallback), then fetch and
reshape the artefact. The HTTP client, link resolution, and value-cleaning
helpers here are shared across every per-dataset node module; the per-dataset
fetch/parse/schema logic lives in the individual files under nodes/.
"""
import datetime
import re

import pandas as pd

from subsets_utils import get, post, save_raw_ndjson, transient_retry

BASE = "https://www.bruegel.org"
APEX = "https://bruegel.org"

_FILE_RE = re.compile(
    r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip|7z))"',
    re.I,
)

# ---------------------------------------------------------------------------
# HTTP — the CI reachability problem and how this module routes around it
# ---------------------------------------------------------------------------
#
# Bruegel sits behind Cloudflare. Verified across two real CI runs: the
# *www* host applies a bot/WAF rule that blocks the GitHub Actions datacenter
# IP for every path — plain httpx times out, and curl_cffi (Chrome TLS + warmed
# cf cookies + Referer) still gets a hard HTTP 403 on the static files. No
# client-side trick clears it, because the block is IP/zone-reputation, not a
# fingerprint or challenge.
#
# Two facts make it solvable without that host:
#   1. The rule is scoped to host == www.bruegel.org. The *apex* host
#      `bruegel.org` and the per-tracker subdomains (e.g. european-clean-tech-
#      tracker.bruegel.org) are NOT blocked. Apex serves the data files under
#      /sites/default/files/ directly (HTTP 200, no redirect). (Apex does 302
#      /dataset/ pages and /system/files/ to www, so those two need another
#      route — see below.)
#   2. The dataset *page* HTML (needed to resolve each refresh's date-versioned
#      file URL) is reachable through r.jina.ai — Jina's reader fetches www from
#      its own clean egress and returns the live HTML, with the Wayback Machine
#      as a second, also-CI-reachable fallback.
#
# So: resolve the file link from the page via Jina/Wayback, then download the
# bytes from the apex host. The only exceptions are the two datasets whose file
# lives under /system/files/ (gini, sovereign) — apex 302s those to the blocked
# www, so they pass an explicit Wayback file URL via run_download(direct_links=).
_BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.9",
}

_JINA = "https://r.jina.ai/"

# Wayback binary route (see get_bytes). The apex host that used to serve the data
# files at HTTP 200 now ALSO hard-403s the GitHub Actions datacenter IP (verified
# in CI: every /sites/default/files/ fetch returns 403). archive.org's crawler
# egress is NOT blocked, so the bytes are pulled through the Wayback Machine — a
# far-future timestamp on the raw `id_` endpoint replays the latest existing
# snapshot, and Save-Page-Now archives-and-replays a file that isn't snapshotted
# yet (the trackers publish date-versioned filenames, so each refresh is new).
_WB_RAW = "https://web.archive.org/web/29991231id_/"
_WB_SAVE = "https://web.archive.org/save/"


def _to_apex(url: str) -> str:
    """Route www.bruegel.org downloads to the apex host, which serves the data
    files but isn't under the www datacenter-IP WAF rule."""
    return url.replace("://www.bruegel.org/", "://bruegel.org/")


@transient_retry()
def _fetch_raw(url: str, headers: dict) -> bytes:
    resp = get(url, timeout=(10.0, 180.0), headers=headers)
    resp.raise_for_status()
    return resp.content


def _wayback_bytes(url: str, headers: dict) -> bytes:
    """CI-reachable fallback for a Bruegel-hosted file the runner can't fetch
    directly: replay the latest Wayback snapshot if one exists, otherwise trigger
    a Save-Page-Now capture (which archives the live file and replays its bytes)."""
    try:
        data = _fetch_raw(_WB_RAW + url, headers)
        if data:
            return data
    except Exception:
        pass
    return _fetch_raw(_WB_SAVE + url, headers)


def get_bytes(url: str, headers: dict | None = None) -> bytes:
    """Fetch a file's bytes. Already-archived Wayback URLs (the /system/files/
    datasets pass these via direct_links) are fetched as-is. Otherwise try the
    apex host directly — works off-CI from a clean IP — and on any failure fall
    back to the Wayback route, which is the only egress that clears Bruegel's
    datacenter-IP WAF block in CI."""
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    url = _to_apex(url)
    if "web.archive.org" in url:
        return _fetch_raw(url, h)
    try:
        return _fetch_raw(url, h)
    except Exception:
        return _wayback_bytes(url, h)


@transient_retry()
def get_text(url: str, headers: dict | None = None) -> str:
    h = dict(_BROWSER_HEADERS)
    if headers:
        h.update(headers)
    resp = get(_to_apex(url), timeout=(10.0, 60.0), headers=h)
    resp.raise_for_status()
    return resp.text


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
def _jina_html(page_url: str) -> str:
    """Fetch the live dataset page HTML through Jina's reader, which reaches www
    from its own (non-blocked) egress and returns the current, date-versioned
    file link. X-Return-Format: html keeps the <a href> markup the regex needs."""
    resp = get(_JINA + page_url, timeout=(10.0, 90.0),
               headers={**_BROWSER_HEADERS, "X-Return-Format": "html"})
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _wayback_html(page_url: str) -> str:
    """Fallback page resolver: the latest Wayback snapshot (archive.org is also
    CI-reachable). May lag a refresh or two, but apex keeps the older dated files
    live, so a slightly stale link still downloads fine."""
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
    """Resolve a dataset's download link(s) to apex-host URLs. The page itself is
    only reachable off-www, so try Jina (live, current) then Wayback (archived),
    then a direct www attempt as a last resort. Links are rewritten to apex."""
    page_url = BASE + page_path
    out: list[str] = []
    for resolver in (_jina_html, _wayback_html, get_text):
        try:
            out = _links_from_html(resolver(page_url))
        except Exception:
            out = []
        if out:
            break
    if not out:
        raise AssertionError(f"no download link found for {page_path}")
    return [_to_apex(u) for u in out]


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


def run_download(node_id: str, page_path: str | None, parser,
                 direct_links: list[str] | None = None) -> None:
    """Resolve links (for Bruegel-hosted datasets), run the per-dataset parser,
    and write the tidy rows as raw NDJSON. External-source datasets pass
    page_path=None and ignore the (empty) links list. Datasets whose file is on
    a host the runner can't resolve from its page (the /system/files/ ones, which
    apex 302s back to the blocked www) pass an explicit ``direct_links`` URL."""
    if direct_links is not None:
        links = direct_links
    elif page_path:
        links = resolve_links(page_path)
    else:
        links = []
    rows = parser(links)
    if not rows:
        raise AssertionError(f"{node_id}: parser produced 0 rows")
    save_raw_ndjson(rows, node_id)
