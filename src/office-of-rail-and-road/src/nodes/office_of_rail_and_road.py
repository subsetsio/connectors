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


def _parse_sheet(sheet_name: str, df: "pd.DataFrame") -> list:
    """Flatten one sheet into long records, block- and header-aware."""
    records = []
    header = None      # list of (col_index, header_text)
    row_dim = None
    block = sheet_name
    after_title = False
    for raw in df.values.tolist():
        cells = list(raw)
        nn = [(j, c) for j, c in enumerate(cells) if not _is_blank(c)]
        if not nn:
            continue
        if len(nn) == 1:
            txt = str(nn[0][1]).strip()
            if _TITLE_RE.match(txt):
                block = txt
                after_title = True
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


def _parse_workbook(content: bytes, ext: str) -> list:
    if ext == "csv":
        df = pd.read_csv(io.BytesIO(content), header=None, dtype=str)
        return _parse_sheet("data", df)
    engine = "odf" if ext == "ods" else "openpyxl"
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, engine=engine)
    records = []
    for name, df in sheets.items():
        if re.search(r"cover|note|content|metadata|contact|definition", name, re.I):
            continue
        records.extend(_parse_sheet(name, df))
    return records


def _resolve_file(entity: str) -> tuple:
    """Return (absolute_url, ext) for the entity's spreadsheet."""
    kind, path = ENTITY_SRC[entity]
    if kind == "file":
        return BASE + path, path.rsplit(".", 1)[-1].lower()
    html = _get_text(BASE + path)
    links = _LINK_RE.findall(html)
    if not links:
        raise ValueError(f"{entity}: no spreadsheet link found on {path}")
    # prefer .ods (uniform parser), then .csv, then .xlsx
    pref = (next((l for l in links if l.lower().endswith(".ods")), None)
            or next((l for l in links if l.lower().endswith(".csv")), None)
            or links[0])
    return BASE + pref, pref.rsplit(".", 1)[-1].lower()


def fetch_one(node_id: str) -> None:
    entity = node_id[len(SLUG) + 1:]            # strip "office-of-rail-and-road-"
    url, ext = _resolve_file(entity)
    content = _get_bytes(url)
    records = _parse_workbook(content, ext)
    if not records:
        raise ValueError(f"{entity}: parsed 0 records from {url}")
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
