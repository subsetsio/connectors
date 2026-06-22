"""Maldives Bureau of Statistics — Statistical Archive of Maldives.

One download node per yearbook table (the rank-active entity union). Each table
is a publication-formatted Excel workbook (multi-row/merged headers, footnotes,
bilingual Dhivehi columns). There is no machine-readable schema and every table
has its own layout, so we parse each crosstab into a uniform tidy long form
``(row_label, series, value)`` — robust whether years run down the rows or across
the columns, and naturally dropping footnote rows and label/translation columns.
The matching transform is then a thin SQL pass-through, one published Delta table
per table.

Access (per research, chosen mechanism ``bulk_xlsx_per_table``): the single
static-HTML archive index is the only manifest. Download URLs embed the upload
year/month and drift when a table is revised, so we re-resolve every href fresh
from the index on each run rather than persisting file URLs. Stateless full
re-pull: every table is tiny (tens of KB) and the whole corpus refetches in a
few minutes, so there is no watermark/cursor — revisions are picked up for free.
"""

import io
import math
import random
import re
import time

import httpx
import pyarrow as pa
import tenacity
from constants import ENTITY_IDS, TABLE_URLS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    is_transient,
    save_raw_parquet,
)

SLUG = "maldives-bureau-of-statistics"
BASE = "https://statisticsmaldives.gov.mv"
INDEX_URL = f"{BASE}/yearbook/statisticalarchive/"

# The source sits behind a WAF that intermittently challenges non-browser
# clients from cloud IPs with a 415 (and occasionally 403) on otherwise-valid
# GETs. Present a browser User-Agent and treat those challenge codes as
# retryable on top of the standard transient set (429/5xx/network).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Referer": INDEX_URL,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}
_WAF_CODES = {403, 408, 415, 425, 429}


def _retryable(exc: BaseException) -> bool:
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in _WAF_CODES
    return False


def _wait(retry_state) -> float:
    """Honor a Retry-After header when the WAF/server sends one; otherwise fall
    back to exponential backoff with jitter."""
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if isinstance(exc, httpx.HTTPStatusError):
        ra = exc.response.headers.get("Retry-After")
        if ra:
            try:
                return min(float(ra), 120.0)
            except ValueError:
                pass
    base = tenacity.wait_exponential(min=5, max=120)(retry_state)
    return base + random.uniform(0, 5)


_waf_retry = tenacity.retry(
    retry=tenacity.retry_if_exception(_retryable),
    stop=tenacity.stop_after_attempt(14),
    wait=_wait,
    reraise=True,
)

SCHEMA = pa.schema([
    ("row_label", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
@_waf_retry
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@_waf_retry
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _resolve_hrefs() -> dict:
    """Scrape the archive index and map each table id (e.g. '1.1') to its
    current .xls/.xlsx download URL. The index is the authoritative manifest."""
    page = _get_text(INDEX_URL)
    hrefs = {}
    for m in re.finditer(r'href="([^"]+/(\d+\.\d+)\.xlsx?)"', page):
        hrefs.setdefault(m.group(2), m.group(1))
    return hrefs


# ---------------------------------------------------------------------------
# Generic crosstab parser — Excel grid -> tidy (row_label, series, value)
# ---------------------------------------------------------------------------
def _isnull(x) -> bool:
    return (
        x is None
        or (isinstance(x, float) and math.isnan(x))
        or (isinstance(x, str) and x.strip() == "")
    )


def _is_num(x) -> bool:
    if x is None:
        return False
    if isinstance(x, (int, float)):
        return not (isinstance(x, float) and math.isnan(x))
    s = str(x).strip().replace(",", "")
    if s == "":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def _to_num(x):
    if isinstance(x, (int, float)):
        return None if (isinstance(x, float) and math.isnan(x)) else float(x)
    s = str(x).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _ascii_ok(s: str) -> bool:
    """True if the string carries any latin letter or digit — used to drop the
    Thaana-script (Dhivehi) header/label cells, keeping the English ones."""
    return any(("a" <= c.lower() <= "z") or c.isdigit() for c in s)


def _cell_str(v) -> str:
    """Render a cell as a clean label token. Legacy .xls reads integer year
    headers as floats (1985.0); show those as plain integers."""
    if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)):
        f = float(v)
        return str(int(f)) if f.is_integer() else str(v)
    return str(v).strip()


def parse_grid(rows: list) -> list:
    """Melt a publication crosstab (list-of-rows grid) into tidy records.

    Strategy: trim leading title/blank rows; drop empty columns; classify each
    column as a numeric *value* column vs a *label* column by majority type;
    treat the rows above the first labelled numeric row as a (possibly
    multi-row, merged) header band and forward-fill it to compose each value
    column's ``series`` name; then emit one record per (data row, value cell).
    """
    def nn(r):
        return sum(0 if _isnull(c) else 1 for c in r)

    start = 0
    while start < len(rows) and nn(rows[start]) <= 1:
        start += 1
    block = rows[start:]
    if not block:
        return []

    ncol = max(len(r) for r in block)
    block = [list(r) + [None] * (ncol - len(r)) for r in block]
    keep = [j for j in range(ncol) if any(not _isnull(r[j]) for r in block)]
    block = [[r[j] for j in keep] for r in block]
    ncol = len(keep)
    if ncol < 2:
        return []

    def frac_num(j):
        vals = [r[j] for r in block if not _isnull(r[j])]
        if not vals:
            return 0.0
        return sum(1 for v in vals if _is_num(v)) / len(vals)

    vcols = [j for j in range(ncol) if frac_num(j) >= 0.5]
    if not vcols:
        return []
    if min(vcols) == 0:
        # leftmost column is itself numeric (e.g. a Year stub) -> it's the label
        label_cols = [0]
        value_cols = [j for j in vcols if j >= 1]
    else:
        label_cols = list(range(min(vcols)))
        value_cols = vcols
    if not value_cols or not label_cols:
        return []

    def has_text_value(r):
        return any((not _isnull(r[j])) and (not _is_num(r[j])) for j in value_cols)

    def has_label(r):
        return any(not _isnull(r[j]) for j in label_cols)

    # first row is always header; the header band ends at the first labelled,
    # text-free row (a real data row).
    h = 1
    while h < len(block):
        r = block[h]
        if has_label(r) and not has_text_value(r):
            break
        h += 1
    header_rows = block[:h]
    data_rows = block[h:]
    if not data_rows:
        return []

    ff = []
    for hr in header_rows:
        out, last = [], None
        for j in range(ncol):
            v = hr[j]
            if _isnull(v):
                out.append(last)
            else:
                last = _cell_str(v)
                out.append(last)
        ff.append(out)

    series_name = {}
    for j in value_cols:
        parts = [
            ff[i][j]
            for i in range(len(ff))
            if ff[i][j] not in (None, "") and _ascii_ok(ff[i][j])
        ]
        series_name[j] = " | ".join(dict.fromkeys(parts)) if parts else f"col_{j}"

    recs = []
    for r in data_rows:
        parts = [
            _cell_str(r[j])
            for j in label_cols
            if not _isnull(r[j]) and _ascii_ok(str(r[j]))
        ]
        lbl = " | ".join(parts)
        if not lbl:
            continue
        for j in value_cols:
            v = _to_num(r[j])
            if v is None:
                continue
            recs.append({"row_label": lbl, "series": series_name[j], "value": v})
    return recs


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
def _download_table(table_id: str) -> bytes:
    """Resolve and download one table's Excel workbook. Prefer the captured URL
    manifest (avoids re-scraping the index on every node, which overloads the
    source WAF); on a 404 the stored path has drifted, so fall back to a fresh
    index scrape — preserving the research directive to resolve drifted URLs."""
    rel = TABLE_URLS.get(table_id)
    if rel:
        try:
            return _get_bytes(BASE + rel)
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 404:
                raise  # 415/5xx/etc are handled by retry, not a stale URL
    href = _resolve_hrefs().get(table_id)
    if href is None:
        raise RuntimeError(
            f"table {table_id!r} not found in archive index {INDEX_URL}"
        )
    return _get_bytes(href)


def fetch_one(node_id: str) -> None:
    import pandas as pd

    configure_http(headers=_BROWSER_HEADERS)
    # De-synchronize the ~122-node burst so the source WAF sees a spread of
    # requests rather than a spike (which it answers with 415 challenges).
    time.sleep(random.uniform(0, 20))

    asset = node_id
    table_id = node_id[len(SLUG) + 1:]  # strip "maldives-bureau-of-statistics-"

    content = _download_table(table_id)
    engine = "openpyxl" if content[:2] == b"PK" else "xlrd"
    df = pd.read_excel(io.BytesIO(content), header=None, engine=engine)
    recs = parse_grid(df.values.tolist())

    table = pa.Table.from_pylist(recs, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                row_label,
                series,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
