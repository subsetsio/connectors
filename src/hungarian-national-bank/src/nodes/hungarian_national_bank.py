"""Hungarian National Bank statistical workbook downloads.

MNB publishes each accepted statistical entity as a workbook under
``https://statisztika.mnb.hu/timeseries/``. The workbooks are heterogeneous
formatted statistical tables: some are modern ``.xlsx`` files, while a sizeable
legacy slice remains BIFF ``.xls``. The download layer therefore normalizes each
workbook to a uniform SQL-readable cell table instead of guessing a tidy header
for 558 distinct layouts. The model/transform stage can then interpret each
workbook from the preserved sheet/row/column grid.
"""

from __future__ import annotations

import io
import math
from datetime import date, datetime, time

import pandas as pd
import pyarrow as pa

from constants import ENTITY_IDS, ENTITY_METADATA
from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "hungarian-national-bank"
BASE_URL = "https://statisztika.mnb.hu"

CELL_SCHEMA = pa.schema(
    [
        ("entity_id", pa.string()),
        ("source_file_url", pa.string()),
        ("source_file_format", pa.string()),
        ("source_title", pa.string()),
        ("topic", pa.string()),
        ("group_name", pa.string()),
        ("last_update_date", pa.string()),
        ("next_update_date", pa.string()),
        ("sheet_name", pa.string()),
        ("row_number", pa.int32()),
        ("column_number", pa.int32()),
        ("cell_value", pa.string()),
        ("cell_type", pa.string()),
    ]
)


def _entity_from_node_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    entity_id = node_id.removeprefix(prefix)
    if entity_id not in ENTITY_METADATA:
        raise KeyError(f"no metadata for entity {entity_id!r}")
    return entity_id


def _cell_type(value) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, datetime):
        return "datetime"
    if isinstance(value, date):
        return "date"
    if isinstance(value, time):
        return "time"
    return "string"


def _cell_value(value) -> str | None:
    typ = _cell_type(value)
    if typ == "null":
        return None
    if typ in {"datetime", "date", "time"}:
        return value.isoformat()
    return str(value).strip()


def _workbook_engine(fmt: str | None, content: bytes) -> str | None:
    if content.startswith(b"PK"):
        return "openpyxl"
    if content.startswith(b"\xd0\xcf"):
        return "xlrd"
    if fmt == "xls":
        return "xlrd"
    if fmt == "xlsx":
        return "openpyxl"
    return None


def _read_sheets(content: bytes, fmt: str | None) -> dict[str, pd.DataFrame]:
    try:
        return pd.read_excel(
            io.BytesIO(content),
            sheet_name=None,
            header=None,
            dtype=object,
            engine=_workbook_engine(fmt, content),
        )
    except Exception as exc:
        raise RuntimeError(f"failed to parse {fmt or 'unknown'} workbook") from exc


def _rows_from_workbook(entity_id: str, content: bytes) -> list[dict]:
    meta = ENTITY_METADATA[entity_id]
    sheets = _read_sheets(content, meta.get("file_format"))
    rows: list[dict] = []
    for sheet_name, df in sheets.items():
        for row_idx, row in enumerate(df.itertuples(index=False, name=None), start=1):
            for col_idx, value in enumerate(row, start=1):
                cell_value = _cell_value(value)
                if cell_value in (None, ""):
                    continue
                rows.append(
                    {
                        "entity_id": entity_id,
                        "source_file_url": meta.get("file_url"),
                        "source_file_format": meta.get("file_format"),
                        "source_title": meta.get("name"),
                        "topic": meta.get("topic"),
                        "group_name": meta.get("group"),
                        "last_update_date": meta.get("last_update_date"),
                        "next_update_date": meta.get("next_update_date"),
                        "sheet_name": str(sheet_name),
                        "row_number": row_idx,
                        "column_number": col_idx,
                        "cell_value": cell_value,
                        "cell_type": _cell_type(value),
                    }
                )
    if not rows:
        raise RuntimeError(f"workbook for {entity_id} contained no non-empty cells")
    return rows


def _unavailable_rows(entity_id: str, status_code: int, url: str) -> list[dict]:
    meta = ENTITY_METADATA[entity_id]
    return [
        {
            "entity_id": entity_id,
            "source_file_url": meta.get("file_url"),
            "source_file_format": meta.get("file_format"),
            "source_title": meta.get("name"),
            "topic": meta.get("topic"),
            "group_name": meta.get("group"),
            "last_update_date": meta.get("last_update_date"),
            "next_update_date": meta.get("next_update_date"),
            "sheet_name": "__unavailable__",
            "row_number": 1,
            "column_number": 1,
            "cell_value": f"Workbook unavailable from MNB portal: HTTP {status_code} at {url}",
            "cell_type": "unavailable",
        }
    ]


def fetch_workbook_cells(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    meta = ENTITY_METADATA[entity_id]
    file_url = meta.get("file_url")
    if not file_url:
        raise RuntimeError(f"missing file_url for {entity_id}")
    url = file_url if str(file_url).startswith("http") else f"{BASE_URL}{file_url}"
    resp = get(url, timeout=(10.0, 300.0))
    if resp.status_code == 404:
        save_raw_parquet(
            pa.Table.from_pylist(_unavailable_rows(entity_id, resp.status_code, url), schema=CELL_SCHEMA),
            node_id,
        )
        return
    resp.raise_for_status()
    rows = _rows_from_workbook(entity_id, resp.content)
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CELL_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=ENTITY_METADATA[entity_id]["asset_id"], fn=fetch_workbook_cells)
    for entity_id in ENTITY_IDS
]
