from __future__ import annotations

import csv
import hashlib
import io
import re
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pandas as pd
from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, record_source_signature, save_raw_ndjson

SLUG = "washington-ofm"
PREFIX = f"{SLUG}-"
OFM_START = "https://ofm.wa.gov/data-research/"
SOCRATA_ENDPOINT = "https://data.wa.gov/resource/{dataset_id}.json"
FILE_EXTENSIONS = (".xlsx", ".xls", ".csv", ".zip", ".json", ".xml", ".sas7bdat")
OFM_HEADERS = {
    "User-Agent": "DataIntegrations/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


SPEC_TO_ENTITY = {_spec_id(entity_id): entity_id for entity_id in ENTITY_IDS}


def _entity_from_spec_id(spec_id: str) -> str:
    try:
        return SPEC_TO_ENTITY[spec_id]
    except KeyError as exc:
        raise ValueError(f"unknown Washington OFM spec id: {spec_id}") from exc


def _html_links(url: str) -> list[str]:
    parser = LinkParser()
    parser.feed(_ofm_get_text(url))
    return [urljoin(url, href).split("#", 1)[0] for href in parser.links]


def _ofm_get_bytes(url: str, timeout: float = 240.0) -> tuple[bytes, str]:
    request_url = quote(url, safe=":/?#[]@!$&'()*+,;=%")
    request = Request(request_url, headers=OFM_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read(), response.url
    except HTTPError as exc:
        raise RuntimeError(f"OFM request failed with HTTP {exc.code} for {request_url}") from exc


def _ofm_get_text(url: str) -> str:
    content, _final_url = _ofm_get_bytes(url, timeout=60.0)
    return content.decode("utf-8", "replace")


def _walk_ofm_links() -> list[str]:
    seen: set[str] = set()
    queue = [OFM_START]
    file_links: set[str] = set()

    for _depth in range(3):
        next_queue: set[str] = set()
        for page_url in queue:
            if page_url in seen:
                continue
            seen.add(page_url)
            for full_url in _html_links(page_url):
                parsed = urlparse(full_url)
                path_lower = parsed.path.lower()
                if parsed.netloc != "ofm.wa.gov":
                    continue
                if path_lower.endswith(FILE_EXTENSIONS) or (
                    "/wp-content/uploads/" in path_lower
                    and any(ext in path_lower for ext in FILE_EXTENSIONS)
                ):
                    file_links.add(full_url)
                    continue
                if parsed.path.startswith("/data-research/") and full_url not in seen:
                    next_queue.add(full_url)
        queue = sorted(next_queue)[:250]

    return sorted(file_links)


def _ofm_file_url(entity_id: str) -> str:
    expected_prefix = entity_id.rsplit("-", 1)[-1]
    matches = [
        url
        for url in _walk_ofm_links()
        if hashlib.sha1(url.encode("utf-8")).hexdigest().startswith(expected_prefix)
    ]
    if len(matches) != 1:
        raise ValueError(f"{entity_id}: expected one OFM file URL match, found {len(matches)}")
    return matches[0]


def _source_file(url: str) -> str:
    return urlparse(url).path.rsplit("/", 1)[-1]


def _base_row(entity_id: str, source_url: str, source_file: str, source_member: str | None) -> dict:
    return {
        "_entity_id": entity_id,
        "_source_type": "ofm_file",
        "_source_url": source_url,
        "_source_file": source_file,
        "_source_member": source_member,
    }


def _cell_rows_from_frame(
    frame: pd.DataFrame,
    *,
    entity_id: str,
    source_url: str,
    source_file: str,
    source_member: str | None,
    sheet_name: str | None,
) -> list[dict]:
    rows: list[dict] = []
    base = _base_row(entity_id, source_url, source_file, source_member)
    for row_idx, values in enumerate(frame.itertuples(index=False, name=None), start=1):
        for col_idx, value in enumerate(values, start=1):
            if pd.isna(value):
                continue
            value_text = str(value).strip()
            if value_text == "":
                continue
            rows.append(
                {
                    **base,
                    "sheet_name": sheet_name,
                    "row_index": row_idx,
                    "column_index": col_idx,
                    "value_text": value_text,
                }
            )
    return rows


def _rows_from_excel(
    content: bytes,
    *,
    entity_id: str,
    source_url: str,
    source_file: str,
    source_member: str | None = None,
) -> list[dict]:
    rows: list[dict] = []
    workbook = pd.read_excel(
        io.BytesIO(content),
        sheet_name=None,
        header=None,
        dtype=str,
        keep_default_na=False,
    )
    for sheet_name, frame in workbook.items():
        rows.extend(
            _cell_rows_from_frame(
                frame,
                entity_id=entity_id,
                source_url=source_url,
                source_file=source_file,
                source_member=source_member,
                sheet_name=str(sheet_name),
            )
        )
    return rows


def _rows_from_csv(
    content: bytes,
    *,
    entity_id: str,
    source_url: str,
    source_file: str,
    source_member: str | None = None,
) -> list[dict]:
    text = content.decode("utf-8-sig", "replace")
    reader = csv.reader(io.StringIO(text))
    base = _base_row(entity_id, source_url, source_file, source_member)
    rows = []
    for row_idx, values in enumerate(reader, start=1):
        for col_idx, value in enumerate(values, start=1):
            value_text = str(value).strip()
            if value_text:
                rows.append(
                    {
                        **base,
                        "sheet_name": None,
                        "row_index": row_idx,
                        "column_index": col_idx,
                        "value_text": value_text,
                    }
                )
    return rows


def _rows_from_json_or_xml(
    content: bytes,
    *,
    entity_id: str,
    source_url: str,
    source_file: str,
    source_member: str | None = None,
) -> list[dict]:
    text = content.decode("utf-8", "replace")
    rows = []
    for row_idx, line in enumerate(text.splitlines(), start=1):
        value_text = line.strip()
        if not value_text:
            continue
        rows.append(
            {
                **_base_row(entity_id, source_url, source_file, source_member),
                "sheet_name": None,
                "row_index": row_idx,
                "column_index": 1,
                "value_text": value_text,
            }
        )
    return rows


def _rows_from_member(
    content: bytes,
    member_name: str,
    *,
    entity_id: str,
    source_url: str,
    source_file: str,
) -> list[dict]:
    lower = member_name.lower()
    if lower.endswith((".xlsx", ".xls")):
        return _rows_from_excel(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
            source_member=member_name,
        )
    if lower.endswith((".csv", ".txt")):
        return _rows_from_csv(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
            source_member=member_name,
        )
    if lower.endswith((".json", ".xml")):
        return _rows_from_json_or_xml(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
            source_member=member_name,
        )
    return []


def _rows_from_file(content: bytes, *, entity_id: str, source_url: str) -> list[dict]:
    source_file = _source_file(source_url)
    lower = source_file.lower()
    if lower.endswith((".xlsx", ".xls")):
        return _rows_from_excel(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
        )
    if lower.endswith((".csv", ".txt")):
        return _rows_from_csv(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
        )
    if lower.endswith((".json", ".xml")):
        return _rows_from_json_or_xml(
            content,
            entity_id=entity_id,
            source_url=source_url,
            source_file=source_file,
        )
    if lower.endswith(".zip"):
        rows: list[dict] = []
        with ZipFile(io.BytesIO(content)) as archive:
            for member in archive.namelist():
                if member.endswith("/"):
                    continue
                rows.extend(
                    _rows_from_member(
                        archive.read(member),
                        member,
                        entity_id=entity_id,
                        source_url=source_url,
                        source_file=source_file,
                    )
                )
        return rows
    raise ValueError(f"{entity_id}: unsupported OFM file type: {source_file}")


def _fetch_ofm_file(spec_id: str, entity_id: str) -> None:
    url = _ofm_file_url(entity_id)
    content, final_url = _ofm_get_bytes(url)
    rows = _rows_from_file(content, entity_id=entity_id, source_url=final_url)
    if not rows:
        raise ValueError(f"{entity_id}: no tabular cells parsed from {url}")
    save_raw_ndjson(rows, spec_id)


def _fetch_socrata(spec_id: str, entity_id: str) -> None:
    dataset_id = entity_id.removeprefix("socrata-")
    rows: list[dict] = []
    offset = 0
    limit = 50_000
    while True:
        response = get(
            SOCRATA_ENDPOINT.format(dataset_id=dataset_id),
            params={"$limit": limit, "$offset": offset},
            timeout=(10.0, 240.0),
        )
        response.raise_for_status()
        batch = response.json()
        if not isinstance(batch, list):
            raise ValueError(f"{entity_id}: expected Socrata JSON list, got {type(batch).__name__}")
        if not batch:
            break
        for record in batch:
            if isinstance(record, dict):
                rows.append(
                    {
                        "_entity_id": entity_id,
                        "_source_type": "socrata",
                        "_socrata_dataset_id": dataset_id,
                        **record,
                    }
                )
        if len(batch) < limit:
            break
        offset += limit

    if not rows:
        raise ValueError(f"{entity_id}: Socrata dataset returned no rows")
    save_raw_ndjson(rows, spec_id)
    record_source_signature(spec_id, SOCRATA_ENDPOINT.format(dataset_id=dataset_id))


def fetch_one(spec_id: str) -> None:
    entity_id = _entity_from_spec_id(spec_id)
    if entity_id.startswith("socrata-"):
        _fetch_socrata(spec_id, entity_id)
    else:
        _fetch_ofm_file(spec_id, entity_id)


DOWNLOAD_SPECS = [NodeSpec(id=_spec_id(entity_id), fn=fetch_one) for entity_id in ENTITY_IDS]
