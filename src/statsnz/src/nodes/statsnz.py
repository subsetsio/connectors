"""Stats NZ downloadable CSV connector.

Stats NZ publishes a public "CSV files for download" page with a structured
Silverstripe pageViewData JSON payload. Each accepted entity is one CSV or ZIP
asset linked from that page. The files are heterogeneous, and ZIPs may contain
one or more CSVs, so the download stage keeps values as strings in NDJSON and
lets the transform stage type each table from observed raw.
"""

import csv
import html
import io
import json
import re
import zipfile
from urllib.parse import urljoin

import pandas as pd

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson

SLUG = "statsnz"
PAGE_URL = "https://www.stats.govt.nz/large-datasets/csv-files-for-download/"


def _slug(value: str) -> str:
    value = value.rsplit(".", 1)[0].lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _page_view_data(page_html: str) -> dict:
    match = re.search(r'<div id="pageViewData" data-value="(.*?)"></div>', page_html, re.S)
    if not match:
        raise RuntimeError("Stats NZ pageViewData block not found")
    return json.loads(html.unescape(match.group(1)))


def _catalog_by_entity_id() -> dict[str, dict]:
    resp = get(PAGE_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = _page_view_data(resp.text)
    out: dict[str, dict] = {}
    seen: set[str] = set()
    for block in data.get("PageBlocks", []):
        for doc in block.get("BlockDocuments", []) or []:
            ext = str(doc.get("DocumentExtension") or "").lower()
            if ext not in {"csv", "zip"}:
                continue
            filename = doc.get("FileName") or doc.get("Name") or str(doc.get("ID") or "")
            entity_id = _slug(filename) or f"document-{doc.get('ID')}"
            if entity_id in seen:
                entity_id = f"{entity_id}-{doc.get('ID')}"
            seen.add(entity_id)
            out[entity_id] = doc
    return out


def _entity_id_from_node(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _decode_csv(content: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", "replace")


def _unique_headers(headers: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    out: list[str] = []
    for i, header in enumerate(headers):
        name = (header or "").strip() or f"column_{i + 1}"
        count = counts.get(name, 0)
        counts[name] = count + 1
        out.append(name if count == 0 else f"{name}_{count + 1}")
    return out


def _rows_from_csv(content: bytes, source_file: str) -> list[dict]:
    text = _decode_csv(content)
    reader = csv.reader(io.StringIO(text))
    try:
        headers = _unique_headers(next(reader))
    except StopIteration:
        return []

    rows: list[dict] = []
    for row_number, values in enumerate(reader, start=2):
        if not values or all(not str(v).strip() for v in values):
            continue
        record = {
            "source_file": source_file,
            "row_number": row_number,
        }
        for i, value in enumerate(values):
            key = headers[i] if i < len(headers) else f"extra_column_{i + 1}"
            record[key] = value
        rows.append(record)
    return rows


def _cell_to_string(value) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def _rows_from_excel(content: bytes, source_file: str) -> list[dict]:
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, dtype=object)
    rows: list[dict] = []
    for sheet_name, frame in sheets.items():
        frame = frame.dropna(axis=0, how="all").dropna(axis=1, how="all")
        for index, values in frame.iterrows():
            record = {
                "source_file": source_file,
                "sheet_name": str(sheet_name),
                "row_number": int(index) + 1,
            }
            for i, value in enumerate(values, start=1):
                record[f"column_{i}"] = _cell_to_string(value)
            rows.append(record)
    return rows


def _rows_from_payload(content: bytes, filename: str) -> list[dict]:
    if filename.lower().endswith(".zip"):
        rows: list[dict] = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for name in sorted(zf.namelist()):
                if name.endswith("/"):
                    continue
                member = zf.read(name)
                if name.lower().endswith(".zip"):
                    rows.extend(_rows_from_payload(member, name))
                elif name.lower().endswith(".csv"):
                    rows.extend(_rows_from_csv(member, name))
                elif name.lower().endswith((".xls", ".xlsx")):
                    rows.extend(_rows_from_excel(member, name))
        return rows
    if filename.lower().endswith((".xls", ".xlsx")):
        return _rows_from_excel(content, filename)
    return _rows_from_csv(content, filename)


def _normalize_rows(rows: list[dict]) -> list[dict]:
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)
    return [{key: row.get(key) for key in keys} for row in rows]


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    catalog = _catalog_by_entity_id()
    doc = catalog[entity_id]
    url = urljoin(PAGE_URL, doc["DocumentLink"])
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    filename = doc.get("FileName") or url.rsplit("/", 1)[-1]
    rows = _rows_from_payload(resp.content, filename)
    if not rows:
        raise RuntimeError(f"{entity_id}: no CSV rows found in downloaded asset")
    save_raw_ndjson(_normalize_rows(rows), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
