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
import re

import pyarrow as pa
from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "maldives-bureau-of-statistics"
INDEX_URL = "https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/"

SCHEMA = pa.schema([
    ("row_label", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
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
def fetch_one(node_id: str) -> None:
    import pandas as pd

    asset = node_id
    table_id = node_id[len(SLUG) + 1:]  # strip "maldives-bureau-of-statistics-"

    href = _resolve_hrefs().get(table_id)
    if href is None:
        raise RuntimeError(
            f"{asset}: table {table_id!r} not found in archive index {INDEX_URL}"
        )

    content = _get_bytes(href)
    engine = "openpyxl" if href.rsplit(".", 1)[-1].lower() == "xlsx" else "xlrd"
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
