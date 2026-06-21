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
that with a fixed parquet schema, each subset's raw is written as line-delimited
JSON with every value kept as a string; the SQL transform publishes one Delta
table per subset and downstream typing is a curation concern.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import datetime, timezone
from urllib.parse import unquote, urljoin, quote

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer, transient_retry
from constants import CATALOG

DADOSABERTOS_BASE = "https://sistemas.anac.gov.br/dadosabertos/"
SAS_BASE = "https://sas.anac.gov.br/sas/"
AIRFARES_START_YEAR = 2002  # documented floor for the domestic fare series
HTTP_TIMEOUT = 600
MAX_CRAWL_DEPTH = 8
_HREF_RE = re.compile(r'href="([^"?#]+)"', re.IGNORECASE)


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
# --------------------------------------------------------------------------- #
def _write_ndjson(asset: str, items: list[tuple[str, bool]]) -> None:
    total = 0
    fetched = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for url, optional in items:
            r = _http_get_optional(url) if optional else _http_get(url)
            if r is None:
                continue
            fetched += 1
            for rec in _parse_csv(r.content):
                out.write(json.dumps(rec, ensure_ascii=False))
                out.write("\n")
                total += 1
    if total == 0:
        raise RuntimeError(
            f"{asset}: parsed 0 rows from {fetched} fetched file(s) "
            f"({len(items)} candidates)"
        )


def fetch_one(node_id: str) -> None:
    eid = node_id[len("anac-"):]
    desc = CATALOG[eid]
    kind = desc["kind"]
    if kind == "airfares":
        items = _airfare_items(desc["sub"])
    elif kind == "file":
        items = [(_pick_file(desc["path"], desc["match"]), False)]
    elif kind == "dir":
        items = [(u, False) for u in _dir_csvs(desc["path"])]
    elif kind == "tree":
        items = [(u, False) for u in _tree_csvs(desc["path"])]
    else:
        raise ValueError(f"{node_id}: unknown catalog kind {kind!r}")
    if not items:
        raise RuntimeError(f"{node_id}: no CSV files discovered for {desc}")
    _write_ndjson(node_id, items)


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
