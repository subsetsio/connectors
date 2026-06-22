"""Banco Central del Ecuador (BCE) — statistical Excel workbooks.

Mechanism (research: ``bulk_xlsx``): BCE publishes its statistics as native
Excel workbooks (``.xlsx`` / a few legacy ``.xls``) at stable, path-based URLs
discovered by crawling the chapter HTML index pages. There is no JSON/SDMX API
and no incremental filter, so each refresh re-fetches the full corpus and
overwrites (stateless full re-pull — the files are small, a few KB to ~12 MB).

The workbooks are human-formatted statistical reports (multi-sheet, title rows,
merged cells, period-across-rows-or-columns layouts), one distinct layout per
file — there is no machine-readable schema. We therefore parse every workbook
with ONE generic melt: for each sheet we detect the leading text label columns
and the header rows, then emit one tidy row per populated data cell, carrying
the cell's row label, column header, and value. This is a faithful, fully
generic long representation that never assumes a per-file schema. The SQL
transform is a thin typed pass over that long table.

TLS note: ``contenido.bce.fin.ec`` serves a valid GlobalSign EV cert, so default
verification works (the cert quirk in research applied only to the unrelated
datosabiertos.gob.ec portal, which is not used here).
"""
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
)
from constants import ENTITY_IDS, FILE_URLS

PREFIX = "banco-central-del-ecuador-"

# Stable long-format contract for the parsed cells of every workbook.
SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("row_index", pa.int32()),
    ("col_index", pa.int32()),
    ("row_label", pa.string()),
    ("col_header", pa.string()),
    ("value", pa.float64()),
    ("value_text", pa.string()),
])

_MAXTEXT = 500
_configured = False


def _ensure_http():
    global _configured
    if not _configured:
        # Browser-ish UA: the wider gob.ec edge occasionally 403s default UAs.
        # ASCII-only header value.
        configure_http(headers={"User-Agent": "Mozilla/5.0 (compatible; subsets-bce/1.0)"})
        _configured = True


@transient_retry()
def _download(url: str) -> bytes:
    # Generous read timeout — the long historical series run to ~12 MB.
    resp = get(url, timeout=(10.0, 240.0))
    resp.raise_for_status()
    return resp.content


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _clean(v) -> str:
    return " ".join(str(v).split())[:_MAXTEXT]


def _iter_sheets(content: bytes, ext: str):
    """Yield (sheet_name, grid) where grid is a list of equal-length cell rows."""
    if ext == "xls":
        import xlrd
        book = xlrd.open_workbook(file_contents=content)
        for sh in book.sheets():
            yield sh.name, [[sh.cell_value(r, c) for c in range(sh.ncols)]
                            for r in range(sh.nrows)]
    else:
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        try:
            for ws in wb.worksheets:
                yield ws.title, [list(r) for r in ws.iter_rows(values_only=True)]
        finally:
            wb.close()


def _parse_workbook(content: bytes, ext: str) -> list:
    """Generic melt of a BCE workbook into tidy long rows (see module docstring)."""
    out = []
    for name, grid in _iter_sheets(content, ext):
        grid = [r for r in grid if r is not None]
        if not grid:
            continue
        ncol = max((len(r) for r in grid), default=0)
        if ncol == 0:
            continue
        grid = [list(r) + [None] * (ncol - len(r)) for r in grid]

        def empty(v):
            return v is None or (isinstance(v, str) and v.strip() == "")

        # First row that carries any numeric data → start of the data region.
        first_data = None
        for ri, r in enumerate(grid):
            if any(_is_num(v) for v in r):
                first_data = ri
                break

        if first_data is None:
            # No numbers anywhere → emit non-empty text cells so the table is
            # never empty (keeps the transform from failing on a label-only file).
            for ri, r in enumerate(grid):
                for ci, v in enumerate(r):
                    if not empty(v):
                        out.append({"sheet": name, "row_index": ri, "col_index": ci,
                                    "row_label": None, "col_header": None,
                                    "value": None, "value_text": _clean(v)})
            continue

        header_rows = grid[:first_data]
        data_rows = grid[first_data:]

        # Leading, contiguous, text-dominant columns are row-label columns.
        label_cols = []
        for ci in range(ncol):
            texts = nums = 0
            for r in data_rows:
                v = r[ci]
                if empty(v):
                    continue
                if _is_num(v):
                    nums += 1
                else:
                    texts += 1
            if ci == len(label_cols) and texts > nums and (texts + nums) > 0:
                label_cols.append(ci)
        label_set = set(label_cols)

        def col_header(ci):
            parts = [_clean(h[ci]) for h in header_rows if not empty(h[ci])]
            return " | ".join(p for p in parts if p) or None

        headers = {ci: col_header(ci) for ci in range(ncol) if ci not in label_set}

        for ri, r in enumerate(data_rows):
            row_label = " | ".join(_clean(r[ci]) for ci in label_cols if not empty(r[ci])) or None
            for ci in range(ncol):
                if ci in label_set:
                    continue
                v = r[ci]
                if empty(v):
                    continue
                num = float(v) if _is_num(v) else None
                out.append({
                    "sheet": name,
                    "row_index": first_data + ri,
                    "col_index": ci,
                    "row_label": row_label,
                    "col_header": headers[ci],
                    "value": num,
                    "value_text": None if num is not None else _clean(v),
                })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    _ensure_http()
    entity_id = node_id[len(PREFIX):]
    url = FILE_URLS[entity_id]
    ext = "xls" if url.lower().endswith(".xls") else "xlsx"

    content = _download(url)
    # Guard: a stale/removed path returns an HTML error page, not a workbook.
    head = content[:8]
    if not (head[:4] == b"PK\x03\x04" or head[:4] == b"\xd0\xcf\x11\xe0"):
        raise AssertionError(
            f"{asset}: expected an Excel workbook at {url}, got non-Excel bytes "
            f"(first bytes {head!r}) — the file may have moved")

    rows = _parse_workbook(content, ext)
    if not rows:
        raise AssertionError(f"{asset}: workbook at {url} parsed to 0 rows")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per workbook: a thin typed pass over the long melt.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                sheet,
                CAST(row_index AS INTEGER) AS row_index,
                CAST(col_index AS INTEGER) AS col_index,
                row_label,
                col_header,
                CAST(value AS DOUBLE)      AS value,
                value_text
            FROM "{s.id}"
            WHERE value IS NOT NULL OR value_text IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
