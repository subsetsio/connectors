"""Bank of Latvia (Latvijas Banka) connector.

Source: the INTS Internet Statistical Database at https://statdb.bank.lv — an
ASP.NET WebForms app exposing a tree of statistical areas. Every leaf data table
lives at /LB/Data/<table_id>. There is no JSON/SDMX catalog API and no GET export
URL; the only way to pull a table is the page's own CSV export, a classic WebForms
__doPostBack: GET the table page (which carries hidden __VIEWSTATE /
__VIEWSTATEGENERATOR / __EVENTVALIDATION), then POST the form back with
__EVENTTARGET set to the CSV export LinkButton ('ctl00$ctl00$Main$Main$lnkCsv').
The postback response body IS the CSV file. The GET and POST share subsets_utils's
process-wide httpx client, so the ASP.NET session cookie set on the GET is replayed
on the POST (required for __EVENTVALIDATION to pass).

Quirks (verified against a full cloud run of all 136 tables):
  - The exported CSV is **Windows-1257** encoded (Baltic), not UTF-8 — we decode it
    in the fetch fn and parse it in Python.
  - Each table is a wide multi-level pivot: a metadata row, one or more period-header
    rows (with merged cells rendered as a value followed by empty cells), an "Item"
    row, then data rows whose leftmost cells are (vertically-merged) row labels and
    whose remaining cells are values under each period column. We reconstruct the
    merges (horizontal fill of the period headers, vertical fill of the row labels)
    and melt the pivot into a faithful long table: (table_id, row_label, period,
    value). One value per (row_label, period) cell, exactly as the source asserts.
  - Under load the host intermittently answers 403 Forbidden; we treat 403 as a
    transient throttle and back off (alongside 429/5xx).

Fetch shape: stateless full re-pull (shape 1). Each table is small; re-fetch the
whole table every run and overwrite. No incremental filter exists on this source.
"""
import csv
import io
import random
import re
import time

import httpx
import pyarrow as pa
from tenacity import (
    retry, retry_if_exception, stop_after_attempt, wait_exponential, wait_random,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, post, configure_http, save_raw_parquet

BASE = "https://statdb.bank.lv"
PREFIX = "bank-of-latvia-"
CSV_EVENT_TARGET = "ctl00$ctl00$Main$Main$lnkCsv"

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
# INTS leaf pages render a server-side pivot and can be slow; be generous.
_TIMEOUT = httpx.Timeout(connect=30.0, read=300.0, write=120.0, pool=60.0)

_SCHEMA = pa.schema([
    ("table_id", pa.string()),
    ("row_label", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])

# The 136 rank-accepted INTS table ids (the entity union).
from constants import ENTITY_IDS

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 403 here is the host's load-shedding throttle, not a real auth denial —
        # backing off and retrying clears it.
        return code in (403, 429) or 500 <= code < 600
    return False


# When the host load-sheds it can keep an IP throttled for several minutes, so a
# node must stay patient enough to outlast the whole throttle window. Earlier runs
# capped at 9 attempts (~4.5 min) and a handful of tables stayed 403 the whole
# time; ride it out longer (~18 min worst case) and jitter each wait so retries on
# successive tables don't re-synchronize into the host's burst detector.
_RETRY = dict(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(12),
    wait=wait_exponential(min=15, max=240) + wait_random(0, 15),
    reraise=True,
)


# ---- CSV pivot parsing -----------------------------------------------------

_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def _is_num(s: str) -> bool:
    s = s.strip()
    return bool(s) and bool(_NUM_RE.match(s))


def _ffill_row(cells: list, lo: int, hi: int) -> list:
    """Forward-fill empty cells across [lo, hi) to reconstruct merged headers."""
    out = list(cells)
    last = ""
    for c in range(lo, hi):
        v = out[c].strip() if c < len(out) else ""
        if v:
            last = v
        elif last:
            while len(out) <= c:
                out.append("")
            out[c] = last
    return out


def parse_pivot(text: str, table_id: str) -> list:
    """Melt one INTS pivot CSV (decoded text) into long (row_label, period, value)
    records. Returns a list of dicts."""
    rows = [[c.strip() for c in r] for r in csv.reader(io.StringIO(text))]
    rows = [r for r in rows if any(c for c in r)]

    def numcols(r):
        return {i for i, c in enumerate(r) if _is_num(c)}

    def first_cell(r):
        for c in r:
            if c.strip():
                return c.strip()
        return ""

    # The "Item" row is the column-dimension header; data starts right after it.
    # Anchoring on it avoids mistaking a header row that carries a bare year (e.g.
    # "Item,,Type,2025") for a data row. Its own value-column cells are the
    # deepest period level, so it stays inside the period-header range below.
    item_row = next((i for i, r in enumerate(rows) if first_cell(r).lower() == "item"), None)
    if item_row is not None:
        first_data = item_row + 1
        data_idx = [i for i in range(first_data, len(rows)) if numcols(rows[i])]
    else:
        # Fallback: a numeric cell plus a non-numeric label in the leftmost cells.
        data_idx = [i for i, r in enumerate(rows)
                    if numcols(r) and any(c and not _is_num(c) for c in r[:4])]
        first_data = data_idx[0] if data_idx else None
    if not data_idx:
        return []

    valcols = set()
    for i in data_idx:
        valcols |= numcols(rows[i])
    first_val, last_val = min(valcols), max(valcols)
    label_cols = list(range(first_val))
    header = rows[:first_data]

    # The "Period"/unit row marks the measure; exclude it from period labels.
    period_marker = None
    for hi, hr in enumerate(header):
        if any(c.lower() == "period" for c in hr):
            period_marker = hi
    # Period-header rows: every header row except the metadata row (0) and the
    # unit/Period row.
    period_rows = [hi for hi in range(len(header)) if hi != 0 and hi != period_marker]
    filled = {hi: _ffill_row(header[hi], first_val, last_val + 1) for hi in period_rows}

    def period_label(c):
        parts = []
        for hi in period_rows:
            hr = filled[hi]
            v = hr[c].strip() if c < len(hr) else ""
            if v and (not parts or parts[-1] != v):
                parts.append(v)
        return " | ".join(parts)

    pcache = {c: period_label(c) for c in sorted(valcols)}

    out = []
    last_lab = {c: "" for c in label_cols}
    for i in data_idx:
        r = rows[i]
        labs = []
        for c in label_cols:
            v = r[c].strip() if c < len(r) else ""
            if v:
                last_lab[c] = v
            if last_lab[c]:
                labs.append(last_lab[c])
        label = " | ".join(labs)
        for c in sorted(valcols):
            if c < len(r) and _is_num(r[c]):
                out.append({"table_id": table_id, "row_label": label,
                            "period": pcache.get(c, ""), "value": float(r[c])})
    return out


# ---- HTTP ------------------------------------------------------------------

_INPUT_RE = re.compile(r"<input\b[^>]*>", re.IGNORECASE)
_ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def _hidden_fields(html: str) -> dict:
    fields = {}
    for tag in _INPUT_RE.findall(html):
        attrs = dict(_ATTR_RE.findall(tag))
        if attrs.get("type", "").lower() != "hidden":
            continue
        name = attrs.get("name")
        if name:
            fields[name] = attrs.get("value", "")
    return fields


def _get_page(url: str) -> str:
    resp = get(url, timeout=_TIMEOUT, headers={"Referer": f"{BASE}/lb/?lang=en"})
    resp.raise_for_status()
    return resp.text


def _post_export(url: str, data: dict) -> httpx.Response:
    resp = post(url, data=data, timeout=_TIMEOUT,
                headers={"Referer": url, "Origin": BASE,
                         "Content-Type": "application/x-www-form-urlencoded"})
    resp.raise_for_status()
    return resp


def _looks_like_csv(resp: httpx.Response) -> bool:
    ctype = resp.headers.get("content-type", "").lower()
    disp = resp.headers.get("content-disposition", "").lower()
    if "csv" in ctype or "csv" in disp or "octet-stream" in ctype or "attachment" in disp:
        return True
    head = resp.content[:500].decode("latin-1", "replace").lower()
    return "text/html" not in ctype and "<html" not in head


@retry(**_RETRY)
def _export_csv(asset: str, table_id: str, page_url: str) -> str:
    """GET the table page → harvest fresh hidden fields → POST the CSV-export
    postback, returning the decoded CSV text. Retried as ONE unit: an ASP.NET
    __VIEWSTATE / __EVENTVALIDATION is single-use and session-bound, so a 403 on
    the POST often means the session/viewstate went stale, not just that we were
    rate-limited. Re-POSTing the same captured form would then 403 forever; only a
    fresh GET (new session cookie + new viewstate) can recover. Each retry
    therefore reloads the page before re-exporting."""
    html = _get_page(page_url)
    fields = _hidden_fields(html)
    if "__VIEWSTATE" not in fields:
        snippet = html[:300].replace("\n", " ")
        raise RuntimeError(
            f"{asset}: INTS page for table {table_id} carried no __VIEWSTATE "
            f"(unexpected page shape). First 300 chars: {snippet!r}")
    fields["__EVENTTARGET"] = CSV_EVENT_TARGET
    fields["__EVENTARGUMENT"] = ""

    time.sleep(0.5)  # small courtesy gap between the GET and the export POST
    resp = _post_export(page_url, fields)
    if not _looks_like_csv(resp):
        ctype = resp.headers.get("content-type")
        disp = resp.headers.get("content-disposition")
        snippet = resp.content[:300].decode("latin-1", "replace").replace("\n", " ")
        raise RuntimeError(
            f"{asset}: CSV export postback did not return a CSV "
            f"(status={resp.status_code} content-type={ctype!r} "
            f"content-disposition={disp!r}). First 300 chars: {snippet!r}")
    return resp.content.decode("cp1257")  # INTS exports are Windows-1257


def fetch_one(node_id: str) -> None:
    """Fetch one INTS table via the CSV-export postback, melt the pivot, and save
    a long parquet. node_id is the spec id ('bank-of-latvia-<table_id>') and the
    asset name; the table id is the suffix."""
    configure_http(headers={"User-Agent": _UA})  # browser UA; resets shared client
    asset = node_id
    table_id = node_id[len(PREFIX):]
    page_url = f"{BASE}/LB/Data/{table_id}?lang=en"

    # Pace the crawl: the host load-sheds (403) under bursts, so jitter the start
    # of each table's fetch to spread requests out.
    time.sleep(random.uniform(2.0, 6.0))
    text = _export_csv(asset, table_id, page_url)
    records = parse_pivot(text, table_id)
    if not records:
        snippet = text[:300].replace("\n", " ")
        raise RuntimeError(
            f"{asset}: parsed 0 data rows from the export "
            f"(unexpected layout). First 300 chars: {snippet!r}")
    table = pa.Table.from_pylist(records, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per INTS table, from its long parquet. All tables
# share the (table_id, row_label, period, value) long schema; row_label and period
# carry the table's own dimension breakdown as text (each INTS leaf is a distinct
# pivot, so there is no shared set of typed dimension columns to normalize to).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT table_id, row_label, period, value FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
