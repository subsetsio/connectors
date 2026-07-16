"""Data.gov datasets — CKAN package-metadata corpus (one row per dataset).

Stateless full re-pull of the ~402k-package corpus via package_search, paged
start/rows over a stable `metadata_created asc` sort. Each package is flattened
to one SQL-friendly row; duplicates from concurrent edits during the crawl are
removed in the transform (row_number over id).
"""

from utils import DATASET_SCHEMA, _crawl_packages, as_int, as_str


def _dataset_row(pkg: dict) -> dict:
    org = pkg.get("organization") or {}
    return {
        "id": as_str(pkg.get("id")),
        "name": as_str(pkg.get("name")),
        "title": as_str(pkg.get("title")),
        "notes": as_str(pkg.get("notes")),
        "organization": as_str(org.get("name")) if isinstance(org, dict) else None,
        "owner_org": as_str(pkg.get("owner_org")),
        "license_id": as_str(pkg.get("license_id")),
        "license_title": as_str(pkg.get("license_title")),
        "metadata_created": as_str(pkg.get("metadata_created")),
        "metadata_modified": as_str(pkg.get("metadata_modified")),
        "num_resources": as_int(pkg.get("num_resources")),
        "num_tags": as_int(pkg.get("num_tags")),
        "type": as_str(pkg.get("type")),
        "state": as_str(pkg.get("state")),
        "maintainer": as_str(pkg.get("maintainer")),
        "author": as_str(pkg.get("author")),
        "version": as_str(pkg.get("version")),
        "url": as_str(pkg.get("url")),
        "tags": ", ".join(t.get("name", "") for t in (pkg.get("tags") or []) if t.get("name")),
        "groups": ", ".join(g.get("name", "") for g in (pkg.get("groups") or []) if g.get("name")),
    }


def fetch_datasets(node_id: str) -> bool | None:
    return _crawl_packages(node_id, lambda pkg: [_dataset_row(pkg)], DATASET_SCHEMA)
