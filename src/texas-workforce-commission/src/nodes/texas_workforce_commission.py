from __future__ import annotations

import io
import re
import zipfile
from urllib.parse import urlencode

import pandas as pd
from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson


SLUG = "texas-workforce-commission"
PREFIX = f"{SLUG}-"


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id.removeprefix(PREFIX)


def _filename_from_response(response, fallback: str) -> str:
    header = response.headers.get("content-disposition", "")
    match = re.search(r'filename="?([^";]+)"?', header)
    return match.group(1).strip() if match else fallback


def _clean_cell(value):
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value.item() if hasattr(value, "item") else value


def _workbook_rows(content: bytes, filename: str) -> list[dict]:
    rows: list[dict] = []
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, dtype=object)
    for sheet_name, frame in sheets.items():
        frame = frame.dropna(how="all")
        for idx, row in frame.iterrows():
            record = {
                "source_file": filename,
                "sheet_name": str(sheet_name),
                "row_number": int(idx) + 1,
            }
            for pos, value in enumerate(row.tolist(), start=1):
                cleaned = _clean_cell(value)
                if cleaned is not None:
                    record[f"c{pos:03d}"] = cleaned
            if len(record) > 3:
                rows.append(record)
    return rows


def _rows_from_lmi_payload(content: bytes, filename: str) -> list[dict]:
    lower = filename.lower()
    if lower.endswith((".xls", ".xlsx")):
        return _workbook_rows(content, filename)
    if lower.endswith(".zip"):
        rows: list[dict] = []
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for member in archive.namelist():
                if member.lower().endswith((".xls", ".xlsx")) and not member.startswith("__MACOSX/"):
                    rows.extend(_workbook_rows(archive.read(member), member))
        return rows
    raise ValueError(f"unsupported Texas LMI payload type for {filename!r}")


def fetch_lmi_report(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    report_id = entity_id.removeprefix("lmi-")
    url = f"https://texaslmi.com/api/PopularDownloads/GetDownloadFileById/{report_id}/"
    response = get(url, timeout=(10.0, 120.0))
    response.raise_for_status()
    filename = _filename_from_response(response, f"{report_id}.xlsx")
    rows = _rows_from_lmi_payload(response.content, filename)
    if not rows:
        raise ValueError(f"{node_id}: no tabular rows parsed from {filename}")
    save_raw_ndjson(rows, node_id)


def fetch_socrata_dataset(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    dataset_id = entity_id.removeprefix("socrata-")
    base = f"https://data.texas.gov/resource/{dataset_id}.json"
    rows: list[dict] = []
    limit = 50000
    offset = 0
    while True:
        params = urlencode({"$limit": limit, "$offset": offset})
        response = get(f"{base}?{params}", timeout=(10.0, 120.0))
        response.raise_for_status()
        page = response.json()
        if not isinstance(page, list):
            raise ValueError(f"{node_id}: expected Socrata list response, got {type(page).__name__}")
        rows.extend(page)
        if len(page) < limit:
            break
        offset += limit
    if not rows:
        raise ValueError(f"{node_id}: Socrata dataset {dataset_id} returned no rows")
    save_raw_ndjson(rows, node_id)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    if entity_id.startswith("lmi-"):
        fetch_lmi_report(node_id)
    elif entity_id.startswith("socrata-"):
        fetch_socrata_dataset(node_id)
    else:
        raise ValueError(f"unsupported entity id {entity_id!r}")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one)
    for entity_id in ENTITY_IDS
]
