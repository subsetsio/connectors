"""Shared IRS SOI helpers.

Every IRS subset is a bulk CSV (or zipped-CSV) file published under
https://www.irs.gov/pub/irs-soi/. There is no catalog/index API, so each
program's file set is *discovered by probing* stable, predictable URLs.

Fetch shape: **stateless full re-pull** every refresh. Filenames embed the tax
year / year-pair, so each release is a distinct file; we re-fetch the whole set
and overwrite. No watermark/cursor — the corpus is bounded and the maintain step
gates whether a node runs at all. A 404 for a candidate period is a permanent
"that file doesn't exist" and is skipped (not retried); transient 5xx/429/timeout
are retried with backoff.

This module holds the HTTP client, the CSV/zip parsing helpers, the parquet
batch writer, and the wide-extract type-inference helpers shared by the
financial / source-book programs. It defines NO NodeSpecs.
"""

from __future__ import annotations

import csv
import datetime
import io
import zipfile

import pyarrow as pa

from subsets_utils import (
    get,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://www.irs.gov/pub/irs-soi"
_CHUNK = 50_000  # rows per parquet row-group write (bounds memory on big files)


# --------------------------------------------------------------------------- #
# HTTP + parsing helpers
# --------------------------------------------------------------------------- #


@transient_retry()
def _fetch(url: str) -> bytes | None:
    """GET a bulk file. Returns its bytes, or None if the file does not exist
    (404 — a permanent "this period isn't published", not retried). Transient
    failures (5xx/429/timeouts) raise and are retried by the decorator."""
    resp = get(url, timeout=(10.0, 300.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content


def _num(v):
    """Parse a numeric cell to float, or None for blank/non-numeric."""
    if v is None:
        return None
    v = v.strip()
    if v in ("", ".", "."):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _int(v):
    f = _num(v)
    return int(f) if f is not None else None


def _str(v):
    if v is None:
        return None
    v = v.strip()
    return v or None


def _csv_dicts(content: bytes):
    """Yield CSV rows as dicts with lowercased, stripped header keys."""
    reader = csv.DictReader(io.StringIO(content.decode("latin-1")))
    for row in reader:
        yield {(k.strip().lower() if k else k): v for k, v in row.items()}


def _extract_member(zip_bytes: bytes, needle: str | None = None) -> bytes:
    """Return the bytes of the (matching) CSV member inside a zip archive."""
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if not csvs:
        raise ValueError(f"zip has no CSV member (members={zf.namelist()[:8]})")
    chosen = csvs[0]
    if needle:
        for n in csvs:
            if needle in n.lower():
                chosen = n
                break
    return zf.read(chosen)


def _write_batch(asset_id: str, schema: pa.Schema, rows) -> int:
    """Stream `rows` (iterable of dicts conforming to `schema`) to one parquet
    batch file, flushing every _CHUNK rows. Returns the row count written."""
    total = 0
    buf: list[dict] = []
    with raw_parquet_writer(asset_id, schema) as w:
        for row in rows:
            buf.append(row)
            if len(buf) >= _CHUNK:
                w.write_table(pa.Table.from_pylist(buf, schema=schema))
                total += len(buf)
                buf = []
        if buf:
            w.write_table(pa.Table.from_pylist(buf, schema=schema))
            total += len(buf)
    return total


def _two_digit_years(start: int) -> list[int]:
    """Candidate 4-digit years from `start` through the current calendar year.
    Existence is decided by probing each URL; non-published years 404 and are
    dropped — so this is a discovery window, not a hardcoded data range."""
    now = datetime.date.today().year
    return list(range(start, now + 1))


# --------------------------------------------------------------------------- #
# Wide zipped-CSV extract helpers (shared by eo-financial + corp-source-book)
# --------------------------------------------------------------------------- #


def _header_cols(content: bytes) -> list[str]:
    reader = csv.reader(io.StringIO(content.decode("latin-1")))
    header = next(reader)
    return [h.strip().lower() for h in header]


def _looks_num(v: str) -> bool:
    try:
        float(v)
        return True
    except ValueError:
        return False


def _classify_wide(content: bytes, cols: list[str]) -> list[tuple[str, bool]]:
    """Infer each wide-extract column's type from its values and drop the
    genuinely empty ones. Returns ordered (col, is_numeric) pairs.

    The SOI financial extracts mix numeric financial measures with categorical
    letter-code indicators (e.g. `efile`='E', `schdbind`='Y'/'N'). A blanket
    numeric cast would silently null every code column; here a column is numeric
    only if ALL its non-blank values parse as numbers, otherwise it's kept as a
    string. `ein` is always a string (preserve leading zeros). Columns with no
    non-blank value at all are dropped (they'd publish as all-null)."""
    # per-column state: "empty" -> "numeric" -> "string" (monotonic downgrade)
    state = {c: "empty" for c in cols}
    for r in _csv_dicts(content):
        for c in cols:
            if state[c] == "string":
                continue
            v = r.get(c)
            if v is None:
                continue
            v = v.strip()
            if v in ("", "."):
                continue
            if _looks_num(v):
                if state[c] == "empty":
                    state[c] = "numeric"
            else:
                state[c] = "string"
    out: list[tuple[str, bool]] = []
    for c in cols:
        s = state[c]
        if s == "empty":
            continue  # all-null column — drop rather than publish dead weight
        out.append((c, s == "numeric" and c != "ein"))
    return out


def _wide_schema(typed: list[tuple[str, bool]]) -> pa.Schema:
    return pa.schema(
        [("file_year", pa.int32())]
        + [(c, pa.float64() if is_num else pa.string()) for c, is_num in typed]
    )


def _wide_rows(content: bytes, typed: list[tuple[str, bool]], file_year: int):
    for r in _csv_dicts(content):
        row = {"file_year": file_year}
        for c, is_num in typed:
            row[c] = _num(r.get(c)) if is_num else _str(r.get(c))
        yield row
