import csv
import io

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson


CKAN_ACTION = "https://ckan.publishing.service.gov.uk/api/3/action"
SLUG = "uk-datagov"


def _package_name_from_spec_id(spec_id: str) -> str:
    entity_id = spec_id.removeprefix(f"{SLUG}-")
    return entity_id.rsplit("--", 1)[0]


def _package_show(package_name: str) -> dict:
    resp = get(
        f"{CKAN_ACTION}/package_show",
        params={"id": package_name},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {package_name}: {data!r}")
    return data["result"]


def _pick_csv_resource(package: dict) -> dict:
    resources = package.get("resources") or []
    for resource in resources:
        fmt = str(resource.get("format") or "").lower()
        name = str(resource.get("name") or "").lower()
        url = str(resource.get("url") or "")
        if "csv" in fmt or name == "csv" or "/CSV/" in url:
            return resource
    raise RuntimeError(f"no CSV resource found for {package.get('name')}")


def _read_csv_rows(content: bytes) -> list[dict]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row_number, row in enumerate(reader, start=1):
        rows.append({"source_row_number": row_number, **row})
    return rows


def fetch_one(spec_id: str) -> None:
    package_name = _package_name_from_spec_id(spec_id)
    package = _package_show(package_name)
    resource = _pick_csv_resource(package)
    url = resource["url"]

    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    rows = _read_csv_rows(resp.content)
    if not rows:
        raise RuntimeError(f"{spec_id}: CSV resource returned no rows")

    enriched = []
    for row in rows:
        enriched.append(
            {
                "package_name": package.get("name"),
                "package_title": package.get("title"),
                "resource_id": resource.get("id"),
                "resource_name": resource.get("name"),
                "resource_format": resource.get("format"),
                "resource_url": url,
                **row,
            }
        )
    save_raw_ndjson(enriched, spec_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one)
    for entity_id in ENTITY_IDS
]
