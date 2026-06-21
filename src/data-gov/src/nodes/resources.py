"""Data.gov resources — file/distribution inventory (one row per resource).

Child of datasets: resources are extracted from the same package payload, so
this node crawls the corpus independently rather than depending on datasets.
Each package's resources[] are flattened to flat rows; duplicates are removed
in the transform (row_number over id).
"""

from subsets_utils import NodeSpec, SqlNodeSpec
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


def fetch_resources(node_id: str) -> None:
    _crawl_packages(node_id, _resource_rows)


DOWNLOAD_SPECS = [
    NodeSpec(id="data-gov-resources", fn=fetch_resources, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="data-gov-resources-transform",
        deps=["data-gov-resources"],
        sql='''
            SELECT
                id,
                package_id,
                dataset_name,
                organization,
                name,
                description,
                format,
                mimetype,
                TRY_CAST(size AS BIGINT)            AS size_bytes,
                TRY_CAST(created AS TIMESTAMP)       AS created,
                TRY_CAST(last_modified AS TIMESTAMP) AS last_modified,
                state,
                resource_type,
                url_type,
                url
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY id ORDER BY created DESC
                ) AS rn
                FROM "data-gov-resources"
            )
            WHERE rn = 1 AND id IS NOT NULL
        ''',
    ),
]
