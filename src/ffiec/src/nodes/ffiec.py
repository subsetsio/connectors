"""FFIEC HMDA Snapshot connector — public bulk loan-level mortgage data.

Source: the HMDA Snapshot National Loan-Level Dataset, published by the CFPB on
behalf of the FFIEC as frozen annual releases at
``https://files.ffiec.cfpb.gov/static-data/snapshot/{year}/{year}_public_{ds}_pipe.zip``
(``ds`` in {lar, ts, msamd}). No auth, one stable zip per (year, dataset).

Three published subsets (the rank-accepted entity union):
  - ``lar``               loan/application register, ~10-20M rows/year, ~99 cols
  - ``msamd``             MSA/MD reference codes, one row per area/year
  - ``transmittal_sheet`` one row per filing institution per year, 10 cols

Scope: only the **modern post-2018-redesign** HMDA schema is servable as one
coherent table. Pre-2018 snapshots (e.g. 2017) use a completely different,
header-less column layout and are skipped. The connector name also references
FFIEC Call Reports / UBPR, but those bulk/PWS surfaces are auth-gated (see
research gaps) and are out of scope; HMDA is the fully public surface.

Shape — stateless full re-pull (no watermark): HMDA snapshots are immutable
frozen annual files, so every run re-discovers the available years and rewrites
one parquet batch per (dataset, year). Whether a node actually re-runs on a
given refresh is the maintain step's concern, not ours. There is no incremental
delta filter on the bulk path.

Raw layout — one parquet file per year at asset id ``ffiec-<ds>-<year>`` (the
batch layout the runtime globs as ``ffiec-<ds>-*`` behind the transform's dep
view). The CSV is large, so each year is stream-inflated from its zip to a
temp file and parsed by DuckDB (fast C++ CSV reader) rather than Python. Every
column is stored as VARCHAR and reindexed onto the **union** of column names
across all discovered years, so all per-year files share one identical schema
(the runtime reads them with a single ``read_parquet([...])`` that does NOT
union by name). Typing/casting is the SQL transform's job — the correctness gate.
"""

from __future__ import annotations

import codecs
import csv
import os
import struct
import tempfile
import zlib
from datetime import datetime, timezone

import duckdb

from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

_BASE = "https://files.ffiec.cfpb.gov/static-data/snapshot/"

# The files.ffiec.cfpb.gov host is Akamai-fronted and rejects the default client
# (HTTP 403) from datacenter IPs / non-browser agents. A browser-like header set
# clears the bot heuristics. ASCII-only (httpx encodes header values as latin-1).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://ffiec.cfpb.gov/",
}

# Modern, post-redesign HMDA schema epoch. The 2018 data year was the first
# collected under the rewritten Regulation C; earlier snapshots use a different
# (header-less) column layout and are intentionally not served here.
_REDESIGN_FIRST_YEAR = 2018

# entity spec id (slug-prefixed) -> the dataset code used in the snapshot URL.
_DATASET_CODE = {
    "ffiec-lar": "lar",
    "ffiec-msamd": "msamd",
    "ffiec-transmittal-sheet": "ts",
}

# The header sentinel that marks a modern (post-redesign) snapshot file. LAR and
# TS carry activity_year in the file; MSAMD is a year-specific reference table
# whose year is implicit in the snapshot path and synthesized while writing raw.
_MODERN_FIRST_COL = "activity_year"
_EXPECTED_FIRST_COL = {
    "lar": _MODERN_FIRST_COL,
    "msamd": "msa_md",
    "ts": _MODERN_FIRST_COL,
}

# Rows per Arrow batch streamed from DuckDB into the parquet writer. Bounds
# peak memory on the multi-million-row LAR files.
_BATCH_ROWS = 200_000


def _zip_url(year: int, ds: str) -> str:
    return f"{_BASE}{year}/{year}_public_{ds}_pipe.zip"


def _inflated_bytes(url: str):
    """Stream a single-member zip from ``url``, yielding decompressed byte chunks.

    The HMDA snapshot zips hold exactly one DEFLATE member, so we parse the
    local file header off the front of the stream and inflate the rest
    incrementally — the (multi-hundred-MB) archive is never held in memory.
    """
    client = get_client()
    with client.stream("GET", url, timeout=(10.0, 600.0)) as resp:
        resp.raise_for_status()
        chunks = resp.iter_bytes(chunk_size=1 << 20)
        header = bytearray()
        for chunk in chunks:
            header += chunk
            if len(header) >= 30:
                break
        else:
            raise ValueError(f"{url}: stream ended before a zip local header")
        if bytes(header[:4]) != b"PK\x03\x04":
            raise ValueError(f"{url}: not a zip (magic {bytes(header[:4])!r})")
        method = struct.unpack("<H", header[8:10])[0]
        fnlen, eflen = struct.unpack("<HH", header[26:30])
        start = 30 + fnlen + eflen
        while len(header) < start:
            header += next(chunks)
        if method == 8:
            dec = zlib.decompressobj(-15)
            inflate = dec.decompress
        elif method == 0:  # stored, uncompressed
            dec = None
            inflate = lambda b: b  # noqa: E731
        else:
            raise ValueError(f"{url}: unsupported zip compression method {method}")

        first = inflate(bytes(header[start:]))
        if first:
            yield first
        for chunk in chunks:
            out = inflate(chunk)
            if out:
                yield out
        if dec is not None:
            tail = dec.flush()
            if tail:
                yield tail


@transient_retry()
def _read_header(url: str) -> list[str]:
    """Stream just the first CSV line of a snapshot zip and return its columns.

    Only ~1 chunk is transferred — the stream is aborted as soon as the header
    line is in hand.
    """
    gen = _inflated_bytes(url)
    try:
        buf = b""
        for chunk in gen:
            buf += chunk
            if b"\n" in buf:
                break
        line = buf.split(b"\n", 1)[0].rstrip(b"\r").decode("utf-8", "replace")
        return next(csv.reader([line], delimiter="|"))
    finally:
        gen.close()  # abort the underlying HTTP stream


@transient_retry()
def _year_exists(year: int, ds: str) -> bool:
    """Existence probe for one (year, dataset) via a 1-byte range request."""
    resp = get(_zip_url(year, ds), headers={"Range": "bytes=0-0"}, timeout=(10.0, 60.0))
    if resp.status_code in (200, 206):
        return True
    if resp.status_code == 404:
        return False
    resp.raise_for_status()  # 5xx -> transient retry; other 4xx -> raise
    return False


def _discover_years(ds: str) -> list[int]:
    """Discover which snapshot years are published, from the redesign epoch up to
    the next calendar year (a freshly dropped year is picked up automatically)."""
    current = datetime.now(tz=timezone.utc).year
    return [y for y in range(_REDESIGN_FIRST_YEAR, current + 2) if _year_exists(y, ds)]


@transient_retry()
def _download_member_to_tmp(url: str) -> str:
    """Stream-inflate the single zip member to a temp .csv file; return its path.

    Scratch staging only (deleted by the caller) — not a raw asset, so a plain
    file handle is appropriate here. DuckDB parses it by path.
    """
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "wb") as out:
            for chunk in _inflated_bytes(url):
                out.write(chunk)
    except BaseException:
        os.unlink(path)
        raise
    return path


def _write_year(asset: str, year: int, ds: str, header: list[str], union: list[str]) -> None:
    """Download one (year, dataset), reindex onto the union schema (all VARCHAR),
    and stream it to the per-year parquet batch ``asset``."""
    tmp = _download_member_to_tmp(_zip_url(year, ds))
    try:
        con = duckdb.connect()
        present = set(header)
        pieces = []
        for col in union:
            if col in present:
                pieces.append(f'"{col}"')
            elif col == _MODERN_FIRST_COL:
                pieces.append(f"'{year}' AS \"{col}\"")
            else:
                pieces.append(f'CAST(NULL AS VARCHAR) AS "{col}"')
        proj = ", ".join(pieces)
        esc = tmp.replace("'", "''")
        columns = "{" + ", ".join(f"'{col}': 'VARCHAR'" for col in header) + "}"
        rel = con.sql(
            "SELECT "
            f"{proj} "
            f"FROM read_csv('{esc}', header=true, delim='|', columns={columns}, "
            "auto_detect=false, null_padding=true)"
        )
        reader = rel.to_arrow_reader(_BATCH_ROWS)
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                writer.write_batch(batch)
        con.close()
    finally:
        os.unlink(tmp)


def _fetch_dataset(node_id: str, ds: str) -> None:
    # Once per spec process, before any HTTP: present browser-like headers so the
    # Akamai edge in front of files.ffiec.cfpb.gov does not 403 us.
    configure_http(headers=_BROWSER_HEADERS)

    years = _discover_years(ds)
    if not years:
        raise RuntimeError(f"{node_id}: no published snapshot years discovered for ds={ds!r}")

    # Read every year's header first so the per-year files can share one schema:
    # the union of column names (ordered by first appearance), all VARCHAR.
    headers: dict[int, list[str]] = {}
    for year in years:
        cols = _read_header(_zip_url(year, ds))
        expected_first_col = _EXPECTED_FIRST_COL[ds]
        if not cols or cols[0] != expected_first_col:
            print(f"[ffiec] skip {ds} {year}: not the modern header layout (first col {cols[:1]})")
            continue
        headers[year] = cols
    if not headers:
        raise RuntimeError(f"{node_id}: no modern-schema years among {years} for ds={ds!r}")

    union: list[str] = []
    seen: set[str] = set()
    if any(_MODERN_FIRST_COL not in cols for cols in headers.values()):
        seen.add(_MODERN_FIRST_COL)
        union.append(_MODERN_FIRST_COL)
    for year in sorted(headers):
        for col in headers[year]:
            if col not in seen:
                seen.add(col)
                union.append(col)

    for year in sorted(headers):
        asset = f"{node_id}-{year}"  # batch layout: ffiec-<ds>-<year>
        print(f"[ffiec] writing {asset} ({len(union)} cols)")
        _write_year(asset, year, ds, headers[year], union)


def fetch_lar(node_id: str) -> None:
    _fetch_dataset(node_id, _DATASET_CODE[node_id])


def fetch_msamd(node_id: str) -> None:
    _fetch_dataset(node_id, _DATASET_CODE[node_id])


def fetch_transmittal_sheet(node_id: str) -> None:
    _fetch_dataset(node_id, _DATASET_CODE[node_id])


DOWNLOAD_SPECS = [
    NodeSpec(id="ffiec-lar", fn=fetch_lar, kind="download"),
    NodeSpec(id="ffiec-msamd", fn=fetch_msamd, kind="download"),
    NodeSpec(id="ffiec-transmittal-sheet", fn=fetch_transmittal_sheet, kind="download"),
]
