"""Statistics Mauritius CKAN package downloader.

The source data lives on the public Mauritius OpenData CKAN portal. Each
accepted collect entity is a heterogeneous CKAN package, so each download node
fetches the package's uploaded CSV resources and writes one NDJSON raw asset.
Rows are kept close to source shape and stamped with resource/package metadata;
the transform stage can then type each package explicitly from observed raw.
"""
from __future__ import annotations

import csv
import io

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_ndjson,
)

SLUG = "statistics-mauritius"
CKAN_ACTION = "https://data.govmu.org/api/3/action"


def _entity_id_from_node(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _package_show(entity_id: str) -> dict:
    response = get(
        f"{CKAN_ACTION}/package_show",
        params={"id": entity_id},
        timeout=(10.0, 120.0),
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {entity_id}: {payload!r}")
    return payload["result"]


def _decode_csv(content: bytes, resource_name: str) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", content, 0, 1, f"could not decode {resource_name}")


def _csv_rows(content: bytes, resource: dict) -> list[dict]:
    text = _decode_csv(content, resource.get("name") or resource.get("id") or "resource")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    if not reader.fieldnames:
        return []

    rows = []
    for row_number, row in enumerate(reader, start=1):
        cleaned = {
            (key or f"unnamed_{idx}").strip(): value
            for idx, (key, value) in enumerate(row.items(), start=1)
        }
        cleaned["__row_number"] = row_number
        rows.append(cleaned)
    return rows


def _csv_resources(package: dict) -> list[dict]:
    resources = [
        resource
        for resource in package.get("resources") or []
        if str(resource.get("format") or "").upper() == "CSV" and resource.get("url")
    ]
    resources.sort(key=lambda r: (r.get("position") if r.get("position") is not None else 9999, r.get("name") or ""))
    return resources


def fetch_package(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    package = _package_show(entity_id)
    resources = _csv_resources(package)
    if not resources:
        raise RuntimeError(f"{entity_id}: no CSV resources found in CKAN package")

    out_rows: list[dict] = []
    for resource in resources:
        response = get(resource["url"], timeout=(10.0, 180.0))
        response.raise_for_status()
        rows = _csv_rows(response.content, resource)
        for row in rows:
            row["__package_id"] = package.get("id")
            row["__package_name"] = package.get("name")
            row["__package_title"] = package.get("title")
            row["__package_metadata_modified"] = package.get("metadata_modified")
            row["__resource_id"] = resource.get("id")
            row["__resource_name"] = resource.get("name")
            row["__resource_format"] = resource.get("format")
            row["__resource_last_modified"] = resource.get("last_modified")
        out_rows.extend(rows)

    if not out_rows:
        raise RuntimeError(f"{entity_id}: CSV resources produced zero rows")

    save_raw_ndjson(out_rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_package, kind="download")
    for entity_id in ENTITY_IDS
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"{SLUG}-{entity_id}",
        description=(
            "Refresh at least monthly; no published machine-readable cadence found, "
            "so this uses a 30-day raw age check against the CKAN package mirror."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=30),
    )
    for entity_id in ENTITY_IDS
]
