"""Statistik Nord connector.

The initial published subset is the latest Schleswig-Holstein consumer price
index workbook. The CKAN package points to an XLSX publication; the workbook's
Tab_2 sheet carries a compact monthly history, so download normalizes that sheet
to SQL-readable parquet instead of storing opaque XLSX bytes.
"""

from __future__ import annotations

import datetime as dt
import io

import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

CKAN_PACKAGE_SHOW = "https://opendata.schleswig-holstein.de/api/3/action/package_show"
PREFIX = "statistik-nord-"

ENTITY_IDS = [
    "verbraucherpreisindex-schleswig-holstein-juni-2026",
]

MONTHS = {
    "Jan.": 1,
    "Feb.": 2,
    "Marz": 3,
    "März": 3,
    "April": 4,
    "Mai": 5,
    "Juni": 6,
    "Juli": 7,
    "Aug.": 8,
    "Sept.": 9,
    "Okt.": 10,
    "Nov.": 11,
    "Dez.": 12,
}

SCHEMA = pa.schema(
    [
        ("entity_id", pa.string()),
        ("release_title", pa.string()),
        ("source_package_id", pa.string()),
        ("source_url", pa.string()),
        ("measure", pa.string()),
        ("date", pa.date32()),
        ("year", pa.int16()),
        ("month", pa.int8()),
        ("value", pa.float64()),
    ]
)


def _package_show(entity_id: str) -> dict:
    resp = get(CKAN_PACKAGE_SHOW, params={"id": entity_id}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {entity_id}: {payload!r}")
    return payload["result"]


def _xlsx_url(package: dict) -> str:
    for resource in package.get("resources", []):
        if (resource.get("format") or "").upper() == "XLSX" and resource.get("url"):
            return resource["url"]
    raise RuntimeError(f"{package.get('name')}: no XLSX resource found")


def _download_workbook(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _parse_tab_2(entity_id: str, package: dict, url: str, content: bytes) -> list[dict]:
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    sheet_name = next((name for name in wb.sheetnames if name.strip() == "Tab_2"), None)
    if not sheet_name:
        raise RuntimeError(f"{entity_id}: workbook has no Tab_2 sheet; sheets={wb.sheetnames!r}")
    ws = wb[sheet_name]

    rows = []
    measure = None
    for raw in ws.iter_rows(values_only=True):
        cells = list(raw)
        label = str(cells[1]).strip() if len(cells) > 1 and cells[1] is not None else ""
        if "Indexstand" in label:
            measure = "index_2020_100"
            continue
        if "Veränderung gegenüber dem entsprechenden Vorjahresergebnis" in label:
            measure = "annual_change_pct"
            continue

        year = cells[0] if cells else None
        if measure is None or not isinstance(year, int):
            continue

        for col_idx, month_name in enumerate(MONTHS, start=1):
            if col_idx >= len(cells):
                continue
            value = cells[col_idx]
            if value is None:
                continue
            rows.append(
                {
                    "entity_id": entity_id,
                    "release_title": package.get("title") or package.get("name") or entity_id,
                    "source_package_id": package.get("id"),
                    "source_url": url,
                    "measure": measure,
                    "date": dt.date(year, MONTHS[month_name], 1),
                    "year": year,
                    "month": MONTHS[month_name],
                    "value": float(value),
                }
            )

    if not rows:
        raise RuntimeError(f"{entity_id}: parsed 0 rows from Tab_2")
    return rows


def fetch_one(node_id: str) -> None:
    entity_id = node_id.removeprefix(PREFIX)
    if entity_id not in ENTITY_IDS:
        raise RuntimeError(f"unknown Statistik Nord entity id: {entity_id}")

    package = _package_show(entity_id)
    url = _xlsx_url(package)
    content = _download_workbook(url)
    rows = _parse_tab_2(entity_id, package, url, content)
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
