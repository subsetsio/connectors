import csv
import io
import re
import zipfile
from html import unescape
from urllib.parse import urljoin

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, post, save_raw_ndjson


SLUG = "tokyo-metropolitan-government-statistics"
SPEC_PREFIX = f"{SLUG}-"
CKAN_ACTION = "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show"
API_SPEC_SEARCH = "https://spec.api.metro.tokyo.lg.jp/spec/search"
API_BASE = "https://service.api.metro.tokyo.lg.jp"


def _entity_to_spec_id(entity_id: str) -> str:
    return f"{SPEC_PREFIX}{entity_id.lower().replace('_', '-')}"


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

    headers = [
        _clean_key(cell, f"column_{i + 1}")
        for i, cell in enumerate(rows[header_index])
    ]
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
            if member.endswith("/") or not member.lower().endswith(".csv"):
                continue
            member_url = f"{url}#{member}"
            with archive.open(member) as file:
                for record in _csv_records(package, resource, member_url, file.read()):
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

    package_resp = get(CKAN_ACTION, params={"id": entity_id}, timeout=(10.0, 60.0))
    package_resp.raise_for_status()
    package = package_resp.json()["result"]
    resources = [
        resource
        for resource in package.get("resources", [])
        if _resource_format(resource) in {"CSV", "ZIP"} and resource.get("url")
    ]
    if not resources:
        raise ValueError(f"{entity_id}: package has no CSV or ZIP resources")

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

        if _resource_format(resource) == "ZIP":
            records.extend(_zip_records(package, resource, url, resource_resp.content))
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
