import csv
import io
import re

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson


SLUG = "tokyo-metropolitan-government-statistics"
SPEC_PREFIX = f"{SLUG}-"
CKAN_ACTION = "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show"


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
        if str(resource.get("format") or "").upper() == "CSV" and resource.get("url")
    ]
    if not resources:
        raise ValueError(f"{entity_id}: package has no CSV resources")

    records = []
    for resource in sorted(resources, key=lambda r: r.get("position") or 0):
        url = resource["url"]
        csv_resp = get(url, timeout=(10.0, 120.0))
        csv_resp.raise_for_status()
        parsed_rows = _csv_rows(_decode_csv(csv_resp.content))
        for parsed in parsed_rows:
            records.append(
                {
                    "entity_id": entity_id,
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
            )

    if not records:
        raise ValueError(f"{entity_id}: CSV resources produced no data rows")
    save_raw_ndjson(records, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_entity_to_spec_id(entity_id), fn=fetch_one)
    for entity_id in ENTITY_IDS
]
