"""Guangdong Bureau of Statistics — Statistical Yearbook tables.

The bureau exposes no machine-readable API. Its only clean structured surface is
the online Statistical Yearbook portal, which serves one Excel (.xls) file per
table, grouped into 24 chapters. Each table is a distinct statistical cross-tab
with its own column list, so each one is published as its own Delta table.

Mechanism (chosen by research): `yearbook_excel`. Per-table .xls at
`directory/{chapter}/excel/{part}.xls` under the current edition portal. Tables
split for the web carry continued ("续表") parts (`-0`/`-1`/...); the collect
catalog recorded the full part list per table in `ENTITY_PARTS`.

Fetch shape: **stateless full re-pull**. Files are small (~20-45 KB each) and the
whole corpus re-fetches cheaply; there is no incremental query parameter on the
source, so every refresh pulls the full set and overwrites. The server is plain
HTTP on a non-standard port (8080), HTTPS is broken, and it is slow/flaky — hence
generous `transient_retry`.

Raw representation: each heterogeneous cross-tab is melted into a single stable
long-format schema (one row per data cell), so all 415 tables share one parquet
schema and each transform is a thin typed pass-through. A table's layout is
title rows, then a header row (col0 = row-dimension label, col1 = its English
label, col2+ = year/category column headers), then bilingual data rows. The melt
keeps the row labels (cn/en), the column header, and the numeric/string value.
"""

import pyarrow as pa
import xlrd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_PARTS

SLUG = "guangdong-bureau-of-statistics"
# Current published edition portal. The collect catalog was enumerated from this
# edition; older editions remain available at the same path with a different year.
EDITION = "2025"
BASE = f"http://tjnj.gdstats.gov.cn:8080/tjnj/{EDITION}/directory"  # noqa: E501 - source is HTTP-only (HTTPS cert is broken; port 8080)

# Map download node id -> (table_id, [part ids]). Pure data derived from the
# imported catalog constant; no I/O at import time.
_BY_NODE = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": (eid, parts)
    for eid, parts in ENTITY_PARTS.items()
}

SCHEMA = pa.schema([
    ("table_id", pa.string()),
    ("part", pa.string()),
    ("row_pos", pa.int32()),
    ("col_pos", pa.int32()),
    ("row_label_cn", pa.string()),
    ("row_label_en", pa.string()),
    ("column_header", pa.string()),
    ("value_num", pa.float64()),
    ("value_str", pa.string()),
])


@transient_retry(attempts=8, min_wait=2, max_wait=60)
def _fetch_xls(url: str) -> bytes:
    # Source is China-hosted on plain HTTP port 8080 and is slow from foreign/
    # cloud networks — the TCP handshake can take tens of seconds, so the connect
    # timeout is generous (a 10s connect timeout fails every request from CI).
    resp = get(url, timeout=(60.0, 180.0))
    resp.raise_for_status()
    content = resp.content
    if content[:2] != b"\xd0\xcf":  # OLE2 magic; a 200 HTML error page would fail xlrd
        raise ValueError(f"not an OLE2 .xls (got {content[:16]!r}) at {url}")
    return content


def _cell(sheet, r: int, c: int):
    if r < 0 or c < 0 or r >= sheet.nrows or c >= sheet.ncols:
        return ""
    return sheet.cell_value(r, c)


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _norm_header(v) -> str:
    """Header cell to a stable string; year floats (2000.0) -> '2000'."""
    if _is_num(v):
        f = float(v)
        if f == int(f):
            return str(int(f))
        return repr(f)
    return str(v).strip()


def _detect_header_row(sheet) -> int:
    """The header row is the first row with >=2 non-empty cells from col 2 on
    (title/unit rows only populate col 0, or col 0 + a trailing unit note)."""
    for r in range(min(sheet.nrows, 15)):
        nz = sum(1 for c in range(2, sheet.ncols) if str(_cell(sheet, r, c)).strip())
        if nz >= 2:
            return r
    return -1


def _parse_sheet(content: bytes, table_id: str, part: str) -> list[dict]:
    book = xlrd.open_workbook(file_contents=content)
    sheet = book.sheet_by_index(0)
    hr = _detect_header_row(sheet)
    start = (hr + 1) if hr >= 0 else 0
    headers = {c: _norm_header(_cell(sheet, hr, c)) for c in range(sheet.ncols)} if hr >= 0 else {}

    rows: list[dict] = []
    for r in range(start, sheet.nrows):
        rl_cn = str(_cell(sheet, r, 0)).strip()
        rl_en = str(_cell(sheet, r, 1)).strip()
        for c in range(2, sheet.ncols):
            v = _cell(sheet, r, c)
            num = _is_num(v)
            s = str(v).strip()
            if not num and not s:
                continue
            rows.append({
                "table_id": table_id,
                "part": part,
                "row_pos": r,
                "col_pos": c,
                "row_label_cn": rl_cn or None,
                "row_label_en": rl_en or None,
                "column_header": headers.get(c) or None,
                "value_num": float(v) if num else None,
                "value_str": s or None,
            })
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_id, parts = _BY_NODE[node_id]

    all_rows: list[dict] = []
    for part in parts:
        chapter = part[:2]
        url = f"{BASE}/{chapter}/excel/{part}.xls"
        content = _fetch_xls(url)
        all_rows.extend(_parse_sheet(content, table_id, part))

    if not all_rows:
        # Every yearbook table holds data cells; an empty parse means the layout
        # changed or the file was truncated. Fail loudly rather than publish empty.
        raise AssertionError(f"{asset}: parsed 0 data cells from parts {parts}")

    table = pa.Table.from_pylist(all_rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_PARTS
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                table_id,
                part,
                CAST(row_pos AS INTEGER) AS row_pos,
                CAST(col_pos AS INTEGER) AS col_pos,
                row_label_cn,
                row_label_en,
                column_header,
                CAST(value_num AS DOUBLE) AS value_num,
                value_str
            FROM "{s.id}"
            WHERE value_num IS NOT NULL OR value_str IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
