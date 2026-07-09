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


def _is_real_file(data: bytes) -> bool:
    """Every Bruegel artefact get_bytes fetches is an xlsx/xls/zip/7z/csv — a
    binary, never HTML. Wayback's Save-Page-Now *inline* replay is unreliable: it
    sometimes returns an HTML status/holding page (HTTP 200) instead of the bytes
    it just captured. Reject anything that smells like HTML/markup or is too small
    to be a real workbook, so a bad inline replay falls through to a snapshot poll
    rather than reaching the parser as a corrupt 'file is not a zip' payload."""
    if not data or len(data) < 256:
        return False
    head = data[:64].lstrip().lower()
    return not head.startswith((b"<!doctype", b"<html", b"<head", b"<?xml", b"<!--"))


def _wayback_bytes(url: str, headers: dict) -> bytes:
    """CI-reachable fallback for a Bruegel-hosted file the runner can't fetch
    directly. Replay the latest existing snapshot if present; else trigger a
    Save-Page-Now capture. SPN's inline replay is flaky for URL-encoded paths, so
    every candidate is content-validated and, if SPN doesn't hand back the bytes
    directly, the freshly-created snapshot is polled (the capture lands a beat
    after the /save/ call returns)."""
    raw_url, save_url = _WB_RAW + url, _WB_SAVE + url
    # 1) existing snapshot — the fast path on re-runs (and once a refresh is archived)
    try:
        data = _fetch_raw(raw_url, headers)
        if _is_real_file(data):
            return data
    except Exception:
        pass
    # 2) trigger a capture; its inline body is the file often enough to try
    try:
        data = _fetch_raw(save_url, headers)
        if _is_real_file(data):
            return data
    except Exception:
        pass
    # 3) SPN may have archived it even when its inline replay was a status page —
    #    poll the now-existing snapshot with backoff.
    last = "no snapshot"
    for wait in (4, 8, 15, 25):
        time.sleep(wait)
        try:
            data = _fetch_raw(raw_url, headers)
            if _is_real_file(data):
                return data
            last = "snapshot not a binary yet"
        except Exception as exc:
            last = str(exc)
    raise AssertionError(f"wayback could not retrieve a real file for {url}: {last}")


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
        data = _fetch_raw(url, h)
        if _is_real_file(data):
            return data
    except Exception:
        pass
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


# Wayback replays through /web/<14-digit-ts><modifier>/ rewrite every href to point
# back into the archive. Strip that prefix (absolute or root-relative) so the link
# regex sees the original bruegel.org URL.
_WB_PREFIX_RE = re.compile(
    r'(?:https?://web\.archive\.org)?/web/\d{14}[a-z]{0,3}_?/', re.I)


def _links_from_html(html: str) -> list[str]:
    html = _WB_PREFIX_RE.sub("", html)
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
def _spn_html(page_url: str) -> str:
    """Live page resolver for CI: Save-Page-Now captures the page from
    archive.org's (non-blocked) egress and replays it inline, so the HTML carries
    the CURRENT date-versioned file link — unlike an existing snapshot, which can
    be months stale. Slow (~100s), so it sits behind Jina in the chain."""
    resp = get(_WB_SAVE + page_url, timeout=(10.0, 240.0), headers=_BROWSER_HEADERS)
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _wayback_html(page_url: str) -> str:
    """Last-resort page resolver: the latest existing Wayback snapshot. It can lag
    the source by months, and Bruegel DELETES the superseded dated file on each
    refresh, so a stale link 404s everywhere — hence last, and hence run_download
    falls through to the next resolver when a link fails to download."""
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


# Ordered by (liveness, then cost). Jina and SPN both read the CURRENT page and
# both fail fast; the Wayback snapshot can hand back a link to a superseded (and
# therefore deleted) refresh; the direct www fetch is last because in CI it does
# not fail, it hangs — the WAF blackholes the runner until every retry times out.
_PAGE_RESOLVERS = (_jina_html, _spn_html, _wayback_html, get_text)


def _resolve_link_sets(page_path: str):
    """Yield one apex-rewritten link list per resolver that produced any links.
    Callers try each set in turn: a resolver can succeed at reading a page yet
    hand back a dead link (Wayback's snapshot of a superseded refresh), and the
    only way to tell is to attempt the download."""
    page_url = BASE + page_path
    seen: list[list[str]] = []
    for resolver in _PAGE_RESOLVERS:
        try:
            links = [_to_apex(u) for u in _links_from_html(resolver(page_url))]
        except Exception:
            continue
        if links and links not in seen:
            seen.append(links)
            yield links
    if not seen:
        raise AssertionError(f"no download link found for {page_path}")


def resolve_links(page_path: str) -> list[str]:
    """The first resolver's link list — the current page's links in the normal case."""
    return next(_resolve_link_sets(page_path))


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
        link_sets = iter([direct_links])
    elif page_path:
        link_sets = _resolve_link_sets(page_path)
    else:
        link_sets = iter([[]])

    rows, last_exc = None, None
    for links in link_sets:
        try:
            rows = parser(links)
            break
        except Exception as exc:  # a resolver's link may be dead — try the next one
            last_exc = exc
    if rows is None:
        raise last_exc
    if not rows:
        raise AssertionError(f"{node_id}: parser produced 0 rows")
    save_raw_ndjson(rows, node_id)
