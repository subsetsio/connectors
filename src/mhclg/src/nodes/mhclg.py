"""MHCLG connector — gov.uk statistical publications.

Mechanism (research-chosen): `gov_uk` REST. Each rank-accepted entity is a gov.uk
publication (a `statistical_data_set` "live table" or a designated statistics
release). Per entity we resolve its attachments from the Content API
(`https://www.gov.uk/api/content/<base_path>`) and download every tabular
attachment (CSV / XLS / XLSX / ODS).

The attachments are heterogeneous, multi-sheet spreadsheets with irregular
title/merged-header layouts that differ table-to-table and year-to-year, so no
single rectangular schema fits a publication. We therefore publish a faithful
**cell-level long extraction**: one row per non-empty cell, carrying its source
attachment, table title, sheet, and (row, column) coordinate plus a numeric
parse. This is uniform across all publications, always non-empty, and lets a
consumer reconstruct/pivot any underlying table by filtering on
attachment_title / sheet_name and pivoting on row_index / col_index.

Fetch shape: stateless full re-pull (shape 1). The corpus is a few hundred
spreadsheet files, re-pullable in one run; asset URLs are content-hash paths
that change on re-upload, so we re-resolve them from the Content API every run
and never store a watermark.
"""

import io
import re

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import ENTITY_IDS, BASE_PATHS

CONTENT_API = "https://www.gov.uk/api/content/"

# content types we can parse into cells; everything else (PDF/HTML previews,
# zip bundles) is skipped.
_CSV_TYPES = {"text/csv", "text/plain"}
_XLSX_TYPES = {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
_XLS_TYPES = {"application/vnd.ms-excel"}
_ODS_TYPES = {"application/vnd.oasis.opendocument.spreadsheet"}
_TABULAR_TYPES = _CSV_TYPES | _XLSX_TYPES | _XLS_TYPES | _ODS_TYPES

# faithful, uniform schema for every publication.
SCHEMA = pa.schema([
    ("attachment_filename", pa.string()),
    ("attachment_title", pa.string()),
    ("content_type", pa.string()),
    ("sheet_name", pa.string()),
    ("row_index", pa.int64()),
    ("col_index", pa.int64()),
    ("value", pa.string()),
    ("value_numeric", pa.float64()),
])

_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_BATCH_ROWS = 200_000  # cells per parquet row group flush — bounds memory


@transient_retry()
def _get_json(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url):
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _to_number(text):
    """Best-effort numeric parse of a cell string, else None."""
    t = text.strip().replace(",", "")
    if t.endswith("%"):
        t = t[:-1].strip()
    if _NUM_RE.match(t):
        try:
            return float(t)
        except ValueError:
            return None
    return None


def _iter_cells(filename, title, content_type, df, sheet_name):
    """Yield (filename, title, content_type, sheet, row, col, value, num) for
    every non-empty cell of a header-less DataFrame."""
    values = df.values
    nrows = len(values)
    for r in range(nrows):
        row = values[r]
        for c in range(len(row)):
            v = row[c]
            if v is None:
                continue
            text = str(v).strip()
            if not text or text.lower() == "nan":
                continue
            yield (filename, title, content_type, sheet_name, r, c, text, _to_number(text))


def _sheets_for(content, raw):
    """Return list of (sheet_name, DataFrame) read header-less, dtype object."""
    import pandas as pd

    if content in _CSV_TYPES:
        # chunked to bound memory on very wide/long CSVs (e.g. 600+ cols).
        return [("csv", chunk) for chunk in pd.read_csv(
            io.BytesIO(raw), header=None, dtype=str, keep_default_na=False,
            na_values=[], chunksize=20_000, low_memory=False, encoding_errors="replace",
        )]
    if content in _XLSX_TYPES:
        engine = "openpyxl"
    elif content in _XLS_TYPES:
        engine = "xlrd"
    elif content in _ODS_TYPES:
        engine = "odf"
    else:
        return []
    book = pd.read_excel(io.BytesIO(raw), sheet_name=None, header=None,
                         dtype=object, engine=engine)
    return list(book.items())


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id = node_id[len("mhclg-"):]
    base_path = BASE_PATHS[entity_id]

    doc = _get_json(CONTENT_API + base_path)
    attachments = (doc.get("details") or {}).get("attachments") or []

    pending = []  # rows buffered before a flush
    wrote_any = False
    with raw_parquet_writer(asset, SCHEMA) as writer:
        def flush():
            nonlocal pending, wrote_any
            if not pending:
                return
            cols = list(zip(*pending))
            table = pa.table({
                "attachment_filename": pa.array(cols[0], pa.string()),
                "attachment_title": pa.array(cols[1], pa.string()),
                "content_type": pa.array(cols[2], pa.string()),
                "sheet_name": pa.array(cols[3], pa.string()),
                "row_index": pa.array(cols[4], pa.int64()),
                "col_index": pa.array(cols[5], pa.int64()),
                "value": pa.array(cols[6], pa.string()),
                "value_numeric": pa.array(cols[7], pa.float64()),
            }, schema=SCHEMA)
            writer.write_table(table)
            pending = []
            wrote_any = True

        for att in attachments:
            ct = att.get("content_type")
            url = att.get("url")
            if ct not in _TABULAR_TYPES or not url:
                continue
            filename = att.get("filename") or url.rsplit("/", 1)[-1]
            title = att.get("title") or filename
            raw = _get_bytes(url)
            try:
                sheets = _sheets_for(ct, raw)
            except Exception as exc:  # noqa: BLE001 - one bad file shouldn't sink the asset
                print(f"  !! parse failed {asset} {filename} ({ct}): {type(exc).__name__}: {exc}")
                continue
            for sheet_name, df in sheets:
                if df is None or df.empty:
                    continue
                for cell in _iter_cells(filename, title, ct, df, str(sheet_name)):
                    pending.append(cell)
                    if len(pending) >= _BATCH_ROWS:
                        flush()
        flush()

        if not wrote_any:
            # No parseable cells at all — write an empty (schema-only) table so the
            # asset exists; the transform's 0-row guard will surface the problem.
            writer.write_table(SCHEMA.empty_table())


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"mhclg-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per publication: a thin pass over the cell extraction,
# dropping any all-empty rows the parser may have let through. Uniform across all
# subsets because the raw schema is uniform.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                attachment_filename,
                attachment_title,
                content_type,
                sheet_name,
                CAST(row_index AS BIGINT) AS row_index,
                CAST(col_index AS BIGINT) AS col_index,
                value,
                CAST(value_numeric AS DOUBLE) AS value_numeric
            FROM "{s.id}"
            WHERE value IS NOT NULL AND length(trim(value)) > 0
        ''',
    )
    for s in DOWNLOAD_SPECS
]
