"""TED procurement notices and companion TED public download inventories."""

from __future__ import annotations

import csv
import io
import re
import tarfile
import xml.etree.ElementTree as ET
from datetime import date, datetime
from urllib.parse import urlparse

from subsets_utils import NodeSpec, get, save_raw_ndjson

CALENDAR_URL = "https://ted.europa.eu/en/release-calendar/-/download/file/CSV/{year}"
CSV_SUBSET_METADATA_URL = "https://data.europa.eu/api/hub/search/datasets/ted-csv?locale=en"
DAILY_PACKAGE_URL = "https://ted.europa.eu/packages/daily/{issue_token}"
SLUG = "ted-eu-procurement"


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


def _first_path(root: ET.Element, *path: str) -> str | None:
    current = [root]
    for wanted in path:
        next_level: list[ET.Element] = []
        for parent in current:
            for child in parent:
                if _local_name(child.tag) == wanted:
                    next_level.append(child)
        current = next_level
        if not current:
            return None
    for elem in current:
        text = " ".join((elem.text or "").split())
        if text:
            return text
    return None


def _texts_with_attr(root: ET.Element, tag_name: str, attr_name: str, attr_value: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for elem in root.iter():
        if _local_name(elem.tag) != tag_name or elem.attrib.get(attr_name) != attr_value:
            continue
        text = " ".join((elem.text or "").split())
        if text and text not in seen:
            values.append(text)
            seen.add(text)
    return values


def _first_with_attr(root: ET.Element, tag_name: str, attr_name: str, attr_value: str) -> str | None:
    values = _texts_with_attr(root, tag_name, attr_name, attr_value)
    return values[0] if values else None


def _joined(root: ET.Element, *tag_names: str) -> str | None:
    values: list[str] = []
    seen: set[str] = set()
    for tag_name in tag_names:
        for value in _texts(root, tag_name):
            if value not in seen:
                values.append(value)
                seen.add(value)
    return " | ".join(values) if values else None


def _joined_with_attr(root: ET.Element, tag_name: str, attr_name: str, attr_value: str) -> str | None:
    values = _texts_with_attr(root, tag_name, attr_name, attr_value)
    return " | ".join(values) if values else None


def _normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = value.removesuffix("Z")
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


def _publication_number_from_filename(filename: str) -> str | None:
    match = re.search(r"(\d{6,8})[_-](\d{4})\.xml$", filename)
    if not match:
        return None
    return _publication_number(f"{match.group(1)}-{match.group(2)}")


def _english_text(value: object) -> str | None:
    if isinstance(value, dict):
        text = value.get("en")
        if isinstance(text, str):
            return text
    if isinstance(value, str):
        return value
    return None


def _first_url(value: object) -> str | None:
    if isinstance(value, list) and value:
        first = value[0]
        return first if isinstance(first, str) else None
    return value if isinstance(value, str) else None


def _year_bounds(text: str | None) -> tuple[int | None, int | None]:
    if not text:
        return None, None
    years = [int(year) for year in re.findall(r"\b(20\d{2}|19\d{2})\b", text)]
    if not years:
        return None, None
    return min(years), max(years)


def _notice_kind(title: str | None) -> str | None:
    if not title:
        return None
    lowered = title.lower()
    if "contract award" in lowered:
        return "contract_award_notice"
    if "contract notice" in lowered:
        return "contract_notice"
    return None


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
    doc_id = (
        root.attrib.get("DOC_ID")
        or _first(root, "NO_DOC_OJS", "NoticePublicationID")
        or _publication_number_from_filename(filename)
    )
    publication_number = _publication_number(doc_id)
    publication_date = _normalize_date(_first(root, "DATE_PUB", "PublicationDate", "RequestedPublicationDate"))
    title = _first(root, "TITLE", "TI_TEXT") or _first_path(root, "ProcurementProject", "Name")
    buyer_names = _joined(root, "OFFICIALNAME") or _joined_with_attr(root, "ID", "schemeName", "organization")
    cpv = _joined(root, "ORIGINAL_CPV", "CPV_CODE") or _joined_with_attr(
        root, "ItemClassificationCode", "listName", "cpv"
    )
    nuts = _joined(root, "PERFORMANCE_NUTS", "CA_CE_NUTS", "TENDERER_NUTS", "NUTS") or _joined_with_attr(
        root, "CountrySubentityCode", "listName", "nuts"
    )
    value_elem = next((elem for elem in root.iter() if _local_name(elem.tag) == "EstimatedOverallContractAmount"), None)
    return {
        "asset_id": node_id,
        "package_issue_number": issue_number,
        "package_issue_token": issue_token,
        "package_publication_date": package_publication_date,
        "xml_filename": filename,
        "publication_number": publication_number,
        "doc_id": doc_id,
        "ojs_reference": _first(root, "NO_DOC_OJS", "GazetteID"),
        "edition": root.attrib.get("EDITION"),
        "schema_version": root.attrib.get("VERSION") or _first(root, "UBLVersionID"),
        "xml_schema": _first(root, "XML_SCHEMA_DEFINITION_LINK", "CustomizationID"),
        "publication_date": publication_date,
        "dispatch_date": _normalize_date(_first(root, "DS_DATE_DISPATCH", "DATE_DISPATCH", "IssueDate")),
        "submission_deadline": _normalize_date(_first(root, "DT_DATE_FOR_SUBMISSION", "EndDate")),
        "country": _first(root, "ISO_COUNTRY", "COUNTRY")
        or _first_with_attr(root, "IdentificationCode", "listName", "country"),
        "document_type": _first(root, "TD_DOCUMENT_TYPE", "NoticeTypeCode"),
        "contract_nature": _first(root, "NC_CONTRACT_NATURE", "TYPE_CONTRACT")
        or _first_with_attr(root, "ProcurementTypeCode", "listName", "contract-nature"),
        "procedure_type": _first(root, "PR_PROC", "ProcedureCode"),
        "regulation": _first(root, "RP_REGULATION", "RegulatoryDomain"),
        "authority_type": _first(root, "AA_AUTHORITY_TYPE", "PartyTypeCode"),
        "main_activity": _first(root, "MA_MAIN_ACTIVITIES", "CA_ACTIVITY", "ActivityTypeCode"),
        "title": title,
        "buyer_names": buyer_names,
        "cpv": cpv,
        "nuts": nuts,
        "value": _first(root, "VALUE", "VAL_TOTAL", "EstimatedOverallContractAmount"),
        "currency": _first(root, "CURRENCY") or (value_elem.attrib.get("currencyID") if value_elem is not None else None),
    }


def fetch_csv_subset(node_id: str) -> None:
    resp = get(CSV_SUBSET_METADATA_URL, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    distributions = data.get("result", {}).get("distributions") or []
    rows: list[dict] = []
    for distribution in distributions:
        title = _english_text(distribution.get("title"))
        url = _first_url(distribution.get("download_url")) or _first_url(distribution.get("access_url"))
        start_year, end_year = _year_bounds(title)
        parsed = urlparse(url or "")
        rows.append(
            {
                "asset_id": node_id,
                "dataset_id": "ted-csv",
                "title": title,
                "format": (distribution.get("format") or {}).get("id"),
                "url": url,
                "filename": parsed.path.rsplit("/", 1)[-1] if parsed.path else None,
                "notice_kind": _notice_kind(title),
                "period_start_year": start_year,
                "period_end_year": end_year,
                "is_deprecated": bool(title and "deprecated" in title.lower()),
                "issued": _normalize_date(distribution.get("issued")),
                "modified": _normalize_date(distribution.get("modified")),
            }
        )
    if not rows:
        raise RuntimeError(f"{node_id}: data.europa.eu returned no TED CSV subset distributions")
    save_raw_ndjson(rows, node_id)


def fetch_release_calendar(node_id: str) -> None:
    current_year = date.today().year
    rows: list[dict] = []
    for year in range(current_year - 1, current_year + 1):
        resp = get(CALENDAR_URL.format(year=year), timeout=60)
        resp.raise_for_status()
        reader = csv.DictReader(io.StringIO(resp.text))
        for row in reader:
            raw_ojs = (row.get("OJS") or row.get("OJS ") or "").strip()
            raw_date = (row.get("Publication date") or row.get("Publication date ") or "").strip()
            if not raw_ojs or not raw_date:
                continue
            publication_date = _normalize_date(raw_date)
            rows.append(
                {
                    "asset_id": node_id,
                    "year": year,
                    "ojs_issue_number": int(raw_ojs),
                    "issue_token": f"{year}{int(raw_ojs):05d}",
                    "publication_date": publication_date,
                }
            )
    if not rows:
        raise RuntimeError(f"{node_id}: release calendar returned no rows")
    save_raw_ndjson(rows, node_id)


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
    NodeSpec(id=f"{SLUG}-csv-subset", fn=fetch_csv_subset, kind="download"),
    NodeSpec(id="ted-eu-procurement-notices", fn=fetch_notices, kind="download"),
    NodeSpec(id=f"{SLUG}-release-calendar", fn=fetch_release_calendar, kind="download"),
]
