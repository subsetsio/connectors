import csv
import json
import io
import re
import zipfile
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd

from constants import ENTITY_IDS, PACKAGE_INDEX_SHA256
from subsets_utils import MaintainSpec, NodeSpec, get, post, raw_asset_exists, save_raw_ndjson


SLUG = "tokyo-metropolitan-government-statistics"
SPEC_PREFIX = f"{SLUG}-"
CKAN_ACTION = "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show"
API_SPEC_SEARCH = "https://spec.api.metro.tokyo.lg.jp/spec/search"
API_BASE = "https://service.api.metro.tokyo.lg.jp"
PACKAGE_INDEX_PATH = Path(__file__).resolve().parents[1] / "package_index.json"
_PACKAGE_INDEX = None


def _entity_to_spec_id(entity_id: str) -> str:
    return f"{SPEC_PREFIX}{entity_id.lower().replace('_', '-')}"


def _package_index() -> dict:
    global _PACKAGE_INDEX
    if _PACKAGE_INDEX is None:
        _ = PACKAGE_INDEX_SHA256
        _PACKAGE_INDEX = json.loads(PACKAGE_INDEX_PATH.read_text())
    return _PACKAGE_INDEX


def _decode_csv(content: bytes) -> str:
    for encoding in ("utf-8-sig", "cp932", "shift_jis", "euc_jp"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _clean_key(value: str | None, fallback: str) -> str:
    value = (value or "").strip()
    if value:
        return value
    return fallback


def _unique_headers(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    unique = []
    for header in headers:
        count = seen.get(header, 0) + 1
        seen[header] = count
        unique.append(header if count == 1 else f"{header}_{count}")
    return unique


def _csv_rows(text: str) -> list[dict]:
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(text), dialect)
    rows = list(reader)
    if not rows:
        return []

    header_index = 0
    for index, row in enumerate(rows[:20]):
        nonempty = [cell for cell in row if str(cell).strip()]
        if len(nonempty) >= 2:
            header_index = index
            break

    headers = _unique_headers([
        _clean_key(cell, f"column_{i + 1}")
        for i, cell in enumerate(rows[header_index])
    ])
    parsed = []
    for row_number, row in enumerate(rows[header_index + 1 :], start=1):
        if not any(str(cell).strip() for cell in row):
            continue
        values = {}
        for index, header in enumerate(headers):
            values[header] = row[index] if index < len(row) else None
        if len(row) > len(headers):
            for index, value in enumerate(row[len(headers) :], start=len(headers) + 1):
                values[f"extra_column_{index}"] = value
        parsed.append({"row_number": row_number, "values": values})
    return parsed


def _json_cell(value):
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def _excel_records(package: dict, resource: dict, url: str, content: bytes) -> list[dict]:
    fmt = _resource_format(resource)
    lower_url = url.lower().split("#", 1)[0]
    is_xlsx = lower_url.endswith(".xlsx") or content.startswith(b"PK\x03\x04")
    engine = "openpyxl" if is_xlsx or fmt == "XLSX" else "xlrd"
    workbook = pd.read_excel(
        io.BytesIO(content),
        sheet_name=None,
        header=None,
        dtype=object,
        engine=engine,
    )
    records = []
    row_number = 1
    for sheet_name, frame in workbook.items():
        frame = frame.dropna(how="all").dropna(how="all", axis=1)
        if frame.empty:
            continue
        for _, row in frame.iterrows():
            values = {
                f"column_{index + 1}": _json_cell(value)
                for index, value in enumerate(row.tolist())
                if not pd.isna(value)
            }
            if not values:
                continue
            records.append(
                {
                    "entity_id": package.get("name"),
                    "package_id": package.get("id"),
                    "package_name": package.get("name"),
                    "package_title": package.get("title"),
                    "resource_id": resource.get("id"),
                    "resource_name": resource.get("name"),
                    "resource_position": resource.get("position"),
                    "resource_url_basename": re.sub(r"[^A-Za-z0-9_.-]+", "_", url.rsplit("/", 1)[-1]),
                    "sheet_name": str(sheet_name),
                    "row_number": row_number,
                    "values": values,
                }
            )
            row_number += 1
    return records


def _resource_format(resource: dict) -> str:
    return str(resource.get("format") or "").strip().upper()


def _record_from_row(package: dict, resource: dict, url: str, parsed: dict) -> dict:
    return {
        "entity_id": package.get("name"),
        "package_id": package.get("id"),
        "package_name": package.get("name"),
        "package_title": package.get("title"),
        "resource_id": resource.get("id"),
        "resource_name": resource.get("name"),
        "resource_position": resource.get("position"),
        "resource_url_basename": re.sub(r"[^A-Za-z0-9_.-]+", "_", url.rsplit("/", 1)[-1]),
        "row_number": parsed["row_number"],
        "values": parsed["values"],
    }


def _csv_records(package: dict, resource: dict, url: str, content: bytes) -> list[dict]:
    return [
        _record_from_row(package, resource, url, parsed)
        for parsed in _csv_rows(_decode_csv(content))
    ]


def _zip_records(package: dict, resource: dict, url: str, content: bytes) -> list[dict]:
    records = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for member in sorted(archive.namelist()):
            if member.endswith("/"):
                continue
            member_url = f"{url}#{member}"
            with archive.open(member) as file:
                member_content = file.read()
            if member.lower().endswith(".csv"):
                member_records = _csv_records(package, resource, member_url, member_content)
            elif member.lower().endswith((".xls", ".xlsx")):
                member_resource = dict(resource)
                member_resource["format"] = "XLSX" if member.lower().endswith(".xlsx") else "XLS"
                member_records = _excel_records(package, member_resource, member_url, member_content)
            else:
                continue
            for record in member_records:
                record["archive_member"] = member
                records.append(record)
    return records


def _api_paths_for_resource(package: dict, resource: dict) -> list[str]:
    title = " ".join(
        part for part in (package.get("title"), resource.get("name")) if part
    )
    if not title:
        return []
    resp = get(API_SPEC_SEARCH, params={"keyword": title}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    escaped_entity = re.escape(str(package.get("name") or ""))
    paths = re.findall(rf'href="(/spec/{escaped_entity}[^"]+)"', resp.text)
    return sorted(set(unescape(path) for path in paths))


def _api_records(package: dict, resource: dict) -> list[dict]:
    records = []
    for spec_path in _api_paths_for_resource(package, resource):
        spec_resp = get(urljoin("https://spec.api.metro.tokyo.lg.jp", spec_path), timeout=(10.0, 60.0))
        spec_resp.raise_for_status()
        api_paths = re.findall(r'"(/api/[^"]+/json)"', spec_resp.text)
        for api_path in sorted(set(unescape(path) for path in api_paths)):
            offset = 0
            row_number = 1
            while True:
                api_resp = post(
                    urljoin(API_BASE, api_path),
                    params={"limit": 1000, "offset": offset},
                    json={},
                    timeout=(10.0, 120.0),
                )
                api_resp.raise_for_status()
                payload = api_resp.json()
                hits = payload.get("hits") or []
                metadata = payload.get("metadata") or {}
                for hit in hits:
                    values = dict(hit)
                    values.pop("row", None)
                    records.append(
                        {
                            "entity_id": package.get("name"),
                            "package_id": package.get("id"),
                            "package_name": package.get("name"),
                            "package_title": package.get("title"),
                            "resource_id": resource.get("id"),
                            "resource_name": resource.get("name") or metadata.get("dataTitle"),
                            "resource_position": resource.get("position"),
                            "resource_url_basename": re.sub(r"[^A-Za-z0-9_.-]+", "_", api_path.rsplit("/", 2)[-2]),
                            "row_number": row_number,
                            "values": values,
                            "api_path": api_path,
                        }
                    )
                    row_number += 1
                offset += len(hits)
                total = int(payload.get("total") or 0)
                if not hits or offset >= total:
                    break
    return records


def fetch_one(node_id: str) -> None:
    if not node_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected node id: {node_id}")
    entity_id = node_id.removeprefix(SPEC_PREFIX)

    package = _package_index().get(entity_id)
    if package is None:
        package_resp = get(CKAN_ACTION, params={"id": entity_id}, timeout=(10.0, 60.0))
        package_resp.raise_for_status()
        package = package_resp.json()["result"]
    resources = [
        resource
        for resource in package.get("resources", [])
        if _resource_format(resource) in {"CSV", "ZIP", "XLS", "XLSX"} and resource.get("url")
    ]
    if not resources:
        raise ValueError(f"{entity_id}: package has no CSV, ZIP, XLS, or XLSX resources")

    records = []
    errors = []
    for resource in sorted(resources, key=lambda r: r.get("position") or 0):
        url = resource["url"]
        try:
            resource_resp = get(url, timeout=(10.0, 120.0))
            resource_resp.raise_for_status()
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            continue

        fmt = _resource_format(resource)
        if fmt == "ZIP":
            records.extend(_zip_records(package, resource, url, resource_resp.content))
        elif fmt in {"XLS", "XLSX"}:
            records.extend(_excel_records(package, resource, url, resource_resp.content))
        else:
            records.extend(_csv_records(package, resource, url, resource_resp.content))

    if not records:
        for resource in sorted(resources, key=lambda r: r.get("position") or 0):
            try:
                records.extend(_api_records(package, resource))
            except Exception as exc:
                errors.append(f"{resource.get('name')}: API fallback failed: {exc}")

    if not records:
        detail = "; ".join(errors[:5])
        raise ValueError(f"{entity_id}: resources produced no data rows; {detail}")
    save_raw_ndjson(records, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_entity_to_spec_id(entity_id), fn=fetch_one)
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Weekly refresh per Tokyo Metropolitan Government statistics maintenance "
            "policy; raw assets younger than 7 days are treated as fresh."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
