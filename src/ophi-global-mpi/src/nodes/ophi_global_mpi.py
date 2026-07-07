"""OPHI Global MPI download nodes.

OPHI publishes the annual Global MPI data as eight small XLSX workbooks. Raw
XLSX is not SQL-readable by the transform runtime, so each download normalizes
the workbook into a parquet cell grid: one row per non-empty worksheet cell,
with sheet/row/column coordinates and typed value columns.
"""

from __future__ import annotations

import datetime as dt
import io

import openpyxl
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

SLUG = "ophi-global-mpi"
BASE_URL = "https://ophi.org.uk/sites/default/files/2025-10"
RELEASE_YEAR = 2025

TABLE_FILES = {
    "table-1": "Table%201%20National%20Results%20MPI%202025.xlsx",
    "table-2": "Table%202%20Other%20k%20Values%20MPI%202025.xlsx",
    "table-3": "Table%203%20Age%20Results%20MPI%202025.xlsx",
    "table-4": "Table%204%20Area%20Results%20MPI%202025.xlsx",
    "table-5": "Table%205%20Subnational%20Results%20MPI%202025.xlsx",
    "table-6": "Table_6_Trends_Over_Time_MPI_2025_30_Oct.xlsx",
    "table-7": "Table%207%20Headship%20Results%20MPI%202025.xlsx",
    "table-8": "Table%208%20All%20MPI%20Data%202010%E2%80%932025.xlsx",
}

SCHEMA = pa.schema(
    [
        ("release_year", pa.int16()),
        ("table_number", pa.int8()),
        ("workbook_filename", pa.string()),
        ("sheet_name", pa.string()),
        ("row_index", pa.int32()),
        ("column_index", pa.int32()),
        ("value_text", pa.string()),
        ("value_number", pa.float64()),
        ("value_bool", pa.bool_()),
        ("value_type", pa.string()),
    ]
)


def _entity_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _table_number(entity_id: str) -> int:
    return int(entity_id.rsplit("-", 1)[1])


def _url_for_entity(entity_id: str) -> str:
    return f"{BASE_URL}/{TABLE_FILES[entity_id]}"


def _url_for_asset(asset_id: str) -> str:
    return _url_for_entity(_entity_id(asset_id))


def _cell_value(value) -> tuple[str | None, float | None, bool | None, str]:
    if value is None:
        return None, None, None, "blank"
    if isinstance(value, bool):
        return str(value), None, value, "boolean"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value), float(value), None, "number"
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat(), None, None, "datetime"
    text = str(value).strip()
    if text == "":
        return None, None, None, "blank"
    return text, None, None, "string"


def _workbook_rows(content: bytes, entity_id: str) -> list[dict]:
    filename = TABLE_FILES[entity_id]
    table_number = _table_number(entity_id)
    workbook = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    rows: list[dict] = []

    for worksheet in workbook.worksheets:
        for row_index, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
            for column_index, value in enumerate(row, start=1):
                value_text, value_number, value_bool, value_type = _cell_value(value)
                if value_type == "blank":
                    continue
                rows.append(
                    {
                        "release_year": RELEASE_YEAR,
                        "table_number": table_number,
                        "workbook_filename": filename,
                        "sheet_name": worksheet.title,
                        "row_index": row_index,
                        "column_index": column_index,
                        "value_text": value_text,
                        "value_number": value_number,
                        "value_bool": value_bool,
                        "value_type": value_type,
                    }
                )

    if not rows:
        raise ValueError(f"{entity_id}: parsed 0 non-empty cells from workbook")
    return rows


def fetch_table(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    url = _url_for_entity(entity_id)
    response = get(url, timeout=(10.0, 180.0))
    response.raise_for_status()

    rows = _workbook_rows(response.content, entity_id)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, url, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="ophi-global-mpi-table-1", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-2", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-3", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-4", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-5", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-6", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-7", fn=fetch_table, kind="download"),
    NodeSpec(id="ophi-global-mpi-table-8", fn=fetch_table, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description="Annual Global MPI workbook; freshness checked via OPHI Last-Modified/ETag headers on the versioned XLSX URL.",
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet")
        and source_unchanged(asset_id, _url_for_asset(asset_id)),
    )
    for spec in DOWNLOAD_SPECS
]
