from __future__ import annotations

import csv
import html
import io
import re

import httpx

from subsets_utils import NodeSpec, save_raw_ndjson

_BASE = "https://genesis.sachsen-anhalt.de/genesis/online"
_SLUG = "statistisches-landesamt-sachsen-anhalt"
_SPEC_PREFIX = _SLUG + "-"

_ENTITY_IDS = [
    "12411-0001",
    "13211-0004",
    "31231-0001",
    "31231-0002",
    "52111-0002",
    "61111-0001",
    "61111-0002",
]


def _entity_from_node_id(node_id: str) -> str:
    if not node_id.startswith(_SPEC_PREFIX):
        raise ValueError(f"unexpected node id: {node_id}")
    return node_id.removeprefix(_SPEC_PREFIX)


def _extract_levelid(html: str) -> str:
    match = re.search(r'name="levelid"\s+value="([^"]+)"', html)
    if not match:
        raise RuntimeError("GENESIS page did not contain a levelid hidden field")
    return match.group(1)


def _extract_ffcsv_action(page_html: str) -> str | None:
    actions = re.findall(r'<form[^>]+action="([^"]+)"', page_html)
    for action in actions:
        action = html.unescape(action)
        if "operation=ergebnistabelleDownload" in action and "option=ffcsv" in action:
            return action
    return None


def _download_ffcsv(table_code: str) -> bytes:
    headers = {"User-Agent": "subsets-connector/1.0"}
    timeout = httpx.Timeout(connect=20.0, read=180.0, write=20.0, pool=20.0)
    with httpx.Client(headers=headers, timeout=timeout, follow_redirects=True) as client:
        setup = client.get(
            _BASE,
            params={"operation": "table", "code": table_code, "bypass": "true"},
        )
        setup.raise_for_status()
        result_html = setup.text
        if _extract_ffcsv_action(result_html) is None and 'name="werteabruf"' not in result_html:
            raise RuntimeError(f"{table_code}: anonymous table setup page is unavailable")

        if _extract_ffcsv_action(result_html) is None:
            levelid = _extract_levelid(result_html)
            result = client.get(
                _BASE,
                params={
                    "operation": "abruftabelleBearbeiten",
                    "levelindex": "0",
                    "levelid": levelid,
                    "auswahloperation": "abruftabelleAuspraegungAuswaehlen",
                    "auswahlverzeichnis": "ordnungsstruktur",
                    "auswahlziel": "werteabruf",
                    "code": table_code,
                    "auswahltext": "",
                    "werteabruf": "starten",
                },
            )
            result.raise_for_status()
            result_html = result.text

        download_action = _extract_ffcsv_action(result_html)
        if download_action is None:
            raise RuntimeError(f"{table_code}: GENESIS result page did not expose FFCSV download form")

        download = client.post(download_action)
        download.raise_for_status()
        disposition = download.headers.get("content-disposition", "")
        if "_flat.csv" not in disposition:
            raise RuntimeError(f"{table_code}: expected FFCSV attachment, got {disposition!r}")
        return download.content


def _parse_ffcsv(table_code: str, content: bytes) -> list[dict]:
    text = content.decode("iso-8859-1")
    reader = csv.DictReader(io.StringIO(text), delimiter=";")
    rows = []
    for row_number, row in enumerate(reader, start=1):
        cleaned = {key: (value if value != "" else None) for key, value in row.items()}
        cleaned["source_table_code"] = table_code
        cleaned["source_row_number"] = row_number
        rows.append(cleaned)
    if not rows:
        raise RuntimeError(f"{table_code}: FFCSV contained no data rows")
    return rows


def fetch_table(node_id: str) -> None:
    table_code = _entity_from_node_id(node_id)
    content = _download_ffcsv(table_code)
    rows = _parse_ffcsv(table_code, content)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{_SLUG}-{entity_id}", fn=fetch_table)
    for entity_id in _ENTITY_IDS
]
