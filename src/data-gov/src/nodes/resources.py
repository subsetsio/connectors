"""Data.gov resources — file/distribution inventory (one row per resource).

Child of datasets: resources are extracted from the same package payload, so
this node crawls the corpus independently rather than depending on datasets.
Each package's resources[] are flattened to flat rows; duplicates are removed
in the transform (row_number over id).
"""

from utils import RESOURCE_SCHEMA, _crawl_packages, as_int, as_str


def _resource_rows(pkg: dict) -> list[dict]:
    org = pkg.get("organization") or {}
    org_name = org.get("name") if isinstance(org, dict) else None
    rows = []
    for r in pkg.get("resources") or []:
        rows.append({
            "id": as_str(r.get("id")),
            "package_id": as_str(r.get("package_id") or pkg.get("id")),
            "dataset_name": as_str(pkg.get("name")),
            "organization": as_str(org_name),
            "name": as_str(r.get("name")),
            "description": as_str(r.get("description")),
            "format": as_str(r.get("format")),
            "mimetype": as_str(r.get("mimetype")),
            "size": as_int(r.get("size")),
            "created": as_str(r.get("created")),
            "last_modified": as_str(r.get("last_modified")),
            "state": as_str(r.get("state")),
            "resource_type": as_str(r.get("resource_type")),
            "url_type": as_str(r.get("url_type")),
            "url": as_str(r.get("url")),
        })
    return rows


def fetch_resources(node_id: str) -> bool | None:
    return _crawl_packages(node_id, _resource_rows, RESOURCE_SCHEMA)
