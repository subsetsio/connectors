from __future__ import annotations

from io import BytesIO
import posixpath
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import pandas as pd
from subsets_utils import NodeSpec, get, save_raw_ndjson


BASE_URL = "https://www.safe.gov.cn"

ARTICLE_PATHS = {
    "article-safe-2015-0630-3269": "/safe/2015/0630/3269.html",
    "article-safe-2018-0209-8254": "/safe/2018/0209/8254.html",
    "article-safe-2018-0329-8810": "/safe/2018/0329/8810.html",
    "article-safe-2018-0410-8816": "/safe/2018/0410/8816.html",
    "article-safe-2018-0410-8817": "/safe/2018/0410/8817.html",
    "article-safe-2018-0419-8806": "/safe/2018/0419/8806.html",
    "article-safe-2019-0419-13027": "/safe/2019/0419/13027.html",
    "article-safe-2019-0627-13519": "/safe/2019/0627/13519.html",
    "article-safe-2019-0627-13520": "/safe/2019/0627/13520.html",
    "article-safe-2020-1218-17833": "/safe/2020/1218/17833.html",
    "article-safe-2023-0215-22329": "/safe/2023/0215/22329.html",
    "article-safe-2026-0205-27113": "/safe/2026/0205/27113.html",
    "article-safe-2026-0227-27170": "/safe/2026/0227/27170.html",
    "article-safe-2026-0228-27175": "/safe/2026/0228/27175.html",
    "article-safe-2026-0529-27515": "/safe/2026/0529/27515.html",
    "article-safe-2026-0625-27610": "/safe/2026/0625/27610.html",
}


def _entity_from_node_id(node_id: str) -> str:
    prefix = "safe-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected SAFE node id: {node_id}")
    return node_id.removeprefix(prefix)


def _absolute_url(href: str, page_path: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return BASE_URL + posixpath.normpath(posixpath.join(posixpath.dirname(page_path), href))


def _clean_html_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def _article_title(page_html: str) -> str:
    match = re.search(r'<meta name="ArticleTitle" content="([^"]+)"', page_html)
    if match:
        return _clean_html_text(match.group(1))
    match = re.search(r'<div class="detail_tit[^"]*">(.+?)</div>', page_html, re.S)
    return _clean_html_text(match.group(1)) if match else ""


def _attachment_links(page_html: str, page_path: str) -> list[dict[str, str]]:
    links = []
    for href, title in re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*?(?:title="([^"]*)")?[^>]*>', page_html, re.I):
        ext = href.rsplit(".", 1)[-1].lower().split("?", 1)[0]
        if ext not in {"xlsx", "xls", "docx"}:
            continue
        links.append(
            {
                "url": _absolute_url(href, page_path),
                "title": _clean_html_text(title) if title else "",
                "extension": ext,
            }
        )
    return links


def _value_text(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text if text else None


def _rows_from_excel(content: bytes, attachment: dict[str, str], attachment_index: int, base: dict) -> list[dict]:
    rows = []
    sheets = pd.read_excel(BytesIO(content), sheet_name=None, header=None, dtype=object)
    for sheet_name, frame in sheets.items():
        for row_idx, row in frame.iterrows():
            for col_idx, value in enumerate(row.tolist()):
                text = _value_text(value)
                if text is None:
                    continue
                rows.append(
                    {
                        **base,
                        "attachment_index": attachment_index,
                        "attachment_title": attachment["title"],
                        "attachment_extension": attachment["extension"],
                        "attachment_url": attachment["url"],
                        "container_name": str(sheet_name),
                        "table_index": None,
                        "row_index": int(row_idx) + 1,
                        "column_index": int(col_idx) + 1,
                        "value_text": text,
                    }
                )
    return rows


def _rows_from_docx(content: bytes, attachment: dict[str, str], attachment_index: int, base: dict) -> list[dict]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    rows = []
    with ZipFile(BytesIO(content)) as docx:
        root = ET.fromstring(docx.read("word/document.xml"))
    for table_idx, table in enumerate(root.findall(".//w:tbl", ns), start=1):
        for row_idx, tr in enumerate(table.findall("./w:tr", ns), start=1):
            for col_idx, tc in enumerate(tr.findall("./w:tc", ns), start=1):
                text = "".join(t.text or "" for t in tc.findall(".//w:t", ns)).strip()
                if not text:
                    continue
                rows.append(
                    {
                        **base,
                        "attachment_index": attachment_index,
                        "attachment_title": attachment["title"],
                        "attachment_extension": attachment["extension"],
                        "attachment_url": attachment["url"],
                        "container_name": "word/document.xml",
                        "table_index": table_idx,
                        "row_index": row_idx,
                        "column_index": col_idx,
                        "value_text": text,
                    }
                )
    return rows


def _rows_from_html_tables(page_html: str, base: dict) -> list[dict]:
    try:
        tables = pd.read_html(BytesIO(page_html.encode("utf-8")), header=None)
    except ValueError:
        return []
    rows = []
    for table_idx, frame in enumerate(tables, start=1):
        for row_idx, row in frame.iterrows():
            for col_idx, value in enumerate(row.tolist()):
                text = _value_text(value)
                if text is None:
                    continue
                rows.append(
                    {
                        **base,
                        "attachment_index": None,
                        "attachment_title": None,
                        "attachment_extension": "html",
                        "attachment_url": base["article_url"],
                        "container_name": "article_html",
                        "table_index": table_idx,
                        "row_index": int(row_idx) + 1,
                        "column_index": int(col_idx) + 1,
                        "value_text": text,
                    }
                )
    return rows


def fetch_article_tables(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    page_path = ARTICLE_PATHS[entity_id]
    article_url = BASE_URL + page_path
    page_resp = get(article_url, timeout=60)
    page_resp.raise_for_status()
    page_html = page_resp.text
    base = {
        "source_entity_id": entity_id,
        "article_url": article_url,
        "article_title": _article_title(page_html),
    }

    rows = []
    for attachment_index, attachment in enumerate(_attachment_links(page_html, page_path), start=1):
        resp = get(attachment["url"], timeout=120)
        resp.raise_for_status()
        if attachment["extension"] in {"xlsx", "xls"}:
            rows.extend(_rows_from_excel(resp.content, attachment, attachment_index, base))
        elif attachment["extension"] == "docx":
            rows.extend(_rows_from_docx(resp.content, attachment, attachment_index, base))

    if not rows:
        rows = _rows_from_html_tables(page_html, base)

    if not rows:
        raise ValueError(f"{entity_id}: no XLS/XLSX/DOCX/HTML table rows found")

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="safe-article-safe-2015-0630-3269", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2018-0209-8254", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2018-0329-8810", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2018-0410-8816", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2018-0410-8817", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2018-0419-8806", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2019-0419-13027", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2019-0627-13519", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2019-0627-13520", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2020-1218-17833", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2023-0215-22329", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2026-0205-27113", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2026-0227-27170", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2026-0228-27175", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2026-0529-27515", fn=fetch_article_tables),
    NodeSpec(id="safe-article-safe-2026-0625-27610", fn=fetch_article_tables),
]
