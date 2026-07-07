from __future__ import annotations

import csv
import io
import posixpath
import re
import zipfile
from datetime import UTC, datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import pandas as pd
from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, save_raw_ndjson


CATALOG_URL = "https://www.statssa.gov.za/?page_id=1847"
SPEC_PRODUCTS = "stats-sa-time-series-products"
SPEC_VALUES = "stats-sa-time-series-values"


class _TimeSeriesParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_tr = False
        self.in_td = False
        self.current_cells: list[dict] = []
        self.current_text: list[str] = []
        self.current_links: list[str] = []
        self.rows: list[list[dict]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "tr":
            self.in_tr = True
            self.current_cells = []
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.current_text = []
            self.current_links = []
        elif tag == "a" and self.in_td:
            href = attrs_dict.get("href")
            if href:
                self.current_links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self.in_td:
            text = _clean_text(" ".join(self.current_text))
            self.current_cells.append({"text": text, "links": list(self.current_links)})
            self.in_td = False
        elif tag == "tr" and self.in_tr:
            if self.current_cells:
                self.rows.append(self.current_cells)
            self.in_tr = False

    def handle_data(self, data: str) -> None:
        if self.in_td:
            self.current_text.append(data)


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def _assert_not_interstitial(text: str, url: str) -> None:
    lowered = text.lower()
    if "incapsula" in lowered or "_incapsula_resource" in lowered:
        raise RuntimeError(f"Stats SA returned Incapsula interstitial for {url}")


def _fetch_catalog_html() -> str:
    response = get(CATALOG_URL, timeout=60.0)
    response.raise_for_status()
    text = response.text
    _assert_not_interstitial(text, CATALOG_URL)
    if "Time series data" not in text:
        raise RuntimeError("Stats SA catalogue response did not contain the expected title")
    return text


def _normalise_link(href: str) -> str:
    return urljoin(CATALOG_URL, href)


def _link_format(url: str) -> str | None:
    path = urlparse(url).path.lower()
    if not path.endswith(".zip"):
        return None
    if "ascii" in path:
        return "ascii"
    if "excel" in path or "xls" in path:
        return "excel"
    return "zip"


def _catalog_products() -> list[dict]:
    parser = _TimeSeriesParser()
    parser.feed(_fetch_catalog_html())
    products: list[dict] = []

    for cells in parser.rows:
        if not cells:
            continue
        title = _clean_text(cells[0]["text"])
        if not title or title.lower().startswith("publication number"):
            continue
        if ".zip" not in title.lower():
            continue

        links = []
        for cell in cells[1:]:
            for href in cell["links"]:
                url = _normalise_link(href)
                fmt = _link_format(url)
                if fmt:
                    links.append({"url": url, "format": fmt})

        product_id = _slug(title.removesuffix(".zip"))
        products.append(
            {
                "product_id": product_id,
                "title": title,
                "excel_available": any(link["format"] == "excel" for link in links),
                "ascii_available": any(link["format"] == "ascii" for link in links),
                "link_count": len(links),
                "links": links,
            }
        )

    if not products:
        raise RuntimeError("No Stats SA time-series products were parsed from the catalogue")
    return products


def fetch_products(node_id: str) -> None:
    products = _catalog_products()
    fetched_at = datetime.now(UTC).isoformat()
    rows = [
        {
            "product_id": product["product_id"],
            "title": product["title"],
            "excel_available": product["excel_available"],
            "ascii_available": product["ascii_available"],
            "link_count": product["link_count"],
            "fetched_at": fetched_at,
        }
        for product in products
    ]
    save_raw_ndjson(rows, node_id)


def _preferred_link(product: dict) -> dict | None:
    ascii_links = [link for link in product["links"] if link["format"] == "ascii"]
    excel_links = [link for link in product["links"] if link["format"] == "excel"]
    return (ascii_links or excel_links or product["links"] or [None])[0]


def _download_zip(url: str) -> bytes:
    response = get(url, timeout=120.0)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "html" in content_type.lower():
        _assert_not_interstitial(response.text, url)
        raise RuntimeError(f"Stats SA returned HTML instead of ZIP for {url}")
    if not response.content.startswith(b"PK"):
        raise RuntimeError(f"Stats SA response for {url} is not a ZIP payload")
    return response.content


def _records_from_ascii(product: dict, file_name: str, data: bytes) -> list[dict]:
    text = data.decode("utf-8", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(text), dialect)
    rows = []
    for row_number, row in enumerate(reader, start=1):
        if not row or not any(cell.strip() for cell in row):
            continue
        rows.append(
            {
                "product_id": product["product_id"],
                "product_title": product["title"],
                "source_file": file_name,
                "source_format": "ascii",
                "sheet_name": None,
                "row_number": row_number,
                "row_values": row,
                "row_object": None,
                "fetched_at": product["fetched_at"],
            }
        )
    return rows


def _records_from_excel(product: dict, file_name: str, data: bytes) -> list[dict]:
    workbook = pd.read_excel(io.BytesIO(data), sheet_name=None, header=None, dtype=object)
    rows = []
    for sheet_name, frame in workbook.items():
        frame = frame.dropna(how="all")
        for idx, row in frame.iterrows():
            values = [None if pd.isna(value) else value for value in row.tolist()]
            if not any(value not in (None, "") for value in values):
                continue
            rows.append(
                {
                    "product_id": product["product_id"],
                    "product_title": product["title"],
                    "source_file": file_name,
                    "source_format": "excel",
                    "sheet_name": str(sheet_name),
                    "row_number": int(idx) + 1,
                "row_values": values,
                "row_object": None,
                "fetched_at": product["fetched_at"],
            }
        )
    return rows


def fetch_values(node_id: str) -> None:
    products = _catalog_products()
    fetched_at = datetime.now(UTC).isoformat()
    for product in products:
        product["fetched_at"] = fetched_at
    selected = [(product, _preferred_link(product)) for product in products]
    selected = [(product, link) for product, link in selected if link is not None]
    if not selected:
        raise RuntimeError("Stats SA catalogue did not expose any ZIP download links")

    rows = []
    for product, link in selected:
        payload = _download_zip(link["url"])
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            for member in archive.namelist():
                if member.endswith("/") or posixpath.basename(member).startswith("."):
                    continue
                suffix = posixpath.splitext(member)[1].lower()
                data = archive.read(member)
                if link["format"] == "ascii" or suffix in {".txt", ".csv", ".asc"}:
                    rows.extend(_records_from_ascii(product, member, data))
                elif suffix in {".xls", ".xlsx"}:
                    rows.extend(_records_from_excel(product, member, data))

    if not rows:
        raise RuntimeError("Downloaded Stats SA ZIP files contained no tabular rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=SPEC_PRODUCTS, fn=fetch_products),
    NodeSpec(id=SPEC_VALUES, fn=fetch_values),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=SPEC_PRODUCTS,
        description="Stats SA time-series catalogue; refreshed weekly (inferred from regularly updated release page).",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=7),
    ),
    MaintainSpec(
        asset_id=SPEC_VALUES,
        description="Stats SA time-series files; refreshed weekly (inferred from regularly updated release page).",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=7),
    ),
]
