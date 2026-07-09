"""Data.gov datasets — CKAN package-metadata corpus (one row per dataset).

Stateless full re-pull of the ~402k-package corpus via package_search, paged
start/rows over a stable `metadata_created asc` sort. Each package is flattened
to one SQL-friendly row; duplicates from concurrent edits during the crawl are
removed in the transform (row_number over id).
"""

from subsets_utils import NodeSpec
from utils import _crawl_packages


def _dataset_row(pkg: dict) -> dict:
    org = pkg.get("organization") or {}
    return {
        "id": pkg.get("id"),
        "name": pkg.get("name"),
        "title": pkg.get("title"),
        "notes": pkg.get("notes"),
        "organization": org.get("name") if isinstance(org, dict) else None,
        "owner_org": pkg.get("owner_org"),
        "license_id": pkg.get("license_id"),
        "license_title": pkg.get("license_title"),
        "metadata_created": pkg.get("metadata_created"),
        "metadata_modified": pkg.get("metadata_modified"),
        "num_resources": pkg.get("num_resources"),
        "num_tags": pkg.get("num_tags"),
        "type": pkg.get("type"),
        "state": pkg.get("state"),
        "maintainer": pkg.get("maintainer"),
        "author": pkg.get("author"),
        "version": pkg.get("version"),
        "url": pkg.get("url"),
        "tags": ", ".join(t.get("name", "") for t in (pkg.get("tags") or []) if t.get("name")),
        "groups": ", ".join(g.get("name", "") for g in (pkg.get("groups") or []) if g.get("name")),
    }


def fetch_datasets(node_id: str) -> None:
    _crawl_packages(node_id, lambda pkg: [_dataset_row(pkg)])


DOWNLOAD_SPECS = [
    NodeSpec(id="data-gov-datasets", fn=fetch_datasets, kind="download"),
]
