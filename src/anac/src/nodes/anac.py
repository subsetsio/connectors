"""ANAC (Brazil) open-data connector — raw fetches.

Two fetch surfaces, both bulk CSV with no incremental filter, so every refresh is
a full re-pull (a monthly-partitioned series simply gains a new file and is
re-crawled):

  * dadosabertos — the nginx autoindex tree at
    https://sistemas.anac.gov.br/dadosabertos/ . A directory URL returns an HTML
    listing of <a href> links (sub-dirs end in '/', leaves are .csv). Each
    accepted entity resolves to a set of leaf CSVs; see src/constants.py for the
    per-entity fetch descriptor and how overlapping datasets in one directory are
    told apart.
  * airfares — commercialized fare microdata at
    https://sas.anac.gov.br/sas/{tarifadomestica|tarifainternacional}/<yyyy>/<yyyymm>.csv .
    That host serves no directory index, so the months are enumerated from
    AIRFARES_START_YEAR to the current month and absent ones (404) are skipped.

Raw format. ANAC's CSVs are messy: a leading "Atualizado em: <date>" preamble
before the header, semicolon delimiters, mixed latin-1/utf-8, decimal commas, and
column sets that drift across a series' yearly files. Rather than force a fixed
parquet schema onto that, every source CSV is written as line-delimited JSON with
each value kept as a string; typing is left to the model/transform layer.

Sharding. One source CSV becomes one *fragment* of the entity's raw asset
(`save_raw_*`/`raw_writer`'s `fragment=` kwarg). Fragments commit independently
and the transform's dep view spans them all, so an interrupted run never leaves a
half-written asset and a continuation leg resumes on the fragments the raw
manifest says are already committed for this RUN_ID. The node itself sets no
wall-clock budget: it drains its file list and the orchestrator interrupts it if
the run nears its CI limit, which is safe precisely because each fragment is
durable the moment it lands.

Column padding. The runtime reads an ndjson asset with DuckDB's
`read_json_auto([...all fragments...])`, which fixes its schema from the first
files it samples — a column that appears only in a later fragment would be
dropped silently. So a multi-file entity first probes each file's header (a
ranged GET of the first bytes) and pads every row to the union, making all
fragments of one asset column-compatible.

Throughput. The host is slow (single-digit KB/s per connection at times) and
truncates large bodies. Files are therefore pulled `_CONCURRENCY` at a time — the
throttle is per-connection, not per-IP — and each body is fetched in ranged
chunks and length-checked against Content-Length, so a silently truncated
response raises instead of committing a short fragment.
"""
from __future__ import annotations

import csv
import json
import os
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import quote, unquote, urljoin

import httpx

from constants import CATALOG, FAMILIES
from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    load_state,
    raw_writer,
    save_state,
    transient_retry,
)

STATE_VERSION = 1

DADOSABERTOS_BASE = "https://sistemas.anac.gov.br/dadosabertos/"
SAS_BASE = "https://sas.anac.gov.br/sas/"
AIRFARES_START_YEAR = 2002  # documented floor of the domestic fare series
MAX_CRAWL_DEPTH = 8
RAW_EXT = "ndjson.gz"

_HREF_RE = re.compile(r'href="([^"?#]+)"', re.IGNORECASE)
_YEAR_RE = re.compile(r"^(19|20)\d{2}$")
# A vintage token: 2024, 202412, or 122025 (ANAC writes SISANT_<mm><yyyy>.csv).
_DATE_TOKEN_RE = re.compile(r"^((19|20)\d{2}(\d{2})?|\d{2}(19|20)\d{2})$")
_TRAILING_YEAR_RE = re.compile(r"^(.*?[a-z])((19|20)\d{2})$")

# The host streams slowly but continuously, so a generous read gap tolerates the
# drip while still tripping a genuinely stalled socket fast enough for
# transient_retry to recover it. A single scalar timeout would let a dead socket
# hang for the whole window.
HTTP_TIMEOUT = httpx.Timeout(connect=15.0, read=120.0, write=120.0, pool=15.0)

# Bodies are pulled in ranged chunks: the host closes large responses early, so a
# whole-file GET of a multi-MB object routinely dies mid-body. Each chunk is
# retried on its own and the assembled length is checked against the object's
# declared size, so a truncated transfer fails the node instead of silently
# committing a short fragment. Sized so a chunk still completes on a slow
# connection; if the host degrades far below that the node fails loudly, which is
# the outcome we want.
_CHUNK_BYTES = 1024 * 1024

# The throttle is per-connection, so concurrency multiplies aggregate throughput.
# Held low enough that `_CONCURRENCY` in-flight files stay inside runner RAM.
_CONCURRENCY = 8


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
@transient_retry()
def _http_get(url: str) -> httpx.Response:
    """GET a required resource. raise_for_status turns 429/5xx into retries and
    4xx into a hard failure."""
    r = get(url, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r


@transient_retry()
def _http_probe(url: str) -> httpx.Response | None:
    """Probe an object for its size, tolerating legitimate absence (404 -> None).

    subsets_utils exposes no head(); a 0-0 ranged GET is the cheap equivalent and
    additionally proves the server honours Range on this object.
    """
    r = get(url, headers={"Range": "bytes=0-0"}, timeout=HTTP_TIMEOUT)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r


@transient_retry()
def _http_get_range(url: str, start: int, end: int) -> bytes:
    """GET one inclusive byte range, verifying the server returned all of it.

    ANAC declares a Content-Length and then closes the connection early on large
    objects. A short chunk is a transient truncation, not a valid body, so raise
    to let transient_retry re-issue just this chunk.
    """
    r = get(url, headers={"Range": f"bytes={start}-{end}"}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    if r.status_code != 206:
        # Range was ignored and the whole body came back. Only the first window
        # can consume that; appending it at a non-zero offset would corrupt.
        if start:
            raise RuntimeError(f"{url}: server ignored Range at offset {start}")
        return r.content
    want = end - start + 1
    if len(r.content) != want:
        raise httpx.RemoteProtocolError(
            f"short range {start}-{end} for {url}: got {len(r.content)} of {want} bytes"
        )
    return r.content


def _fetch_body(url: str, optional: bool = False) -> bytes | None:
    """Fetch a whole object in ranged chunks. None when `optional` and absent."""
    probe = _http_probe(url)
    if probe is None:
        if optional:
            return None
        raise RuntimeError(f"required object missing: {url}")

    total = _content_total(probe)
    if total is None:
        # No length advertised — one shot, nothing to length-check against.
        return _http_get(url).content

    buf = bytearray()
    while len(buf) < total:
        end = min(len(buf) + _CHUNK_BYTES, total) - 1
        buf += _http_get_range(url, len(buf), end)
    if len(buf) != total:
        raise RuntimeError(f"{url}: assembled {len(buf)} bytes, expected {total}")
    return bytes(buf)


def _content_total(resp: httpx.Response) -> int | None:
    """Total object size from a ranged response's Content-Range, else None."""
    cr = resp.headers.get("content-range", "")
    m = re.match(r"bytes \d+-\d+/(\d+)$", cr)
    if m:
        return int(m.group(1))
    cl = resp.headers.get("content-length")
    return int(cl) if cl and resp.status_code == 200 else None


def _enc_path(path: str) -> str:
    """Percent-encode each path segment, keeping the slashes."""
    return "/".join(quote(seg) for seg in path.split("/"))


def _dir_url(path: str) -> str:
    return DADOSABERTOS_BASE + _enc_path(path) + "/"


# --------------------------------------------------------------------------- #
# nginx autoindex crawling
# --------------------------------------------------------------------------- #
def _list_dir(dir_url: str) -> tuple[list[str], list[str]]:
    """(subdir_urls, csv_file_urls) directly under one autoindex directory."""
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


def _tree_csvs(root_urls: list[str]) -> list[str]:
    """Every .csv leaf anywhere under the given roots (depth-limited BFS)."""
    out: list[str] = []
    frontier = [(u, 0) for u in root_urls]
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
                    f"crawl depth {MAX_CRAWL_DEPTH} exceeded at {url} — "
                    "unexpected directory nesting"
                )
            continue
        frontier.extend((s, depth + 1) for s in subdirs)
    return out


# --------------------------------------------------------------------------- #
# Entity -> file-set resolution
# --------------------------------------------------------------------------- #
def _slug(s: str) -> str:
    """The collect stage's identifier normalization. Non-ASCII is DROPPED, not
    replaced: ANAC serves some filenames in latin-1, which decode to U+FFFD, and
    dropping them is what makes `Fila_Inspe<?><?>o_Seguran<?>a` a different
    family from `Fila_Inspecao_Seguranca` — they are different datasets."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = "".join(c for c in s if c.isascii())
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def _strip_date_tokens(fslug: str) -> str:
    """Drop the leading/trailing date tokens a file stem carries per vintage, so
    `2021_Atendimento_PNAE`, `SISANT_122025` and `dadosconsumidor2025` all reduce
    to their family."""
    toks = [t for t in fslug.split("-") if t]
    while toks and _DATE_TOKEN_RE.match(toks[0]):
        toks.pop(0)
    while toks and _DATE_TOKEN_RE.match(toks[-1]):
        toks.pop()
    if toks and all(t.isdigit() for t in toks):
        return ""  # the whole stem was a date, e.g. Historico_RAB/2026-06.csv
    if toks:
        m = _TRAILING_YEAR_RE.match(toks[-1])
        if m:
            toks[-1] = m.group(1)
    return "-".join(toks)


def _family_of(file_url: str, families: list[str]) -> str | None:
    """The longest family that prefixes this file's date-stripped stem.

    Longest wins so `Ciac_cursos.csv` goes to `ciac-cursos` and not `ciac`, and
    `tfacmicro.csv` to `tfacmicro` and not `tfac`.
    """
    stem = unquote(file_url.rsplit("/", 1)[-1])[: -len(".csv")]
    fs = _strip_date_tokens(_slug(stem))
    best = None
    for fam in families:
        if fs == fam or fs.startswith(fam + "-"):
            if best is None or len(fam) > len(best):
                best = fam
    return best


def _airfare_items(sub: str) -> list[tuple[str, bool]]:
    """Every <yyyy>/<yyyymm>.csv from the series floor to the current month.
    All optional: months before a series starts, and the not-yet-published
    current month, both 404."""
    now = datetime.now(timezone.utc)
    items: list[tuple[str, bool]] = []
    for year in range(AIRFARES_START_YEAR, now.year + 1):
        last_month = 12 if year < now.year else now.month
        for month in range(1, last_month + 1):
            items.append((f"{SAS_BASE}{sub}/{year}/{year}{month:02d}.csv", True))
    return items


def _discover_items(desc: dict) -> list[tuple[str, bool]]:
    """(url, optional) for every source file of one entity, in a stable order."""
    kind = desc["kind"]
    if kind == "airfares":
        return _airfare_items(desc["sub"])

    if kind == "family":
        _, files = _list_dir(_dir_url(desc["path"]))
        fams = FAMILIES[desc["path"]]
        keep = [u for u in files if _family_of(u, fams) == desc["family"]]
        if not keep:
            raise RuntimeError(
                f"family {desc['family']!r} matched no CSV in {desc['path']!r} — "
                "the directory's file naming changed; re-run collect"
            )
        return [(u, False) for u in sorted(keep)]

    if kind == "dir":
        _, files = _list_dir(_dir_url(desc["path"]))
        return [(u, False) for u in sorted(files)]

    if kind == "partitioned":
        subdirs, _ = _list_dir(_dir_url(desc["path"]))
        # Only four-digit-year subdirs: a non-year sibling is a separate collect
        # entity (accept rejected `reuniao-deliberativa-eletronica`), and pulling
        # it here would smuggle a rejected dataset into this asset.
        years = [
            u for u in subdirs
            if _YEAR_RE.match(unquote(u.rstrip("/").rsplit("/", 1)[-1]))
        ]
        if not years:
            raise RuntimeError(f"no year partitions under {desc['path']!r}")
        return [(u, False) for u in sorted(_tree_csvs(years))]

    raise ValueError(f"unknown catalog kind {desc['kind']!r}")


# --------------------------------------------------------------------------- #
# CSV parsing — every value kept as a string
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


def _find_header(lines: list[str], delim: str) -> int | None:
    """The first delimited line — skips ANAC's "Atualizado em: <date>" preamble."""
    for i, line in enumerate(lines):
        if line.count(delim) >= 1:
            return i
    return None


def _dedupe_header(header: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for i, h in enumerate(header):
        name = (h or "").strip().lstrip("﻿") or f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out


def _header_of(content: bytes) -> list[str]:
    text = _decode(content)
    lines = text.splitlines()
    if not lines:
        return []
    delim = _detect_delim(lines)
    start = _find_header(lines, delim)
    if start is None:
        return []
    try:
        return _dedupe_header(next(csv.reader(lines[start:], delimiter=delim)))
    except StopIteration:
        return []


def _iter_rows(content: bytes):
    """One dict per data row, all values strings."""
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
        header = _dedupe_header(next(reader))
    except StopIteration:
        return
    width = len(header)
    for row in reader:
        if not any(cell.strip() for cell in row):
            continue
        yield {header[i]: (row[i] if i < len(row) else None) for i in range(width)}


@transient_retry()
def _fetch_header(url: str, optional: bool) -> list[str]:
    """Read just enough of a CSV to see its preamble and header."""
    r = get(url, headers={"Range": "bytes=0-65535"}, timeout=HTTP_TIMEOUT)
    if optional and r.status_code == 404:
        return []
    r.raise_for_status()
    return _header_of(r.content)


def _header_union(node_id: str, items: list[tuple[str, bool]], run_id: str) -> list[str]:
    """Stable union of every file's header, in first-seen order.

    Cached in state for the duration of one run. The union has to be taken over
    *all* files, not just the pending ones — fragments committed by an earlier
    leg were padded to it — so an uncached continuation leg would re-probe every
    file (1800+ ranged GETs on the largest node). The cache keys on run_id, so a
    fresh run re-probes and picks up newly published columns; it is a per-run
    discovery cache, not a watermark.
    """
    state = load_state(node_id)
    if state.get("schema_version") == STATE_VERSION and state.get("run_id") == run_id:
        return state["columns"]

    with ThreadPoolExecutor(max_workers=_CONCURRENCY) as ex:
        per_file = list(ex.map(lambda it: _fetch_header(*it), items))
    columns: list[str] = []
    seen: set[str] = set()
    for cols in per_file:
        for col in cols:
            if col not in seen:
                seen.add(col)
                columns.append(col)
    save_state(node_id, {
        "schema_version": STATE_VERSION,
        "run_id": run_id,
        "columns": columns,
    })
    return columns


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #
def _fragment_name(node_id: str, url: str) -> str:
    """A stable, collision-free fragment id derived from the file's own path.

    Derived from the URL rather than its index in the listing, so a file that
    ANAC inserts mid-run cannot shift every later fragment's identity and
    resurrect already-committed work under a new name.
    """
    tail = unquote(url).split("/dadosabertos/", 1)[-1].split("/sas/", 1)[-1]
    return _slug(tail[: -len(".csv")]) or "part"


def _fetch_fragment(node_id: str, url: str, optional: bool, columns: list[str]) -> None:
    body = _fetch_body(url, optional=optional)
    if body is None:
        return  # optional file genuinely absent — nothing to commit
    frag = _fragment_name(node_id, url)
    with raw_writer(node_id, RAW_EXT, mode="wt", compression="gzip", fragment=frag) as out:
        for rec in _iter_rows(body):
            row = {c: rec.get(c) for c in columns} if columns else rec
            out.write(json.dumps(row, ensure_ascii=False))
            out.write("\n")


def fetch_one(node_id: str) -> None:
    """Fetch every source CSV of one entity, one raw fragment per file.

    Fragments already committed under this RUN_ID are skipped, so a continuation
    leg resumes where the interrupted one stopped. A *new* run re-fetches
    everything: the source exposes no incremental filter, and re-pulling is how
    revisions and late corrections are picked up.
    """
    desc = CATALOG[node_id[len("anac-"):]]
    items = _discover_items(desc)

    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag for frag, meta in list_raw_fragments(node_id, RAW_EXT).items()
        if meta.get("run_id") == run_id
    }
    pending = [it for it in items if _fragment_name(node_id, it[0]) not in done]
    if not pending:
        return

    # Pad to the union of every file's header, not just the pending ones: the
    # asset's committed fragments must stay column-compatible across legs.
    columns = _header_union(node_id, items, run_id) if len(items) > 1 else []

    with ThreadPoolExecutor(max_workers=_CONCURRENCY) as ex:
        futures = [
            ex.submit(_fetch_fragment, node_id, url, optional, columns)
            for url, optional in pending
        ]
        for fut in futures:
            fut.result()  # propagate the first failure — the node fails, others retry next run


DOWNLOAD_SPECS = [
    NodeSpec(id=f"anac-{eid}", fn=fetch_one, kind="download")
    for eid in CATALOG
]
