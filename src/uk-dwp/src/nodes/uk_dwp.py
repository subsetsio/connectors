"""DWP (UK Department for Work and Pensions) connector.

Mechanism: data.gov.uk CKAN v3 (https://ckan.publishing.service.gov.uk/api/3),
publisher `department-for-work-and-pensions`. Each rank-accepted entity is one
CKAN *package* whose CSV resources are period partitions (monthly/quarterly
transparency returns) of one logical dataset. We fetch every CSV resource of a
package and union it into a single raw parquet.

These transparency CSVs drift heavily across years (renamed/added columns,
title rows, embedded newlines, mixed delimiters), so we cannot impose one
typed schema. Instead each fetch:
  1. downloads every CSV resource to a temp dir (single download per file),
  2. parses headers, normalising names to snake_case, and computes the union
     of column names across the package's data-bearing files,
  3. streams every data row into one parquet whose schema is provenance
     columns + the (string-typed) union — absent columns are null per file.

The SQL transform is then a thin `SELECT *`: it publishes the package's data
faithfully, with provenance (resource name carries the period). Values stay
strings — casting is left to consumers because column semantics vary by year.

Stateless full re-pull: the whole catalog is small and re-fetchable in minutes,
revisions are picked up for free, so there is no watermark/cursor state. CKAN
exposes no row-level delta filter anyway.
"""
from __future__ import annotations

import csv
import io
import os
import re
import shutil
import tempfile

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_parquet_writer

# --- the entity union (rank-accepted CKAN package ids) -----------------------
ENTITY_IDS = [
    "dwp-prompt-payment-data",
    "dwp_government_procurement_card_payments_over_500",
    "exceptions-to-government-moratoria-department-work-and-pensions",
    "financial-transactions-data-dwp",
    "ministerial-data-dwp",
    "organogram-of-staff-roles-salaries30092019",
    "senior-officials-expenses-travel-and-hospitality-in-dwp",
    "special-advisers-dwp",
    "workforce_management_information_dwp",
]

CKAN_BASE = "https://ckan.publishing.service.gov.uk/api/3"

# A single CSV resource producing more columns than this is treated as
# malformed (wrong delimiter / not really tabular) and skipped, rather than
# exploding the parquet schema. A whole package exceeding the union cap raises.
MAX_FILE_COLS = 300
MAX_UNION_COLS = 800

PROV_FIELDS = [
    "resource_name",
    "resource_id",
    "resource_last_modified",
    "source_url",
    "row_index",
]


def _node_id(entity_id: str) -> str:
    return f"uk-dwp-{entity_id.lower().replace('_', '-')}"


# node id -> the CKAN package id to query (lossy lower/hyphen transform is not
# reversible, so we keep the original ids and map back).
CKAN_ID_BY_NODE = {_node_id(e): e for e in ENTITY_IDS}


# --- HTTP with honest retry --------------------------------------------------
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
    # TLS certificate problems (some legacy gov hosts present a mismatched
    # cert) never recover on retry — treat as permanent so the per-resource
    # handler skips them immediately instead of burning the backoff budget.
    if isinstance(exc, httpx.ConnectError) and "CERTIFICATE_VERIFY" in str(exc).upper():
        return False
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


# --- CSV parsing -------------------------------------------------------------
_NORM_RE = re.compile(r"[^a-z0-9]+")


def _norm(name: str, i: int) -> str:
    s = _NORM_RE.sub("_", (name or "").strip().lower()).strip("_")
    return s or f"col_{i}"


def _decode(raw: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def _sniff_delimiter(lines: list[str]) -> str:
    sample = "\n".join(lines[:20])
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


# Marker phrases that only ever appear in the SAP/BusinessObjects banner
# preamble of DWP spending exports (never in a real header or data row). Rows
# carrying any of these are dropped before header detection — in some years the
# banner is split across cells and would otherwise be mistaken for the header.
_BANNER_MARKERS = (
    "workbook name",
    "worksheet name",
    "workbook was run",
    "from payment date",
    "to payment date",
    "invoice amount greater than",
)


def _is_banner(row) -> bool:
    for cell in row:
        low = (cell or "").lower()
        if any(m in low for m in _BANNER_MARKERS):
            return True
    return False


def _read_rows(text: str, delim: str):
    """Parse `text` into rows. Prefer a proper streaming parse (so newlines
    inside quoted fields — common in DWP's newer workbook exports, e.g.
    'Payroll staff;\\nAO/AA;\\nHeadcount' — stay within one field). Fall back to
    a lenient line-split only if the source is malformed enough that the strict
    parser raises ('new-line character seen in unquoted field')."""
    try:
        return list(csv.reader(io.StringIO(text), delimiter=delim))
    except csv.Error:
        return list(csv.reader(text.splitlines(), delimiter=delim))


def _parse_csv(raw: bytes):
    """Return (column_names, data_rows). data_rows is a list of cell lists.

    Robust to title rows, blank lines, quoted embedded newlines, and
    non-comma delimiters. Returns ([], []) for an empty/headerless file.
    """
    text = _decode(raw)
    sniff_lines = [ln for ln in text.splitlines() if ln.strip()]
    if not sniff_lines:
        return [], []
    delim = _sniff_delimiter(sniff_lines)
    rows = [r for r in _read_rows(text, delim) if any((c or "").strip() for c in r)]
    if not rows:
        return [], []
    # Strip SAP banner preamble (only ever in the top rows) before detecting
    # the header, so a split banner line can't be adopted as the column row.
    head = [r for r in rows[:25] if not _is_banner(r)]
    rows = head + rows[25:]
    if not rows:
        return [], []

    # header = the FIRST row among the first 15 that reaches half the maximum
    # width seen in that window. This skips narrow banner/preamble lines
    # (SAP/BusinessObjects exports prefix "Date and time the workbook was
    # run...", "Parameters: ..." rows of 1-2 cells) while still landing on the
    # header rather than a later data row — picking the single widest row would
    # latch onto a data row that happens to be one cell wider than the header,
    # turning its values into column names and exploding the schema union.
    window = rows[:15]
    widths = [sum(1 for c in r if (c or "").strip()) for r in window]
    maxw = max(widths)
    if maxw >= 2:
        threshold = max(2, maxw // 2)
        hidx = next(i for i, w in enumerate(widths) if w >= threshold)
    else:
        hidx = 0
    header = rows[hidx]
    cols, seen = [], {}
    for i, h in enumerate(header):
        c = _norm(h, i)
        if c in seen:
            seen[c] += 1
            c = f"{c}_{seen[c]}"
        else:
            seen[c] = 0
        cols.append(c)
    data = rows[hidx + 1:]
    return cols, data


def _list_csv_resources(ckan_id: str):
    res = _get_json(f"{CKAN_BASE}/action/package_show", id=ckan_id)["result"]["resources"]
    out = []
    for r in res:
        if (r.get("format") or "").upper() == "CSV" and r.get("url"):
            out.append(
                {
                    "url": r["url"],
                    "name": r.get("name") or "",
                    "id": r.get("id") or "",
                    "last_modified": r.get("last_modified") or r.get("created") or "",
                }
            )
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id
    ckan_id = CKAN_ID_BY_NODE[node_id]
    resources = _list_csv_resources(ckan_id)
    if not resources:
        raise AssertionError(f"{node_id}: package {ckan_id!r} has no CSV resources")

    tmpdir = tempfile.mkdtemp(prefix="uk-dwp-")
    try:
        # Pass A: download every resource once, parse to learn columns/row-count.
        kept = []  # (tmp_path, resource, cols)
        union: set[str] = set()
        skipped = 0
        for r in resources:
            try:
                raw = _get_bytes(r["url"])
            except Exception as exc:  # noqa: BLE001 - per-resource isolation
                # A single bad resource (dead URL, mismatched TLS cert on a
                # legacy host, exhausted transient retries) must not sink the
                # whole package — log the URL + class and skip it.
                skipped += 1
                print(
                    f"[uk-dwp] skip resource {r['name']!r} ({r['url']}) of "
                    f"{ckan_id}: {type(exc).__name__}: {exc}"
                )
                continue
            cols, data = _parse_csv(raw)
            if not data:
                continue  # title-only / empty file contributes nothing
            if len(cols) > MAX_FILE_COLS:
                print(
                    f"[uk-dwp] skip malformed resource {r['name']!r} of {ckan_id}: "
                    f"{len(cols)} columns > {MAX_FILE_COLS}"
                )
                continue
            # Only columns that actually carry a value anywhere in this file
            # join the union — header names with no data behind them would
            # otherwise publish as all-null columns and bloat the schema.
            nonempty = {
                cols[j]
                for row in data
                for j in range(min(len(row), len(cols)))
                if (row[j] or "").strip()
            }
            if not nonempty:
                continue
            path = os.path.join(tmpdir, f"{len(kept)}.bin")
            with open(path, "wb") as fh:
                fh.write(raw)
            kept.append((path, r, cols))
            union |= nonempty

        if not kept:
            raise AssertionError(
                f"{node_id}: package {ckan_id!r} yielded no data rows across "
                f"{len(resources)} CSV resource(s)"
            )
        if len(union) > MAX_UNION_COLS:
            raise AssertionError(
                f"{node_id}: column union {len(union)} > {MAX_UNION_COLS} — "
                "likely a parsing bug (delimiter/encoding), refusing to publish"
            )

        data_cols = sorted(union)
        schema = pa.schema(
            [(f, pa.int64() if f == "row_index" else pa.string()) for f in PROV_FIELDS]
            + [(c, pa.string()) for c in data_cols]
        )

        # Pass B: stream each cached file into the unioned parquet.
        with raw_parquet_writer(asset, schema) as writer:
            for path, r, cols in kept:
                with open(path, "rb") as fh:
                    _cols, data = _parse_csv(fh.read())
                n = len(data)
                if n == 0:
                    continue
                # Only file columns that survived into the published union get
                # written; columns dropped as all-null are silently ignored.
                datacol_set = set(data_cols)
                columns = {
                    "resource_name": [r["name"]] * n,
                    "resource_id": [r["id"]] * n,
                    "resource_last_modified": [r["last_modified"]] * n,
                    "source_url": [r["url"]] * n,
                    "row_index": list(range(n)),
                }
                for c in data_cols:
                    columns[c] = [None] * n
                for i, row in enumerate(data):
                    for j, c in enumerate(cols):
                        if c in datacol_set and j < len(row):
                            val = row[j]
                            columns[c][i] = val if (val is not None and val != "") else None
                table = pa.table(
                    {f.name: pa.array(columns[f.name], type=f.type) for f in schema},
                    schema=schema,
                )
                writer.write_table(table)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(e), fn=fetch_one, kind="download") for e in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
