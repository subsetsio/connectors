"""Data.gov datasets — CKAN package-metadata corpus (one row per dataset).

Stateless full re-pull of the ~402k-package corpus via package_search, paged
start/rows over a stable `metadata_created asc` sort. Each package is flattened
to one SQL-friendly row; duplicates from concurrent edits during the crawl are
removed in the transform (row_number over id).
"""

from subsets_utils import NodeSpec, SqlNodeSpec
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


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="data-gov-datasets-transform",
        deps=["data-gov-datasets"],
        sql='''
            SELECT
                id,
                name,
                title,
                notes AS description,
                organization,
                owner_org,
                license_id,
                license_title,
                TRY_CAST(metadata_created AS TIMESTAMP)  AS metadata_created,
                TRY_CAST(metadata_modified AS TIMESTAMP) AS metadata_modified,
                TRY_CAST(num_resources AS INTEGER)       AS num_resources,
                TRY_CAST(num_tags AS INTEGER)            AS num_tags,
                type,
                state,
                maintainer,
                author,
                version,
                url,
                tags,
                groups
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY id ORDER BY metadata_modified DESC
                ) AS rn
                FROM "data-gov-datasets"
            )
            WHERE rn = 1 AND id IS NOT NULL
        ''',
    ),
]
