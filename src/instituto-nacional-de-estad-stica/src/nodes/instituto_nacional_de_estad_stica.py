"""Instituto Nacional de Estadistica (Uruguay) CKAN connector.

Mechanism: the national open-data CKAN portal at
https://catalogodatos.gub.uy/api/3. Each accepted entity is one INE CKAN
package. The package resources contain JSON metadata files and CSV data files;
download stores only the CSV data rows, enriched with CKAN package/resource
metadata, as NDJSON so package-specific columns can drift independently.
"""

from __future__ import annotations

import csv
import io

from subsets_utils import NodeSpec, configure_http, get, save_raw_ndjson

from constants import ENTITY_IDS, SPEC_TO_PACKAGE

CKAN_ACTION = "https://catalogodatos.gub.uy/api/3/action"
PREFIX = "instituto-nacional-de-estad-stica-"


def _api(action: str, **params) -> dict:
    resp = get(f"{CKAN_ACTION}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN {action} returned success=false: {payload.get('error')}")
    return payload["result"]


def _decode_csv(content: bytes) -> str:
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return _decode_csv(resp.content)


def _csv_resources(package: dict) -> list[dict]:
    resources = []
    for resource in package.get("resources", []):
        fmt = (resource.get("format") or "").strip().upper()
        url = resource.get("url")
        if fmt == "CSV" and url:
            resources.append(resource)
    return resources


def _rows_from_resource(package_id: str, resource: dict) -> list[dict]:
    text = _fetch_csv(resource["url"])
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for idx, row in enumerate(reader, start=1):
        cleaned = {
            (key or "").lstrip("\ufeff").strip(): (value if value not in ("", None) else None)
            for key, value in row.items()
            if key is not None and str(key).strip()
        }
        cleaned["__source_package_id"] = package_id
        cleaned["__source_resource_id"] = resource.get("id")
        cleaned["__source_resource_name"] = resource.get("name")
        cleaned["__source_resource_url"] = resource.get("url")
        cleaned["__source_row_number"] = idx
        rows.append(cleaned)
    return rows


def fetch_one(node_id: str) -> None:
    configure_http(verify=False)
    package_id = SPEC_TO_PACKAGE.get(node_id)
    if package_id is None:
        raise RuntimeError(f"unknown node id: {node_id}")

    package = _api("package_show", id=package_id)
    resources = _csv_resources(package)
    if not resources:
        raise RuntimeError(f"{package_id}: no CSV resources found")

    rows = []
    for resource in resources:
        rows.extend(_rows_from_resource(package_id, resource))

    if not rows:
        raise RuntimeError(f"{package_id}: CSV resources yielded 0 rows")
    save_raw_ndjson(rows, node_id)
    print(f"{node_id}: wrote {len(rows):,} rows from {len(resources)} CSV resource(s)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
