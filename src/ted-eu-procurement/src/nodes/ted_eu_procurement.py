"""TED procurement notices from the latest OJ S daily XML package."""

from __future__ import annotations

import csv
import io
import tarfile
import xml.etree.ElementTree as ET
from datetime import date, datetime

from subsets_utils import NodeSpec, get, save_raw_ndjson

CALENDAR_URL = "https://ted.europa.eu/en/release-calendar/-/download/file/CSV/{year}"
DAILY_PACKAGE_URL = "https://ted.europa.eu/packages/daily/{issue_token}"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _texts(root: ET.Element, tag_name: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for elem in root.iter():
        if _local_name(elem.tag) != tag_name:
            continue
        text = " ".join((elem.text or "").split())
        if text and text not in seen:
            values.append(text)
            seen.add(text)
    return values


def _first(root: ET.Element, *tag_names: str) -> str | None:
    for tag_name in tag_names:
        values = _texts(root, tag_name)
        if values:
            return values[0]
    return None


def _joined(root: ET.Element, *tag_names: str) -> str | None:
    values: list[str] = []
    seen: set[str] = set()
    for tag_name in tag_names:
        for value in _texts(root, tag_name):
            if value not in seen:
                values.append(value)
                seen.add(value)
    return " | ".join(values) if values else None


def _normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y%m%d", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value[:10], fmt).date().isoformat()
        except ValueError:
            pass
    return value


def _publication_number(doc_id: str | None) -> str | None:
    if not doc_id:
        return None
    if "-" not in doc_id:
        return doc_id
    left, right = doc_id.split("-", 1)
    return f"{int(left)}-{right}" if left.isdigit() else doc_id


def _latest_issue() -> tuple[int, str, str]:
    today = date.today()
    for year in (today.year, today.year - 1):
        resp = get(CALENDAR_URL.format(year=year), timeout=60)
        resp.raise_for_status()
        rows = csv.DictReader(io.StringIO(resp.text))
        candidates: list[tuple[date, int]] = []
        for row in rows:
            raw_ojs = (row.get("OJS") or row.get("OJS ") or "").strip()
            raw_date = (row.get("Publication date") or row.get("Publication date ") or "").strip()
            if not raw_ojs or not raw_date:
                continue
            published = datetime.strptime(raw_date, "%d/%m/%Y").date()
            if published <= today:
                candidates.append((published, int(raw_ojs)))
        if candidates:
            published, ojs = max(candidates)
            return ojs, f"{year}{ojs:05d}", published.isoformat()
    raise RuntimeError("No TED release-calendar issue found for current or prior year")


def _notice_row(
    node_id: str,
    root: ET.Element,
    filename: str,
    issue_number: int,
    issue_token: str,
    package_publication_date: str,
) -> dict:
    doc_id = root.attrib.get("DOC_ID") or _first(root, "NO_DOC_OJS")
    return {
        "asset_id": node_id,
        "package_issue_number": issue_number,
        "package_issue_token": issue_token,
        "package_publication_date": package_publication_date,
        "xml_filename": filename,
        "publication_number": _publication_number(doc_id),
        "doc_id": doc_id,
        "ojs_reference": _first(root, "NO_DOC_OJS"),
        "edition": root.attrib.get("EDITION"),
        "schema_version": root.attrib.get("VERSION"),
        "xml_schema": _first(root, "XML_SCHEMA_DEFINITION_LINK"),
        "publication_date": _normalize_date(_first(root, "DATE_PUB")),
        "dispatch_date": _normalize_date(_first(root, "DS_DATE_DISPATCH", "DATE_DISPATCH")),
        "submission_deadline": _normalize_date(_first(root, "DT_DATE_FOR_SUBMISSION")),
        "country": _first(root, "ISO_COUNTRY", "COUNTRY"),
        "document_type": _first(root, "TD_DOCUMENT_TYPE"),
        "contract_nature": _first(root, "NC_CONTRACT_NATURE", "TYPE_CONTRACT"),
        "procedure_type": _first(root, "PR_PROC"),
        "regulation": _first(root, "RP_REGULATION"),
        "authority_type": _first(root, "AA_AUTHORITY_TYPE"),
        "main_activity": _first(root, "MA_MAIN_ACTIVITIES", "CA_ACTIVITY"),
        "title": _first(root, "TITLE", "TI_TEXT"),
        "buyer_names": _joined(root, "OFFICIALNAME"),
        "cpv": _joined(root, "ORIGINAL_CPV", "CPV_CODE"),
        "nuts": _joined(root, "PERFORMANCE_NUTS", "CA_CE_NUTS", "TENDERER_NUTS", "NUTS"),
        "value": _first(root, "VALUE", "VAL_TOTAL"),
        "currency": _first(root, "CURRENCY"),
    }


def fetch_notices(node_id: str) -> None:
    issue_number, issue_token, package_publication_date = _latest_issue()
    package_url = DAILY_PACKAGE_URL.format(issue_token=issue_token)
    resp = get(package_url, timeout=(10.0, 300.0))
    resp.raise_for_status()

    rows: list[dict] = []
    with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as archive:
        for member in archive:
            if not member.isfile() or not member.name.lower().endswith(".xml"):
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            content = extracted.read()
            root = ET.fromstring(content)
            rows.append(
                _notice_row(
                    node_id,
                    root,
                    member.name,
                    issue_number,
                    issue_token,
                    package_publication_date,
                )
            )

    if not rows:
        raise RuntimeError(f"{node_id}: daily package {issue_token} contained no XML notices")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ted-eu-procurement-notices", fn=fetch_notices, kind="download"),
]
