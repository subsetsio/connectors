"""Office of Rail and Road (ORR) data-portal connector.

The ORR data portal (https://dataportal.orr.gov.uk) exposes no API: each
numbered statistical table publishes as a single OpenDocument Spreadsheet
(.ods) -- occasionally also .csv -- linked from a /statistics/.../table-NNNN/
page or directly from a /media/... path. These workbooks follow the GSS
spreadsheet standard: a cover sheet, a notes sheet, then one or more data
sheets. A data sheet may stack several sub-tables ("blocks"), each introduced
by a title row ("Table 5200b: ...") and its own header row.

We download one workbook per table and flatten every data sheet into a uniform
tidy long format -- one record per (sheet, block, row_label, column, value) --
which is robust to the wide, multi-block, per-table-bespoke layouts. Each table
is published as its own Delta table (heterogeneous catalog: one schema per
table is the natural unit). The long schema is identical across tables, so the
SQL transforms are pass-throughs.
"""

import io
import re
import math

import pandas as pd
from odf import teletype
from odf.opendocument import load as _odf_load
from odf.table import Table, TableRow, TableCell
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS, ENTITY_SRC

SLUG = "office-of-rail-and-road"
BASE = "https://dataportal.orr.gov.uk"

# GSS shorthand markers / placeholders that are not numbers.
_NON_NUMERIC = {"..", "...", "-", "n/a", "na", ""}
# A row whose single populated cell looks like a sub-table title ("Table 5200b:",
# "7210a2:") starts a new block; the row after it is that block's header.
_TITLE_RE = re.compile(r"^(table\s+)?\d{3,4}[a-z]?\d*\s*[:.]", re.I)
# Spreadsheet link on a table page (the ?cb=<guid> suffix is only a cache-buster).
_LINK_RE = re.compile(r'href="(/media/[^"?]+?\.(?:ods|csv|xlsx))(?:\?[^"]*)?"', re.I)


def _is_blank(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    return isinstance(v, str) and not v.strip()


def _to_num(v):
    """Best-effort numeric parse; None for GSS markers / text / blanks."""
    if _is_blank(v):
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("%", "")
    if not s or s.startswith("[") or s.lower() in _NON_NUMERIC:
        return None
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


@transient_retry()
def _get_text(url: str) -> str:
    return get(url, timeout=60).text


@transient_retry()
def _get_bytes(url: str) -> bytes:
    return get(url, timeout=120).content


_REPEAT_CAP = 1000   # ODS pads trailing empty space with huge repeat counts


def _cell_value(cell) -> "str | None":
    """Display text of an ODS cell, or its office:value, or None.

    Returning the text (not a typed value) keeps numeric parsing in _to_num and
    sidesteps pandas' odf reader, which raises on error-typed cells."""
    text = teletype.extractText(cell).strip()
    if text:
        return text
    v = cell.getAttribute("value")        # office:value (numeric cells)
    return v if v not in (None, "") else None


def _read_ods(content: bytes) -> dict:
    """Read an ODS workbook into {sheet_name: list-of-rows} grids using odfpy
    directly. Robust to error cells and to repeated-cell/row padding."""
    doc = _odf_load(io.BytesIO(content))
    sheets = {}
    for table in doc.spreadsheet.getElementsByType(Table):
        name = table.getAttribute("name") or ""
        grid = []
        for tr in table.getElementsByType(TableRow):
            rr = int(tr.getAttribute("numberrowsrepeated") or 1)
            cells = []
            for tc in tr.getElementsByType(TableCell):
                cr = int(tc.getAttribute("numbercolumnsrepeated") or 1)
                val = _cell_value(tc)
                if cr > _REPEAT_CAP and val is None:
                    cr = 1            # trailing column padding
                cells.extend([val] * cr)
            while cells and cells[-1] is None:
                cells.pop()
            if rr > _REPEAT_CAP and not cells:
                rr = 1                # trailing row padding
            for _ in range(rr):
                grid.append(list(cells))
        while grid and not any(c is not None for c in grid[-1]):
            grid.pop()
        sheets[name] = grid
    return sheets


def _parse_sheet(sheet_name: str, rows: list) -> list:
    """Flatten one sheet (list of cell-rows) into long records, block- and
    header-aware."""
    records = []
    header = None      # list of (col_index, header_text)
    row_dim = None
    block = sheet_name
    after_title = False
    for raw in rows:
        cells = list(raw)
        nn = [(j, c) for j, c in enumerate(cells) if not _is_blank(c)]
        if not nn:
            continue
        # A title row introduces a sub-table: its first cell is a table code
        # ("Table 5200b:", "7210a2:"). This covers BOTH vertically stacked blocks
        # (single-cell title) and horizontally stacked blocks (several titles
        # across one row, e.g. the regional tables) -- in either case the next
        # populated row is the real header.
        first_j, first_v = nn[0]
        if first_j == 0 and _TITLE_RE.match(str(first_v).strip()):
            block = str(first_v).strip()
            after_title = True
            continue
        if len(nn) == 1:
            continue
        # >=2 populated cells: a header row or a data row. Switch header only at
        # sheet start or immediately after a sub-table title -- never re-detect
        # mid-block (sparse [x]/[z] rows would fool any text-vs-number guess).
        if header is None or after_title:
            after_title = False
            last = max(j for j, _ in nn)
            header = [(j, str(cells[j]).strip()) for j in range(last + 1) if not _is_blank(cells[j])]
            row_dim = header[0][1] if header else None
            continue
        after_title = False
        if not header:
            continue
        first_col = header[0][0]
        label = "" if _is_blank(cells[0]) else str(cells[0]).strip()
        for j, name in header:
            if j == first_col:
                continue
            val = cells[j] if j < len(cells) else None
            if _is_blank(val):
                continue
            records.append({
                "sheet": sheet_name,
                "block": block,
                "row_dim": row_dim,
                "row_label": label,
                "column": name,
                "col_index": j,
                "value": str(val).strip(),
                "value_num": _to_num(val),
            })
    return records


# Boilerplate sheets (anchored at the sheet-name start so data sheets like
# "4143_Complaint_contact_methods" are NOT excluded).
_SKIP_SHEET_RE = re.compile(
    r"^\W*(cover|notes?|contents?|metadata|definitions?|about|contact|guidance|index)\b",
    re.I,
)


def _parse_workbook(content: bytes, ext: str) -> list:
    if ext == "csv":
        df = pd.read_csv(io.BytesIO(content), header=None, dtype=str)
        return _parse_sheet("data", df.values.tolist())
    if ext == "ods":
        sheets = _read_ods(content)
    else:  # xlsx / xls
        frames = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, dtype=str)
        sheets = {name: df.values.tolist() for name, df in frames.items()}
    records = []
    for name, rows in sheets.items():
        if _SKIP_SHEET_RE.match(name or ""):
            continue
        records.extend(_parse_sheet(name, rows))
    return records


def _long_from_frame(sheet: str, block: str, df: "pd.DataFrame") -> list:
    """Melt a header-resolved DataFrame (row 0 = data) into long records."""
    cols = [str(c) for c in df.columns]
    if not cols:
        return []
    row_dim = cols[0]
    records = []
    for _, row in df.iterrows():
        label = "" if _is_blank(row.iloc[0]) else str(row.iloc[0]).strip()
        for j in range(1, len(cols)):
            val = row.iloc[j]
            if _is_blank(val):
                continue
            records.append({
                "sheet": sheet,
                "block": block,
                "row_dim": row_dim,
                "row_label": label,
                "column": cols[j],
                "col_index": j,
                "value": str(val).strip(),
                "value_num": _to_num(val),
            })
    return records


def _parse_report_table(html: str, entity: str) -> list:
    """Some tables (the 4-weekly 'periodic' ones) ship no spreadsheet: the data
    is embedded as an HTML <table id="reportTable"> that a Tabulator widget
    renders client-side. Parse that table directly into long records."""
    m = re.search(r'<table[^>]*id="reportTable"[^>]*>.*?</table>', html, re.I | re.S)
    if not m:
        return []
    title = re.search(r'reportFilename\s*=\s*"([^"]+)"', html)
    block = title.group(1).strip() if title else entity
    frames = pd.read_html(io.StringIO(m.group(0)))
    records = []
    for df in frames:
        records.extend(_long_from_frame("reportTable", block, df))
    return records


def _find_link(html: str) -> str | None:
    links = _LINK_RE.findall(html)
    if not links:
        return None
    # prefer .ods (uniform parser), then .csv, then .xlsx
    return (next((l for l in links if l.lower().endswith(".ods")), None)
            or next((l for l in links if l.lower().endswith(".csv")), None)
            or links[0])


def fetch_one(node_id: str) -> None:
    entity = node_id[len(SLUG) + 1:]            # strip "office-of-rail-and-road-"
    kind, path = ENTITY_SRC[entity]
    if kind == "file":
        url = BASE + path
        records = _parse_workbook(_get_bytes(url), path.rsplit(".", 1)[-1].lower())
        source = url
    else:
        html = _get_text(BASE + path)
        link = _find_link(html)
        if link:
            ext = link.rsplit(".", 1)[-1].lower()
            records = _parse_workbook(_get_bytes(BASE + link), ext)
            source = link
        else:
            # no downloadable spreadsheet -> embedded HTML report table
            records = _parse_report_table(html, entity)
            source = path
    if not records:
        raise ValueError(f"{entity}: parsed 0 records from {source}")
    save_raw_ndjson(records, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

_TRANSFORM_SQL = (
    'SELECT sheet, block, row_dim, row_label, '
    '"column" AS column_name, col_index, value, value_num '
    'FROM "{dep}"'
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-{eid}-transform",
        fn=None,
        kind="transform",
        deps=(f"{SLUG}-{eid}",),
        sql=_TRANSFORM_SQL.format(dep=f"{SLUG}-{eid}"),
    )
    for eid in ENTITY_IDS
]
