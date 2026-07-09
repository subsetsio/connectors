"""Maddison Project source-reference sheets."""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import load_workbook

SOURCE_SCHEMA = pa.schema([
    ("countrycode", pa.string()),
    ("country", pa.string()),
    ("period", pa.string()),
    ("source", pa.string()),
    ("source_order", pa.int64()),
])


def _text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_source_sheet(sheet_name: str) -> list[dict]:
    wb = load_workbook()
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    header_idx = None
    for idx, row in enumerate(rows):
        labels = [_text(cell) for cell in row[:3]]
        if labels[:3] == ["ISO code", "Country", "Source"]:
            header_idx = idx
            break
    assert header_idx is not None, f"{sheet_name}: header row not found"

    out = []
    current_code = None
    current_country = None
    source_order = 0
    for row in rows[header_idx + 1:]:
        iso_code = _text(row[0]) if len(row) > 0 else None
        country_or_period = _text(row[1]) if len(row) > 1 else None
        source = _text(row[2]) if len(row) > 2 else None

        if iso_code:
            current_code = iso_code
            current_country = country_or_period

        if not source:
            continue
        assert current_code, f"{sheet_name}: source row before country header"
        source_order += 1
        out.append({
            "countrycode": current_code,
            "country": current_country,
            "period": country_or_period if not iso_code else None,
            "source": source,
            "source_order": source_order,
        })

    assert out, f"{sheet_name}: no source rows parsed"
    return out


def fetch_sources(node_id: str) -> None:
    rows = _parse_source_sheet("Sources")
    table = pa.Table.from_pylist(rows, schema=SOURCE_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_original_sources(node_id: str) -> None:
    rows = _parse_source_sheet("Maddison original sources")
    table = pa.Table.from_pylist(rows, schema=SOURCE_SCHEMA)
    save_raw_parquet(table, node_id)
