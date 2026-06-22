"""BCRD (Banco Central de la República Dominicana) — single node module.

Mechanism: ``bulk_excel`` (the only public, comprehensive distribution). BCRD
publishes its official statistics as Excel workbooks (mostly legacy OLE ``.xls``,
some ``.xlsx``) on ``cdn.bancentral.gov.do``. Each statistical topic is one
download spec; topics that are year/month partitioned are several files of one
schema fetched together. The whole corpus is small (hundreds of workbooks, tens
of KB to a few MB each) and revised in place, so every spec is a **stateless
full re-pull**: fetch every file for the topic each run and overwrite. There is
no incremental filter (files mutate in place) and no rate limit (plain CDN).

Parsing: the workbooks have no machine-readable schema and no uniform layout —
Spanish title/units banners, multi-row merged headers, and several sheets per
file, differing topic to topic. Rather than 286 brittle bespoke parsers, each
workbook is read faithfully into a **long cell grid**: one record per non-empty
cell carrying its sheet, (row, col) coordinate, the forward-filled first-column
row label, the cell's text, and a parsed numeric value when the cell is a
number. This is generic, never silently drops data, and is re-typed by the thin
SQL transform that publishes one Delta table per topic. Downstream curation can
pivot the grid into tidy series; the raw structure is preserved losslessly here.

Raw format: NDJSON — cell records are heterogeneous (text headers vs numeric
data interleaved), so a declared parquet schema would be the wrong contract.
"""
import io
import math

import msoffcrypto
import pandas as pd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENTITY_IDS, FILES_BY_SPEC

CDN_BASE = "https://cdn.bancentral.gov.do/"

# Placeholder tokens BCRD uses for "no data" in otherwise-numeric cells.
_NULL_TOKENS = {"-", "--", "n.d.", "nd", "n/d", "...", "."}


@transient_retry()  # 6 attempts, exp backoff 4..120s; reraises 4xx (non-429) at once
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


_OLE_MAGIC = b"\xd0\xcf\x11\xe0"
# Excel's default key for a workbook "encrypted" with an empty password — BCRD
# ships a few legacy .xls files this way (xlrd reports "Workbook is encrypted").
_DEFAULT_XLS_PASSWORD = "VelvetSweatshop"


def _decrypt_if_needed(content: bytes) -> bytes:
    """Transparently decrypt a default-empty-password-encrypted OLE workbook.

    Zip-based formats (.xlsx/.xlsm) and unencrypted .xls pass through unchanged.
    """
    if not content.startswith(_OLE_MAGIC):
        return content
    try:
        office = msoffcrypto.OfficeFile(io.BytesIO(content))
        if not office.is_encrypted():
            return content
        out = io.BytesIO()
        office.load_key(password=_DEFAULT_XLS_PASSWORD)
        office.decrypt(out)
        return out.getvalue()
    except Exception:  # noqa: BLE001 — fall back to the original bytes for the engine to try
        return content


def _read_sheets(content: bytes, filename: str) -> dict:
    """Read every sheet of a workbook as a header-less DataFrame.

    Legacy ``.xls`` is OLE/BIFF (xlrd); ``.xlsx``/``.xlsm`` are zip-based
    (openpyxl). The declared extension picks the preferred engine, with the
    other as fallback in case a file is mislabelled. Default-password-encrypted
    OLE files are decrypted first.
    """
    content = _decrypt_if_needed(content)
    ext = filename.lower().rsplit(".", 1)[-1]
    engines = ["xlrd", "openpyxl"] if ext == "xls" else ["openpyxl", "xlrd"]
    last_err = None
    for engine in engines:
        try:
            return pd.read_excel(
                io.BytesIO(content), sheet_name=None, header=None, engine=engine
            )
        except Exception as err:  # noqa: BLE001 — try the next engine, then reraise
            last_err = err
    raise RuntimeError(f"could not parse {filename!r}: {type(last_err).__name__}: {last_err}")


def _to_number(value, text: str):
    """Numeric value of a cell, or None. Pandas yields native ints/floats for
    numeric cells; string cells are parsed leniently (thousands separators)."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return None if (isinstance(value, float) and math.isnan(value)) else float(value)
    if text.lower() in _NULL_TOKENS:
        return None
    cleaned = text.replace(",", "").replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def _cells(sheets: dict, filename: str) -> list[dict]:
    """Flatten every sheet into long cell records, forward-filling the first
    column as a row label (handles merged year/header cells)."""
    rows: list[dict] = []
    for sheet_name, df in sheets.items():
        if df is None or df.empty:
            continue
        grid = df.values
        n_rows, n_cols = df.shape
        row_label = None
        for r in range(n_rows):
            # Refresh the forward-filled row label from column 0, if present.
            if n_cols:
                c0 = grid[r][0]
                if c0 is not None and not (isinstance(c0, float) and math.isnan(c0)):
                    c0_text = str(c0).strip()
                    if c0_text:
                        row_label = c0_text
            for c in range(n_cols):
                value = grid[r][c]
                if value is None or (isinstance(value, float) and math.isnan(value)):
                    continue
                text = str(value).strip()
                if not text:
                    continue
                rows.append(
                    {
                        "file": filename,
                        "sheet": str(sheet_name),
                        "row": int(r),
                        "col": int(c),
                        "row_label": row_label,
                        "value": text,
                        "num": _to_number(value, text),
                    }
                )
    return rows


def fetch_one(node_id: str) -> None:
    """Download every workbook for one BCRD topic and write its long cell grid.

    Stateless full re-pull: the spec id is the asset name, and the file list is
    looked up from the catalog constants. A workbook that 404s (a partition
    revised away) is skipped; a transient error propagates and fails the node.
    If no file yields any cell, the node fails rather than publish an empty
    asset.
    """
    asset = node_id
    paths = FILES_BY_SPEC[node_id]
    all_rows: list[dict] = []
    for rel_path in paths:
        url = CDN_BASE + rel_path
        filename = rel_path.rsplit("/", 1)[-1]
        try:
            content = _download(url)
        except Exception as err:  # noqa: BLE001
            status = getattr(getattr(err, "response", None), "status_code", None)
            if status is not None and 400 <= status < 500 and status != 429:
                # Permanent: a partition that no longer exists. Skip it, keep going.
                print(f"{asset}: skipping {url} (HTTP {status})")
                continue
            raise
        try:
            sheets = _read_sheets(content, filename)
        except Exception as err:  # noqa: BLE001
            # A single corrupt/unreadable partition must not kill a multi-year
            # topic; log and skip. If every file fails, the empty-guard below
            # fails the node.
            print(f"{asset}: skipping {filename} (unreadable: {type(err).__name__}: {err})")
            continue
        all_rows.extend(_cells(sheets, filename))

    if not all_rows:
        raise RuntimeError(
            f"{asset}: parsed 0 cells from {len(paths)} workbook(s) — "
            "format change or all partitions missing"
        )
    save_raw_ndjson(all_rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bcrd-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per topic: a thin, typed projection of the cell
# grid. The cast to INTEGER/DOUBLE is the correctness gate — a wrong raw shape
# fails here loudly, and a 0-row result fails the node by design.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'''
            SELECT
                file,
                sheet,
                CAST("row" AS INTEGER) AS row_idx,
                CAST("col" AS INTEGER) AS col_idx,
                row_label,
                value         AS value_text,
                CAST(num AS DOUBLE) AS value_num
            FROM "{spec.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for spec in DOWNLOAD_SPECS
]
