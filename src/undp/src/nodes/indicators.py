"""UNDP HDR composite-indices metadata codebook.

The workbook documents indicator short codes, display names, and time-series
coverage for the HDR25 composite-indices bulk CSV. It is normalized from XLSX
to parquet so the model stage can profile and join it directly.
"""
import io
import re

import openpyxl
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import fetch_bytes

METADATA_URL = "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_metadata.xlsx"

INDICATORS_SCHEMA = pa.schema([
    ("section", pa.string()),
    ("full_name", pa.string()),
    ("short_name", pa.string()),
    ("time_series", pa.string()),
    ("start_year", pa.int32()),
    ("end_year", pa.int32()),
    ("is_group", pa.bool_()),
])

_YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def _year_bounds(value) -> tuple[int | None, int | None]:
    years = [int(match.group(0)) for match in _YEAR_RE.finditer(str(value or ""))]
    if not years:
        return None, None
    return min(years), max(years)


def fetch_indicators(node_id: str) -> None:
    content = fetch_bytes(METADATA_URL)
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb["codebook"]

    rows = []
    section = None
    for i, record in enumerate(ws.iter_rows(values_only=True), start=1):
        if i == 1:
            continue
        full_name = str(record[0]).strip() if record and record[0] else None
        short_name = str(record[1]).strip() if len(record) > 1 and record[1] else None
        time_series = str(record[2]).strip() if len(record) > 2 and record[2] is not None else None
        if not full_name:
            continue

        is_group = short_name is None and time_series is None
        if is_group:
            section = full_name
        start_year, end_year = _year_bounds(time_series)
        rows.append({
            "section": section,
            "full_name": full_name,
            "short_name": short_name,
            "time_series": time_series,
            "start_year": start_year,
            "end_year": end_year,
            "is_group": is_group,
        })
    wb.close()

    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 rows from HDR metadata codebook")
    table = pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA)
    save_raw_parquet(table, node_id)
