"""ANAC (Brazil) open-data connector.

Two fetch surfaces, both bulk CSV with no incremental filter, so every refresh
is a full re-pull (monthly-partitioned series simply gain a new file and are
re-crawled):

  * dadosabertos — the nginx autoindex tree at
    https://sistemas.anac.gov.br/dadosabertos/ . Directory URLs return an HTML
    listing of <a href> links (sub-dirs end in '/', leaves are .csv). Each
    accepted subset maps to a single file, a directory of files, or a
    year/month-partitioned tree (see src/constants.py CATALOG).
  * airfares — commercialized fare microdata at
    https://sas.anac.gov.br/sas/{tarifadomestica|tarifainternacional}/<yyyy>/<yyyymm>.csv
    whose directory index is not scrapeable, so files are discovered by probing
    each year/month from 2002 to the current month and skipping 404s.

ANAC CSVs are messy: a leading "Atualizado em: <date>" preamble line before the
header, semicolon delimiters, mixed latin-1/utf-8 encodings, and decimal commas.
Column sets and types also drift across a series' yearly files. Rather than fight
that with a fixed parquet schema, each source CSV is written as line-delimited
JSON with every value kept as a string; the SQL transform publishes one Delta
table per subset and downstream typing is a curation concern. (DuckDB's
read_json_auto unions columns by name across the per-file shards, so drift is
absorbed at read time.)

Fetching is the hard part: ANAC's host throttles each connection to ~0.18 MB/s,
so the partitioned series (airport movements, VRA, airfares) are multi-GB and a
single sequential fetch cannot finish inside one cloud run's time budget. Three
things make every node completable regardless of size:
  * concurrency — files are pulled `_CONCURRENCY` at a time, multiplying the
    per-connection throughput (the throttle is per-connection, not per-IP);
  * sharded raw — each source file lands as its own run-scoped raw object
    `<node>.sNNNNN.ndjson.gz`. The transform globs `<node>.*` and unions them,
    and each shard is an atomic PUT, so an interrupted run never leaves a
    half-written asset;
  * cooperative continuation — a node processes work until a wall-clock budget,
    persists which shards are done to state, and returns True to ask the runner
    for a continuation. Already-done shards are skipped (idempotent via
    `raw_asset_exists`), so each continuation makes monotonic forward progress.
"""
from __future__ import annotations

import csv
import json
import os
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import unquote, urljoin, quote

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    load_state,
    raw_asset_exists,
    raw_writer,
    save_state,
    transient_retry,
)
from constants import CATALOG

DADOSABERTOS_BASE = "https://sistemas.anac.gov.br/dadosabertos/"
SAS_BASE = "https://sas.anac.gov.br/sas/"
AIRFARES_START_YEAR = 2002  # documented floor for the domestic fare series
MAX_CRAWL_DEPTH = 8
_HREF_RE = re.compile(r'href="([^"?#]+)"', re.IGNORECASE)

# Per-request timeout. The host serves ~0.18 MB/s but streams continuously, so a
# generous read gap (90s) tolerates the slow drip while still tripping a genuine
# stall fast enough for transient_retry to recover. A single scalar timeout
# (e.g. 600) would let a stalled socket hang for the full window.
HTTP_TIMEOUT = httpx.Timeout(connect=15.0, read=90.0, write=90.0, pool=15.0)

# How many files to pull at once. The throttle is per-connection (measured:
# 4 connections → 4x aggregate throughput), so this multiplies download speed.
# Capped low enough that `_CONCURRENCY` in-flight files stay within runner RAM.
_CONCURRENCY = 8

# Wall-clock budget per node invocation. On expiry the node persists progress
# and returns True for a continuation. Sharded writes + per-chunk state
# checkpointing make a hard SIGTERM at the run's deadline cheap (at most one
# in-flight chunk is lost), so this is set high to let even the largest series
# (VRA, airfares) finish within a single run rather than burning extra
# continuation windows — each of which carries heavy CI queue overhead.
_INVOCATION_BUDGET_S = 120 * 60


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
@transient_retry()
def _http_get(url: str):
    """GET a required resource. raise_for_status() turns 429/5xx into retries
    (via transient_retry) and 4xx into a hard failure."""
    r = get(url, timeout=HTTP_TIMEOUT)
    if r.status_code >= 400:
        r.raise_for_status()
    return r


@transient_retry()
def _http_get_optional(url: str):
    """GET a resource that may legitimately be absent (404 -> None)."""
    r = get(url, timeout=HTTP_TIMEOUT)
    if r.status_code == 404:
        return None
    if r.status_code >= 400:
        r.raise_for_status()
    return r


def _enc_path(path: str) -> str:
    """Percent-encode each path segment (keeping the slashes)."""
    return "/".join(quote(seg) for seg in path.split("/"))


def _dir_url(path: str) -> str:
    return DADOSABERTOS_BASE + _enc_path(path) + "/"


# --------------------------------------------------------------------------- #
# nginx autoindex crawling
# --------------------------------------------------------------------------- #
def _list_dir(dir_url: str) -> tuple[list[str], list[str]]:
    """Return (subdir_urls, csv_file_urls) directly under an autoindex dir."""
    r = _http_get(dir_url)
    subdirs, files = [], []
    for href in _HREF_RE.findall(r.text):
        if href.startswith(("../", "/", "http://", "https://")):
            continue
        full = urljoin(dir_url, href)
        if href.endswith("/"):
            subdirs.append(full)
        elif unquote(href).lower().endswith(".csv"):
            files.append(full)
    return subdirs, files


def _dir_csvs(path: str) -> list[str]:
    _, files = _list_dir(_dir_url(path))
    return files


def _tree_csvs(path: str) -> list[str]:
    """All .csv leaves anywhere under `path` (depth-limited BFS)."""
    out: list[str] = []
    frontier = [(_dir_url(path), 0)]
    seen: set[str] = set()
    while frontier:
        url, depth = frontier.pop()
        if url in seen:
            continue
        seen.add(url)
        subdirs, files = _list_dir(url)
        out.extend(files)
        if depth >= MAX_CRAWL_DEPTH:
            if subdirs:
                raise RuntimeError(
                    f"crawl depth {MAX_CRAWL_DEPTH} exceeded under {path!r} — "
                    "unexpected directory nesting"
                )
            continue
        frontier.extend((s, depth + 1) for s in subdirs)
    return out


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _pick_file(path: str, match: str) -> str:
    """Select the one CSV in `path` whose name contains the ASCII `match`
    token — for directories that hold several distinct datasets."""
    files = _dir_csvs(path)
    token = _norm(match)
    hits = [u for u in files if token in _norm(unquote(u.rsplit("/", 1)[-1]))]
    if len(hits) != 1:
        raise RuntimeError(
            f"file match {match!r} under {path!r} matched {len(hits)} files "
            f"(expected 1); candidates={[unquote(u.rsplit('/', 1)[-1]) for u in files]}"
        )
    return hits[0]


def _airfare_items(sub: str) -> list[tuple[str, bool]]:
    now = datetime.now(timezone.utc)
    items: list[tuple[str, bool]] = []
    for year in range(AIRFARES_START_YEAR, now.year + 1):
        last_month = 12 if year < now.year else now.month
        for month in range(1, last_month + 1):
            url = f"{SAS_BASE}{sub}/{year}/{year}{month:02d}.csv"
            items.append((url, True))  # optional: months before data starts 404
    return items


# --------------------------------------------------------------------------- #
# CSV parsing (string-typed rows)
# --------------------------------------------------------------------------- #
def _decode(content: bytes) -> str:
    try:
        return content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def _detect_delim(lines: list[str]) -> str:
    best, best_count = ";", 0
    for line in lines[:50]:
        for d in (";", ",", "\t", "|"):
            c = line.count(d)
            if c > best_count:
                best, best_count = d, c
    return best


def _find_header(lines: list[str], delim: str):
    for i, line in enumerate(lines):
        if line.count(delim) >= 1:
            return i
    return None


def _dedupe_header(header: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for i, h in enumerate(header):
        name = (h or "").strip().lstrip("﻿") or f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out


def _parse_csv(content: bytes):
    """Yield one dict per data row, all values as strings. Skips the ANAC
    'Atualizado em' preamble by locating the first delimited line as the
    header."""
    text = _decode(content)
    lines = text.splitlines()
    if not lines:
        return
    delim = _detect_delim(lines)
    start = _find_header(lines, delim)
    if start is None:
        return
    reader = csv.reader(lines[start:], delimiter=delim)
    try:
        raw_header = next(reader)
    except StopIteration:
        return
    header = _dedupe_header(raw_header)
    width = len(header)
    for row in reader:
        if not any(cell.strip() for cell in row):
            continue
        yield {header[i]: (row[i] if i < len(row) else None) for i in range(width)}


# --------------------------------------------------------------------------- #
# Download node — one generic fetcher for every entity
#
# Each source CSV is a shard: raw object `<node>.sNNNNN.ndjson.gz`. Shards are
# fetched `_CONCURRENCY` at a time, the index→url map is pinned in run-scoped
# state, and a node returns True (continuation) when it runs out of wall-clock
# budget before finishing. Idempotency is anchored on `raw_asset_exists`, so a
# continuation (or a crash-and-resume) re-checks rather than re-downloads.
# --------------------------------------------------------------------------- #
def _discover_items(desc: dict) -> list[tuple[str, bool]]:
    """Enumerate (url, optional) for an entity, in a stable sorted order so the
    shard index of a given file is the same across continuations."""
    kind = desc["kind"]
    if kind == "airfares":
        return _airfare_items(desc["sub"])  # already chronological / stable
    if kind == "file":
        return [(_pick_file(desc["path"], desc["match"]), False)]
    if kind == "dir":
        return [(u, False) for u in sorted(_dir_csvs(desc["path"]))]
    if kind == "tree":
        return [(u, False) for u in sorted(_tree_csvs(desc["path"]))]
    raise ValueError(f"unknown catalog kind {kind!r}")


def _shard_id(node_id: str, idx: int) -> str:
    # The '.' keeps these under the transform's primary `<node>.*` glob while
    # staying collision-safe against sibling node ids (which use '-').
    return f"{node_id}.s{idx:05d}"


def _fetch_shard(node_id: str, idx: int, url: str, optional: bool) -> int:
    """Fetch one source file into its shard. Idempotent: an existing shard is a
    no-op, and an absent optional file (404) resolves without writing. Returns
    the shard index so the caller can mark it resolved."""
    shard = _shard_id(node_id, idx)
    if raw_asset_exists(shard, "ndjson.gz"):
        return idx
    r = _http_get_optional(url) if optional else _http_get(url)
    if r is None:  # optional file genuinely absent — resolved, nothing to write
        return idx
    with raw_writer(shard, "ndjson.gz", mode="wt", compression="gzip") as out:
        for rec in _parse_csv(r.content):
            out.write(json.dumps(rec, ensure_ascii=False))
            out.write("\n")
    return idx


def fetch_one(node_id: str):
    """Resumable, concurrent, budgeted fetch. Returns True to request a
    continuation when work remains, else None when the entity is complete."""
    eid = node_id[len("anac-"):]
    desc = CATALOG[eid]
    run_id = os.environ.get("RUN_ID", "")

    # Pin the index→url map for this run so shard indices are stable across
    # continuations. State is connector-scoped (persists across runs), so it is
    # keyed by run_id; a fresh run re-discovers (picking up new monthly files).
    st = load_state(node_id)
    if st.get("run_id") != run_id or "urls" not in st:
        items = _discover_items(desc)
        if not items:
            raise RuntimeError(f"{node_id}: no CSV files discovered for {desc}")
        st = {
            "run_id": run_id,
            "urls": [u for u, _ in items],
            "optional": [bool(o) for _, o in items],
            "resolved": [],
        }
        save_state(node_id, st)

    urls = st["urls"]
    optional = st["optional"]
    resolved = set(st.get("resolved", []))
    pending = [i for i in range(len(urls)) if i not in resolved]
    if not pending:
        return None

    deadline = time.monotonic() + _INVOCATION_BUDGET_S
    i = 0
    with ThreadPoolExecutor(max_workers=_CONCURRENCY) as ex:
        while i < len(pending) and time.monotonic() < deadline:
            chunk = pending[i:i + _CONCURRENCY]
            i += len(chunk)
            futs = [
                ex.submit(_fetch_shard, node_id, idx, urls[idx], optional[idx])
                for idx in chunk
            ]
            for fut in futs:
                resolved.add(fut.result())  # propagate exceptions → node fails
            # Checkpoint after every chunk so a SIGTERM/OOM loses at most one
            # chunk of probing (the shards themselves are already durable).
            st["resolved"] = sorted(resolved)
            save_state(node_id, st)

    if len(resolved) < len(urls):
        return True  # more files remain — ask the runner for a continuation
    return None


DOWNLOAD_SPECS = [
    NodeSpec(id=f"anac-{eid}", fn=fetch_one, kind="download")
    for eid in CATALOG
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"anac-{eid}-transform",
        deps=(f"anac-{eid}",),
        sql=f'SELECT * FROM "anac-{eid}"',
    )
    for eid in CATALOG
]
