"""Kobe Customs regional trade statistics connector.

Source: Kobe Customs (神戸税関), one of Japan Customs' 9 regional customs offices.
Its finalized annual regional trade statistics are published as one ZIP per
(statistic-type x year) on the boueki "kakutei" (確定資料) listing page, each ZIP
holding a single human-formatted Japanese .xls (BIFF8, Shift-JIS / code page 932).

There are 9 statistic-types (kobe, hyogo, chugoku, shikoku, shina_ex, shina_im,
kuni_ex, kuni_im, kenbetsu). Each type is one entity -> one download spec -> one
published subset; YEAR is a column, not a separate dataset.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is ~36 small
.xls files; re-fetch everything every run and overwrite. The year set is
*discovered* from the listing page (never hardcoded); for each (type, year) we
prefer the finalized 確々報 (kakukaku) file and fall back to the provisional
確報 (kaku) file when no finalized one exists yet.

Parsing: these are formatted statistical reports (title rows, merged header
cells, multi-sheet, footnotes), not flat tables. We normalize every sheet into a
tidy long form: one row per numeric cell, carrying its reconstructed row label
(merged label columns, forward-filled down), its reconstructed column-header path
(merged header rows above the data, forward-filled right), the sheet name, and
the cell's (row, col) coordinate. This is lossless and uniform across all 9
heterogeneous layouts; downstream SQL/curation can pivot on row_label/col_header.
"""

import io
import numbers
import re
import zipfile

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "kobe-customs"
LISTING_URL = "https://www.customs.go.jp/kobe/boueki/02kakutei.html"
FILE_BASE = "https://www.customs.go.jp/kobe/boueki/"

# The 9 statistic-types Kobe Customs publishes (also the entity union).
ENTITY_IDS = [
    "chugoku", "hyogo", "kenbetsu", "kobe", "kuni_ex",
    "kuni_im", "shikoku", "shina_ex", "shina_im",
]

# href -> (year, classification, statistic-type)
_HREF_RE = re.compile(r'(kakutei/r\d{2}/(\d{4})_(kakukaku|kaku)_([a-z_]+)\.zip)')

SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("classification", pa.string()),   # "finalized" (確々報) | "provisional" (確報)
    ("sheet", pa.string()),
    ("row_label", pa.string()),
    ("col_header", pa.string()),
    ("row_idx", pa.int32()),
    ("col_idx", pa.int32()),
    ("value", pa.float64()),
])


# ---- HTTP with retry ---------------------------------------------------------


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


# ---- listing discovery -------------------------------------------------------

def _discover_files(stat_type: str) -> dict:
    """Return {year: (classification, absolute_url)} for one statistic-type,
    preferring the finalized (kakukaku) file when both classes exist for a year."""
    html = _get_bytes(LISTING_URL).decode("shift_jis", "replace")
    chosen: dict[int, tuple[str, str]] = {}
    for href, year_s, cls, typ in _HREF_RE.findall(html):
        if typ != stat_type:
            continue
        year = int(year_s)
        finalized = cls == "kakukaku"
        existing = chosen.get(year)
        # finalized wins over provisional; otherwise first seen.
        if existing is None or (finalized and existing[0] != "finalized"):
            chosen[year] = (
                "finalized" if finalized else "provisional",
                FILE_BASE + href,
            )
    return chosen


# ---- xls -> tidy long rows ---------------------------------------------------

def _is_number(v) -> bool:
    return (
        isinstance(v, numbers.Number)
        and not isinstance(v, bool)
        and pd.notna(v)
    )


def _melt_sheet(df: pd.DataFrame, sheet: str) -> list[dict]:
    """Melt one formatted sheet into one record per numeric cell, reconstructing
    the merged row label (left columns, ffilled down) and column-header path
    (rows above the data, ffilled right)."""
    nrows, ncols = df.shape
    numcells = [
        (r, c)
        for r in range(nrows)
        for c in range(ncols)
        if _is_number(df.iat[r, c])
    ]
    if not numcells:
        return []

    min_r = min(r for r, _ in numcells)
    min_c = min(c for _, c in numcells)
    label_cols = list(range(0, min_c)) if min_c > 0 else [0]
    header_rows = list(range(0, min_r))  # may be empty

    # Forward-fill label columns downward (handles vertically merged labels).
    lab: dict[tuple[int, int], str] = {}
    for c in label_cols:
        last = ""
        for r in range(nrows):
            v = df.iat[r, c]
            if isinstance(v, str) and v.strip():
                last = " ".join(v.split())
            lab[(r, c)] = last

    # Forward-fill header rows rightward (handles horizontally merged headers).
    hdr: dict[tuple[int, int], str] = {}
    for r in header_rows:
        last = ""
        for c in range(ncols):
            v = df.iat[r, c]
            if isinstance(v, str) and v.strip():
                last = " ".join(v.split())
            hdr[(r, c)] = last

    out = []
    for r, c in numcells:
        row_label = " ".join(
            x for x in (lab.get((r, cc), "") for cc in label_cols) if x
        )
        col_header = " | ".join(
            x for x in (hdr.get((rr, c), "") for rr in header_rows) if x
        )
        out.append({
            "sheet": sheet,
            "row_label": row_label or None,
            "col_header": col_header or None,
            "row_idx": r,
            "col_idx": c,
            "value": float(df.iat[r, c]),
        })
    return out


def _parse_zip(content: bytes) -> list[dict]:
    """Extract the inner .xls (Shift-JIS entry name) and melt all its sheets."""
    z = zipfile.ZipFile(io.BytesIO(content))
    inner = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx"))]
    if not inner:
        raise AssertionError(f"no .xls inside zip; entries={z.namelist()}")
    name = inner[0]
    data = z.read(name)
    engine = "openpyxl" if name.lower().endswith(".xlsx") else "xlrd"
    sheets = pd.read_excel(io.BytesIO(data), sheet_name=None, header=None, engine=engine)
    rows: list[dict] = []
    for sheet_name, df in sheets.items():
        rows.extend(_melt_sheet(df, str(sheet_name)))
    return rows


# ---- download fn (shared across all 9 specs) ---------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    stat_type = node_id[len(SLUG) + 1:].replace("-", "_")  # e.g. shina-ex -> shina_ex

    files = _discover_files(stat_type)
    if not files:
        raise AssertionError(
            f"{node_id}: no ZIPs found for statistic-type {stat_type!r} on listing"
        )

    rows: list[dict] = []
    for year in sorted(files):
        classification, url = files[year]
        content = _get_bytes(url)
        for rec in _parse_zip(content):
            rec["year"] = year
            rec["classification"] = classification
            rows.append(rec)

    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 numeric cells from {len(files)} file(s)")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
