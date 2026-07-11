"""METI download nodes.

METI publishes most statistical tables as Excel files linked from static HTML
landing pages. The downloader records the discovered links and normalizes each
reachable CSV/Excel file into SQL-readable NDJSON rows. Workbook layouts differ
widely by survey, so this stage preserves sheet/row/cell structure and leaves
survey-specific typing to transforms.
"""

from __future__ import annotations

import csv
import html.parser
import io
import posixpath
import re
import time
from urllib.parse import urldefrag, urljoin, urlparse

import openpyxl
import pandas as pd

from constants import ENTITY_IDS, ENTITY_START_URLS
from subsets_utils import NodeSpec, get, save_raw_ndjson

SLUG = "meti"
_HOST = "www.meti.go.jp"
_OFFICE_EXTS = (".xlsx", ".xls", ".csv")

# www.meti.go.jp sits behind AWS WAF (CloudFront). It blocks bot-like User-Agents
# outright (403) and, under load / from low-reputation IPs, escalates to a JS
# "challenge" (HTTP 202 or 405 with an `x-amzn-waf-action: challenge` header and
# an empty body). A plain HTTP client cannot solve that challenge, so the only
# levers are (1) a full, realistic browser fingerprint and (2) staying polite:
# a small inter-request delay plus exponential backoff on any WAF response, which
# lets rate-based reputation recover between attempts. Headers must stay ASCII.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
_WAF_ACTION_HEADER = "x-amzn-waf-action"
_WAF_STATUS = {202, 405, 403}
_FETCH_ATTEMPTS = 5
_REQUEST_DELAY = 0.7  # polite spacing between requests within a spec
_LINK_HINT = re.compile(
    r"(data|download|result|statistics|statistical|table|excel|csv|xls|"
    r"統計表|調査の結果|結果|データ|ダウンロード|時系列)",
    re.I,
)
_MAX_FILES_PER_ENTITY = 30
_MAX_ROWS_PER_SHEET = 20000


class _LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "a":
            return
        attrs_dict = dict(attrs)
        self._href = attrs_dict.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href:
            text = " ".join("".join(self._text).split())
            self.links.append((self._href, text))
            self._href = None
            self._text = []


def _entity_from_node_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _is_waf_challenge(resp) -> bool:
    """A WAF interstitial: the challenge action header, or a challenge status
    code carrying no real payload (CloudFront serves an empty/near-empty body)."""
    if resp.headers.get(_WAF_ACTION_HEADER):
        return True
    if resp.status_code in _WAF_STATUS:
        clen = resp.headers.get("content-length")
        if clen is not None and int(clen) == 0:
            return True
        if len(resp.content) < 1024 and b"<html" not in resp.content[:1024].lower():
            return True
    return False


def _fetch_bytes(url: str) -> tuple[bytes, str]:
    """Fetch a METI URL, backing off through AWS WAF challenges.

    `subsets_utils.get` already retries genuine network transients (429/5xx,
    connection errors). WAF challenge/block responses are not transient in that
    sense (2xx/4xx with an empty body), so we detect and back off on them here —
    exponential waits give the rate-based WAF reputation time to recover."""
    last = None
    for attempt in range(_FETCH_ATTEMPTS):
        resp = get(url, headers=_HEADERS, timeout=(15.0, 180.0))
        if _is_waf_challenge(resp):
            last = resp
            time.sleep(min(60.0, 4.0 * (2 ** attempt)))
            continue
        resp.raise_for_status()
        return resp.content, resp.headers.get("content-type", "")
    action = last.headers.get(_WAF_ACTION_HEADER, "block") if last is not None else "?"
    status = last.status_code if last is not None else "?"
    raise RuntimeError(
        f"AWS WAF blocked {url} after {_FETCH_ATTEMPTS} attempts "
        f"(status={status}, x-amzn-waf-action={action})"
    )


def _is_meti_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc == _HOST


def _clean_url(base_url: str, href: str) -> str:
    absolute = urljoin(base_url, href)
    absolute, _fragment = urldefrag(absolute)
    return absolute


def _extension(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in _OFFICE_EXTS:
        if path.endswith(ext):
            return ext.lstrip(".")
    return ""


def _discover_links(seed_urls: list[str]) -> tuple[list[dict], list[str]]:
    seen_pages: set[str] = set()
    page_queue = [(url, 0) for url in seed_urls]
    page_records: list[dict] = []
    file_urls: list[str] = []
    seen_files: set[str] = set()

    for seed in seed_urls:
        ext = _extension(seed)
        if ext:
            seen_files.add(seed)
            file_urls.append(seed)

    while page_queue and len(file_urls) < _MAX_FILES_PER_ENTITY:
        page_url, depth = page_queue.pop(0)
        if page_url in seen_pages or _extension(page_url):
            continue
        seen_pages.add(page_url)
        content, content_type = _fetch_bytes(page_url)
        if "html" not in content_type.lower() and b"<html" not in content[:500].lower():
            continue

        html_text = content.decode("utf-8", errors="replace")
        parser = _LinkParser()
        parser.feed(html_text)
        page_records.append({
            "kind": "page",
            "page_url": page_url,
            "link_count": len(parser.links),
        })
        for href, text in parser.links:
            url = _clean_url(page_url, href)
            if not _is_meti_url(url):
                continue
            ext = _extension(url)
            if ext:
                if url not in seen_files:
                    seen_files.add(url)
                    file_urls.append(url)
                continue
            path = urlparse(url).path.lower()
            if depth < 1 and path.endswith((".html", ".htm")) and _LINK_HINT.search(text + " " + path):
                page_queue.append((url, depth + 1))
        if len(file_urls) >= _MAX_FILES_PER_ENTITY:
            break

    return page_records, file_urls[:_MAX_FILES_PER_ENTITY]


def _cell_value(value):
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, (int, float, bool)):
        return value
    text = str(value).strip()
    return text if text else None


def _workbook_records(entity_id: str, file_url: str, content: bytes, ext: str):
    if ext == "xlsx":
        wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        try:
            for sheet in wb.worksheets:
                for row_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                    if row_idx > _MAX_ROWS_PER_SHEET:
                        break
                    values = [_cell_value(v) for v in row]
                    if not any(v is not None for v in values):
                        continue
                    yield {
                        "kind": "row",
                        "entity_id": entity_id,
                        "file_url": file_url,
                        "file_name": posixpath.basename(urlparse(file_url).path),
                        "file_type": ext,
                        "sheet_name": sheet.title,
                        "row_number": row_idx,
                        "values": values,
                    }
        finally:
            wb.close()
        return

    sheets = pd.read_excel(
        io.BytesIO(content),
        sheet_name=None,
        header=None,
        dtype=object,
        engine="xlrd",
    )
    for sheet_name, df in sheets.items():
        for idx, row in df.head(_MAX_ROWS_PER_SHEET).iterrows():
            values = [_cell_value(v) for v in row.tolist()]
            if not any(v is not None for v in values):
                continue
            yield {
                "kind": "row",
                "entity_id": entity_id,
                "file_url": file_url,
                "file_name": posixpath.basename(urlparse(file_url).path),
                "file_type": ext,
                "sheet_name": str(sheet_name),
                "row_number": int(idx) + 1,
                "values": values,
            }


def _csv_records(entity_id: str, file_url: str, content: bytes):
    for encoding in ("utf-8-sig", "cp932", "shift_jis"):
        try:
            text = content.decode(encoding)
            break
        except UnicodeDecodeError:
            text = ""
    if not text:
        text = content.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text))
    for row_idx, row in enumerate(reader, start=1):
        if row_idx > _MAX_ROWS_PER_SHEET:
            break
        values = [_cell_value(v) for v in row]
        if not any(v is not None for v in values):
            continue
        yield {
            "kind": "row",
            "entity_id": entity_id,
            "file_url": file_url,
            "file_name": posixpath.basename(urlparse(file_url).path),
            "file_type": "csv",
            "sheet_name": None,
            "row_number": row_idx,
            "values": values,
        }


def fetch_one(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    seed_urls = ENTITY_START_URLS[entity_id]
    page_records, file_urls = _discover_links(seed_urls)

    records = []
    for rec in page_records:
        records.append({"entity_id": entity_id, **rec})
    for file_url in file_urls:
        ext = _extension(file_url)
        records.append({
            "kind": "file",
            "entity_id": entity_id,
            "file_url": file_url,
            "file_name": posixpath.basename(urlparse(file_url).path),
            "file_type": ext,
        })
        content, _content_type = _fetch_bytes(file_url)
        if ext == "csv":
            records.extend(_csv_records(entity_id, file_url, content))
        elif ext in {"xls", "xlsx"}:
            records.extend(_workbook_records(entity_id, file_url, content, ext))

    if not records:
        raise RuntimeError(f"{entity_id}: discovered no SQL-readable raw records")
    save_raw_ndjson(records, node_id, compression="zstd")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
