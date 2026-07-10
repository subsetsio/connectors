"""Data.gov resources — file/distribution inventory (one row per resource).

Child of datasets: resources are extracted from the same package payload, so
this node crawls the corpus independently rather than depending on datasets.
Each package's resources[] are flattened to flat rows; duplicates are removed
in the transform (row_number over id).
"""

from utils import _crawl_packages


def _resource_rows(pkg: dict) -> list[dict]:
    org = pkg.get("organization") or {}
    org_name = org.get("name") if isinstance(org, dict) else None
    rows = []
    for r in pkg.get("resources") or []:
        rows.append({
            "id": r.get("id"),
            "package_id": r.get("package_id") or pkg.get("id"),
            "dataset_name": pkg.get("name"),
            "organization": org_name,
            "name": r.get("name"),
            "description": r.get("description"),
            "format": r.get("format"),
            "mimetype": r.get("mimetype"),
            "size": r.get("size"),
            "created": r.get("created"),
            "last_modified": r.get("last_modified"),
            "state": r.get("state"),
            "resource_type": r.get("resource_type"),
            "url_type": r.get("url_type"),
            "url": r.get("url"),
        })
    return rows


def fetch_resources(node_id: str) -> bool | None:
    return _crawl_packages(node_id, _resource_rows)
