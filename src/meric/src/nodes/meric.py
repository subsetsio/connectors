"""MERIC public data tables.

MERIC publishes Missouri labor-market and economic statistics as Drupal data
pages. Most accepted entities render an HTML table for the current/default
selection and expose a page-level download control; WIOA demographics is an
Excel download linked from the Regional Profiles page. There is no documented
API route, so each node performs a stateless full re-pull of one page/file and
normalizes the visible tabular content to NDJSON.

The site is protected by Incapsula/Imperva in some environments. Fetches reject
challenge pages explicitly so a blocked run fails loudly instead of saving the
challenge HTML as data.
"""

from __future__ import annotations

import html
import re
import zipfile
from html.parser import HTMLParser
from io import BytesIO
from xml.etree import ElementTree as ET

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, configure_http, get, save_raw_ndjson

SLUG = "meric"
BASE = "https://meric.mo.gov"

ENTITY_URLS = {
    "career-pathways": f"{BASE}/data/occupation/career-pathways",
    "cost-of-living": f"{BASE}/data/cost-living-data-series",
    "county-average-wages": f"{BASE}/data/county-average-wages",
    "current-employment-statistics": f"{BASE}/data/industry/current-employment-statistics",
    "industry-employment-projections": f"{BASE}/data/industry/industry-employment-projections",
    "occupational-employment-wages": f"{BASE}/data/occupation/occupational-employment-wages",
    "occupational-projections": f"{BASE}/data/occupation/occupational-projections",
    "qcew-by-geographic-area": f"{BASE}/data/industry/quarterly-census-employment-wages-qcew-ga",
    "qcew-by-industry": f"{BASE}/data/industry/quarterly-census-employment-wages-qcew-in",
    "unemployment-rates": f"{BASE}/data/economic/local-area-unemployment-statistics/laus",
    "wioa-county-demographics": f"{BASE}/media/3991/download",
}

_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
_http_configured = False


class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._in_table = False
        self._in_row = False
        self._in_cell = False
        self._current_table: list[list[str]] = []
        self._current_row: list[str] = []
        self._cell_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._in_table = True
            self._current_table = []
        elif self._in_table and tag == "tr":
            self._in_row = True
            self._current_row = []
        elif self._in_row and tag in {"td", "th"}:
            self._in_cell = True
            self._cell_parts = []

    def handle_endtag(self, tag):
        if self._in_cell and tag in {"td", "th"}:
            text = _clean_text(" ".join(self._cell_parts))
            self._current_row.append(text)
            self._cell_parts = []
            self._in_cell = False
        elif self._in_row and tag == "tr":
            if any(cell for cell in self._current_row):
                self._current_table.append(self._current_row)
            self._current_row = []
            self._in_row = False
        elif self._in_table and tag == "table":
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = []
            self._in_table = False

    def handle_data(self, data):
        if self._in_cell:
            self._cell_parts.append(data)


def _ensure_http():
    global _http_configured
    if not _http_configured:
        configure_http(headers=_HTTP_HEADERS)
        _http_configured = True


def _entity_id_from_node(node_id: str) -> str:
    return node_id[len(SLUG) + 1 :]


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def _slug(value: str, fallback: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not out:
        out = fallback
    if out[0].isdigit():
        out = f"c_{out}"
    return out


def _headers(row: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for i, value in enumerate(row):
        base = _slug(value, f"col_{i + 1}")
        n = seen.get(base, 0) + 1
        seen[base] = n
        out.append(base if n == 1 else f"{base}_{n}")
    return out


def _reject_block_page(text: str, url: str) -> None:
    lowered = text.lower()
    if "incapsula" in lowered or "_incapsula_resource" in lowered:
        raise RuntimeError(f"{url}: blocked by Incapsula/Imperva challenge")
    if "request unsuccessful" in lowered and "incident id" in lowered:
        raise RuntimeError(f"{url}: received WAF challenge page")


def _fetch(url: str) -> bytes:
    _ensure_http()
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _html_records(entity_id: str, url: str, content: bytes) -> list[dict]:
    text = content.decode("utf-8", errors="replace")
    _reject_block_page(text, url)
    parser = _TableParser()
    parser.feed(text)
    records: list[dict] = []
    for table_index, table in enumerate(parser.tables, start=1):
        if len(table) < 2:
            continue
        header = _headers(table[0])
        for row_index, row in enumerate(table[1:], start=1):
            if not any(row):
                continue
            rec = {
                "_entity_id": entity_id,
                "_source_url": url,
                "_table_index": table_index,
                "_row_index": row_index,
            }
            for i, name in enumerate(header):
                rec[name] = row[i] if i < len(row) else None
            records.append(rec)
    if not records:
        raise RuntimeError(f"{url}: no HTML table rows found")
    return records


def _xlsx_shared_strings(root: ET.Element) -> list[str]:
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings = []
    for si in root.findall("x:si", ns):
        parts = [t.text or "" for t in si.findall(".//x:t", ns)]
        strings.append("".join(parts))
    return strings


def _xlsx_cell_value(cell: ET.Element, shared: list[str]) -> str | None:
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    typ = cell.get("t")
    if typ == "inlineStr":
        return _clean_text("".join(t.text or "" for t in cell.findall(".//x:t", ns)))
    value = cell.findtext("x:v", namespaces=ns)
    if value is None:
        return None
    if typ == "s":
        return _clean_text(shared[int(value)])
    return _clean_text(value)


def _xlsx_records(entity_id: str, url: str, content: bytes) -> list[dict]:
    records: list[dict] = []
    with zipfile.ZipFile(BytesIO(content)) as zf:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            shared = _xlsx_shared_strings(ET.fromstring(zf.read("xl/sharedStrings.xml")))
        sheet_names = sorted(
            name
            for name in zf.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )
        ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        for sheet_index, sheet_name in enumerate(sheet_names, start=1):
            root = ET.fromstring(zf.read(sheet_name))
            rows = []
            for row in root.findall(".//x:sheetData/x:row", ns):
                values = [_xlsx_cell_value(c, shared) for c in row.findall("x:c", ns)]
                if any(v not in (None, "") for v in values):
                    rows.append([v or "" for v in values])
            if len(rows) < 2:
                continue
            header = _headers(rows[0])
            for row_index, row in enumerate(rows[1:], start=1):
                rec = {
                    "_entity_id": entity_id,
                    "_source_url": url,
                    "_sheet_index": sheet_index,
                    "_row_index": row_index,
                }
                for i, name in enumerate(header):
                    rec[name] = row[i] if i < len(row) else None
                records.append(rec)
    if not records:
        raise RuntimeError(f"{url}: no Excel rows found")
    return records


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    url = ENTITY_URLS[entity_id]
    content = _fetch(url)
    if entity_id == "wioa-county-demographics":
        records = _xlsx_records(entity_id, url, content)
    else:
        records = _html_records(entity_id, url, content)
    save_raw_ndjson(records, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
