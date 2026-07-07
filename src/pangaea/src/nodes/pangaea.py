from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from xml.etree import ElementTree as ET

from constants import ENTITY_IDS, ENTITY_TO_SET
from subsets_utils import NodeSpec, get, save_raw_ndjson


OAI_ENDPOINT = "https://ws.pangaea.de/oai/provider"
DOI_BASE = "https://doi.pangaea.de"
OAI_NS = {"o": "http://www.openarchives.org/OAI/2.0/"}


def _entity_from_node_id(node_id: str) -> str:
    prefix = "pangaea-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    wanted = node_id[len(prefix) :].replace("-", "").lower()
    for entity_id in ENTITY_IDS:
        if entity_id.replace("_", "").lower() == wanted:
            return entity_id
    raise KeyError(f"no entity configured for node id {node_id!r}")


def _list_source_dois(set_spec: str) -> list[str]:
    params = {"verb": "ListIdentifiers", "metadataPrefix": "datacite4", "set": set_spec}
    dois: list[str] = []

    while True:
        resp = get(OAI_ENDPOINT, params=params, timeout=(10.0, 120.0))
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        for header in root.findall(".//o:header", OAI_NS):
            if header.get("status") == "deleted":
                continue
            identifier = header.findtext("o:identifier", namespaces=OAI_NS) or ""
            marker = "oai:pangaea.de:doi:"
            if identifier.startswith(marker):
                dois.append(identifier[len(marker) :])

        token = (
            root.findtext(".//o:ListIdentifiers/o:resumptionToken", namespaces=OAI_NS)
            or ""
        ).strip()
        if not token:
            break
        params = {"verb": "ListIdentifiers", "resumptionToken": token}

    return sorted(set(dois))


def _linkset_items(doi: str) -> list[dict]:
    url = f"{DOI_BASE}/{doi}?format=linkset_json"
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    for linkset in data.get("linkset", []):
        if linkset.get("anchor") == f"{DOI_BASE}/{doi}":
            return linkset.get("item", [])
    return []


def _download_item(href: str) -> bytes:
    resp = get(href, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _decode_tab(content: bytes) -> str:
    for encoding in ("utf-8-sig", "ISO-8859-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _dataset_doi_from_text(text: str, fallback: str) -> str:
    match = re.search(r"https://doi\.org/(10\.1594/PANGAEA\.\d+)", text)
    return match.group(1) if match else fallback


def _parse_tab_rows(
    *,
    collection: str,
    source_doi: str,
    filename: str,
    content: bytes,
) -> list[dict]:
    text = _decode_tab(content)
    dataset_doi = _dataset_doi_from_text(text, source_doi)
    lines = text.splitlines()
    metadata_lines: list[str] = []
    data_start = 0

    if lines and lines[0].startswith("/*"):
        for idx, line in enumerate(lines):
            metadata_lines.append(line)
            if line.strip() == "*/":
                data_start = idx + 1
                break

    while data_start < len(lines) and not lines[data_start].strip():
        data_start += 1
    if data_start >= len(lines):
        return []

    reader = csv.reader(lines[data_start:], delimiter="\t")
    try:
        columns = next(reader)
    except StopIteration:
        return []

    metadata_text = "\n".join(metadata_lines)
    rows: list[dict] = []
    for source_row_number, values in enumerate(reader, start=1):
        if not values or not any(value.strip() for value in values):
            continue
        for pos, column_name in enumerate(columns):
            value = values[pos] if pos < len(values) else None
            rows.append(
                {
                    "record_type": "cell",
                    "collection": collection,
                    "source_doi": source_doi,
                    "dataset_doi": dataset_doi,
                    "file_name": filename,
                    "source_row_number": source_row_number,
                    "column_position": pos + 1,
                    "column_name": column_name,
                    "value": value,
                    "metadata_text": metadata_text,
                }
            )
    return rows


def _extract_tab_payloads(content: bytes, href: str) -> list[tuple[str, bytes]]:
    if zipfile.is_zipfile(io.BytesIO(content)):
        payloads: list[tuple[str, bytes]] = []
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for name in archive.namelist():
                if name.lower().endswith(".tab") and not name.endswith("/"):
                    payloads.append((name, archive.read(name)))
        return payloads

    filename = href.rsplit("/", 1)[-1].split("?", 1)[0] or "dataset.tab"
    return [(filename, content)]


def fetch_one(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    set_spec = ENTITY_TO_SET[entity_id]
    source_dois = _list_source_dois(set_spec)
    rows: list[dict] = []
    seen_datasets: set[tuple[str, str]] = set()

    for source_doi in source_dois:
        rows.append(
            {
                "record_type": "source",
                "collection": entity_id,
                "source_doi": source_doi,
                "dataset_doi": None,
                "file_name": None,
                "source_row_number": None,
                "column_position": None,
                "column_name": None,
                "value": None,
                "metadata_text": None,
            }
        )
        for item in _linkset_items(source_doi):
            href = item.get("href", "")
            item_type = item.get("type", "")
            if item_type not in {"application/zip", "text/tab-separated-values"}:
                continue
            content = _download_item(href)
            for filename, payload in _extract_tab_payloads(content, href):
                parsed = _parse_tab_rows(
                    collection=entity_id,
                    source_doi=source_doi,
                    filename=filename,
                    content=payload,
                )
                if not parsed:
                    continue
                dataset_key = (parsed[0]["dataset_doi"], filename)
                if dataset_key in seen_datasets:
                    continue
                seen_datasets.add(dataset_key)
                rows.extend(parsed)

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="pangaea-glacierlengthsaustria", fn=fetch_one),
]
