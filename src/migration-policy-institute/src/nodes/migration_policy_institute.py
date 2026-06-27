"""Migration Policy Institute (MPI) Data Hub connector.

Mechanism: bulk_download. Each rank-active entity is one Data Hub tool backed by
a single Excel workbook under /sites/default/files/datahub/ (see research). The
site is behind a Cloudflare managed challenge that 403s non-browser User-Agents
and all HTML pages, but the static Excel files serve normally with a desktop
browser UA — so we fetch each file directly and a browser UA is mandatory.

These workbooks are human-formatted (leading blank/title rows, merged multi-row
headers with years across the top, footnote rows at the bottom) and every file
has a different shape. Rather than 21 brittle bespoke parsers, the download fn
runs ONE generic extractor that turns each workbook into a uniform **long /
tidy cell table**: one row per non-empty data cell, carrying the sheet, a stable
row id, the row's leading label, the column's (forward-filled, multi-row)
header as `variable`, and the value as both text and (when numeric) a number.
Year-header rows are folded into the column header so a matrix like
"region x year" becomes ("Germany", "2024 | Estimate", 1234). This absorbs the
source's annual updates for free — a new year is a new `variable` value, not a
schema change.

Stateless full re-pull every run (shape 1): each file is a small full snapshot
(tens of KB to ~2MB), so there is no watermark/cursor — we re-fetch and overwrite.
No incremental filter exists on a static file anyway.
"""

import io

import pyarrow as pa
from python_calamine import CalamineWorkbook

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS, FILENAMES

SLUG = "migration-policy-institute"
PREFIX = f"{SLUG}-"
BASE_URL = "https://www.migrationpolicy.org/sites/default/files/datahub/"

# Cloudflare on this host 403s the default UA; a desktop browser UA is required
# for the static file paths to serve. ASCII-only (httpx rejects non-ASCII headers).
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("row_id", pa.int64()),
    ("col_index", pa.int64()),
    ("row_label", pa.string()),
    ("variable", pa.string()),
    ("value_text", pa.string()),
    ("value_num", pa.float64()),
])


def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _is_year(x):
    return _is_num(x) and float(x).is_integer() and 1800 <= x <= 2100


def _fmt(v):
    """Render a cell as text, dropping the trailing '.0' on integer-valued floats."""
    if _is_num(v) and float(v).is_integer():
        return str(int(v))
    return str(v)


def _extract_long(sheet_name, rows):
    """Turn one worksheet (list of cell-rows) into long tidy cell records."""
    grid = [[(c if c != "" else None) for c in r] for r in rows]
    if not grid:
        return []
    ncols = max((len(r) for r in grid), default=0)
    if ncols == 0:
        return []
    grid = [r + [None] * (ncols - len(r)) for r in grid]
    nrows = len(grid)

    def numcount(r):
        return sum(1 for c in r if _is_num(c))

    def nonnull(r):
        return sum(1 for c in r if c is not None)

    def is_yearrow(r):
        nums = [c for c in r if _is_num(c)]
        return len(nums) >= 2 and all(_is_year(c) for c in nums)

    # First real data row: >=2 numeric cells and not an all-years header row.
    r0 = next(
        (i for i, r in enumerate(grid) if numcount(r) >= 2 and not is_yearrow(r)),
        None,
    )
    if r0 is None:  # degenerate single-value-column table
        r0 = next((i for i, r in enumerate(grid) if numcount(r) >= 1), None)
    if r0 is None:
        return []

    # Header band: every row above the data (year rows, metric sub-headers, the
    # label-title row). Forward-fill each horizontally to spread merged cells.
    parts = [[] for _ in range(ncols)]
    for i in range(r0):
        r = grid[i]
        if nonnull(r) < 2:
            continue
        last = None
        for c in range(ncols):
            if r[c] is not None:
                last = r[c]
            if last is not None and str(last).strip():
                parts[c].append(_fmt(last).strip())
    header = [" | ".join(dict.fromkeys(p)) if p else None for p in parts]

    out = []
    for r in range(r0, nrows):
        row = grid[r]
        if nonnull(row) == 0:
            break  # contiguous data block ends; footnotes follow
        rl = _fmt(row[0]).strip() if row[0] is not None else None
        for c in range(ncols):
            v = row[c]
            if v is None:
                continue
            out.append({
                "sheet": sheet_name,
                "row_id": r,
                "col_index": c,
                "row_label": rl,
                "variable": header[c] or f"col{c}",
                "value_text": _fmt(v),
                "value_num": float(v) if _is_num(v) else None,
            })
    return out


def _extract_file(content):
    wb = CalamineWorkbook.from_filelike(io.BytesIO(content))
    rows = []
    for name in wb.sheet_names:
        rows.extend(_extract_long(name, wb.get_sheet_by_name(name).to_python()))
    return rows


@transient_retry()
def _download(url):
    resp = get(url, headers={"User-Agent": BROWSER_UA}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(PREFIX):]
    filename = FILENAMES[entity_id]
    content = _download(BASE_URL + filename)
    rows = _extract_file(content)
    if not rows:
        raise AssertionError(f"{node_id}: extracted 0 cells from {filename}")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                sheet,
                CAST(row_id AS INTEGER)    AS row_id,
                CAST(col_index AS INTEGER) AS col_index,
                row_label,
                variable,
                value_text,
                value_num
            FROM "{s.id}"
            WHERE value_text IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
