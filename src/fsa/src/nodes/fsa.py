"""FSA (Japan) connector — CKAN catalog over the national e-Gov data portal.

FSA (金融庁) publishes open data through data.e-gov.go.jp, a standard CKAN 3
instance, as organization `org_0800`. Each entity in the union is one CKAN
**package**; its publishable content is the spreadsheet (XLS/XLSX/CSV)
resources hosted on www.fsa.go.jp (PDF/HTML resources are administrative docs,
skipped). Resource urls can change across re-publications, so we re-resolve
them per refresh via `package_show` rather than hardcoding.

The spreadsheets are heterogeneous Japanese government statistical tables —
title rows, merged cells, mid-sheet headers, varied per-dataset layouts — with
no machine-readable per-dataset schema. There is no reliable way to author 64
bespoke wide parsers, so each package is normalized into a single uniform
**long / cell-level** table: one row per non-empty spreadsheet cell, carrying
its resource, sheet, (row, col) coordinate, the cell text, and a parsed numeric
value when the cell is numeric. This is robust to any layout and never invents
structure that isn't there.

Fetch shape: **stateless full re-pull** (shape 1). The whole corpus is a few MB
across 64 small spreadsheet packages; there is no usable changed-only delta
(CKAN `metadata_modified` exists but no reliable incremental window), so every
refresh re-resolves and re-downloads each package's resources and overwrites.
No watermark, no cursor.
"""
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
import pandas as pd

from constants import ENTITY_IDS

CKAN = "https://data.e-gov.go.jp/data/api/3/action"
SPREADSHEET_FORMATS = {"XLSX", "XLS", "CSV"}

# Uniform long/cell-level schema, declared once and reused for every package.
# Every emitted row is one non-empty spreadsheet cell.
SCHEMA = pa.schema([
    ("resource_id", pa.string()),
    ("resource_name", pa.string()),
    ("sheet", pa.string()),
    ("row_idx", pa.int32()),
    ("col_idx", pa.int32()),
    ("value", pa.string()),
    ("num_value", pa.float64()),
])


@transient_retry()  # 6 attempts, exp backoff on transient net errors + 429 + 5xx
def _ckan_package_show(package_id: str) -> dict:
    resp = get(f"{CKAN}/package_show", params={"id": package_id},
               timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise AssertionError(f"package_show success=false for {package_id}")
    return body["result"]


@transient_retry()
def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _excel_engine(content: bytes) -> str | None:
    """Pick the pandas engine from the file's magic bytes — the declared CKAN
    `format` is unreliable (XLS-labelled resources are frequently real .xlsx)."""
    if content[:4] == b"PK\x03\x04":
        return "openpyxl"          # zip-based modern .xlsx
    if content[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        return "xlrd"              # OLE2 legacy .xls
    return None


def _num_value(v) -> float | None:
    """Numeric cells (ints/floats, excluding bools) become a parsed double;
    text/date cells leave num_value null."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        try:
            f = float(v)
        except (ValueError, OverflowError):
            return None
        # pandas yields NaN for blank numeric cells; those are dropped upstream
        return f if f == f else None
    return None


def _cells_from_sheet(rows_out: list, resource_id: str, resource_name: str,
                      sheet: str, df: pd.DataFrame) -> None:
    """Melt one sheet (read header-less) to one record per non-empty cell."""
    for r, (_, series) in enumerate(df.iterrows()):
        for c, v in enumerate(series.tolist()):
            if v is None:
                continue
            if isinstance(v, float) and v != v:   # NaN
                continue
            text = str(v).strip()
            if text == "":
                continue
            rows_out.append({
                "resource_id": resource_id,
                "resource_name": resource_name,
                "sheet": sheet,
                "row_idx": r,
                "col_idx": c,
                "value": text,
                "num_value": _num_value(v),
            })


def _parse_spreadsheet(rows_out: list, resource_id: str, resource_name: str,
                       fmt: str, content: bytes) -> None:
    engine = _excel_engine(content)
    if engine is not None:
        xl = pd.ExcelFile(io.BytesIO(content), engine=engine)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, header=None, dtype=object)
            _cells_from_sheet(rows_out, resource_id, resource_name, str(sheet), df)
        return
    if fmt == "CSV":
        df = None
        for enc in ("utf-8-sig", "cp932", "shift_jis"):
            try:
                df = pd.read_csv(io.BytesIO(content), header=None, dtype=object,
                                 encoding=enc)
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        if df is not None:
            _cells_from_sheet(rows_out, resource_id, resource_name, "csv", df)
        return
    # Unknown magic and not declared CSV: skip — not a SQL-readable spreadsheet.


def fetch_one(node_id: str) -> None:
    asset = node_id                               # the spec id IS the asset name
    package_id = node_id[len("fsa-"):]            # recover the CKAN package uuid
    result = _ckan_package_show(package_id)

    rows: list[dict] = []
    for res in result.get("resources", []) or []:
        fmt = (res.get("format") or "").upper().strip()
        if fmt not in SPREADSHEET_FORMATS:
            continue
        url = res.get("url")
        if not url:
            continue
        resource_id = res.get("id") or url
        resource_name = res.get("name") or ""
        try:
            content = _download_bytes(url)
        except Exception as exc:                  # noqa: BLE001 - logged + per-resource
            # A dead/moved resource url is permanent for this resource; skip it
            # and keep the rest of the package's resources rather than failing
            # the whole node. transient_retry already exhausted retries above.
            print(f"fsa: resource fetch failed, skipping "
                  f"url={url} resource={resource_id} "
                  f"err={type(exc).__name__}: {exc}")
            continue
        _parse_spreadsheet(rows, resource_id, resource_name, fmt, content)

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fsa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
