"""Open Government Canada (open.canada.ca · CKAN 2.10.8) — metadata redistributor.

The federal Open Government portal is a heterogeneous CKAN catalog: ~47k
packages across ~130 publishers, whose underlying files are externally hosted
and wildly mixed (CSV/XLSX tables alongside SHP/GEOJSON/KML map layers, PDFs,
imagery, ESRI REST services). There is no uniform per-package tabular schema, so
the publishable unit is the **harmonized catalog metadata corpus** — the same
shape as the eu-open-data-portal redistributor. Two Delta tables:

  - open-government-canada-datasets       : one row per CKAN package (corpus).
  - open-government-canada-organizations  : the publisher directory (taxonomy),
                                            joinable to datasets via organization.

Mechanism: CKAN action API (no auth). Datasets are enumerated via the
Solr-backed `package_search` action with an `fl` field restriction (keeps each
page small) paged by `rows`+`start`; the per-request latency is throughput-bound
(~0.03s/doc), so pages are fetched concurrently to land a full sweep in a few
minutes. Organizations come from a single `organization_list?all_fields=true`
call. Stateless full re-pull every run — the corpus is small, revisions land in
place, and there is no trustworthy whole-corpus watermark.
"""

import logging
from concurrent.futures import ThreadPoolExecutor

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

log = logging.getLogger(__name__)

ACTION = "https://open.canada.ca/data/api/3/action"
PAGE_SIZE = 500
WORKERS = 8
# Solr stored fields kept per package (verbatim catalog facts).
FL = "id,name,title,organization,metadata_created,metadata_modified,license_id,res_format,subject,keywords,notes,portal_release_date"
MAX_PAGES_ABS = 400  # safety ceiling: ~200k packages; raises if the portal blows past it


def _clean_text(s):
    if not s:
        return None
    s = " ".join(str(s).replace("\r", " ").replace("\n", " ").replace("#", "").split())
    return s[:2000] if s else None


@transient_retry()
def _action(path, params):
    resp = get(f"{ACTION}/{path}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN action {path} returned success=false")
    return body["result"]


def _normalize_dataset(rec):
    fmts = sorted({(f or "").upper() for f in (rec.get("res_format") or []) if f})
    res_list = rec.get("res_format") or []
    return {
        "dataset_id": rec.get("id"),
        "name": rec.get("name"),
        "title": rec.get("title"),
        "organization": rec.get("organization"),
        "subjects": ", ".join(rec.get("subject") or []) or None,
        "keywords": ", ".join((rec.get("keywords") or [])[:40]) or None,
        "license_id": rec.get("license_id"),
        "resource_formats": ", ".join(fmts) or None,
        "num_resources": len(res_list),
        "notes": _clean_text(rec.get("notes")),
        "metadata_created": rec.get("metadata_created"),
        "metadata_modified": rec.get("metadata_modified"),
        "portal_release_date": rec.get("portal_release_date"),
    }


def _fetch_page(start):
    res = _action(
        "package_search",
        {"rows": PAGE_SIZE, "start": start, "q": "*:*", "sort": "metadata_created asc", "fl": FL},
    )
    return res["results"]


def fetch_datasets(node_id: str) -> None:
    asset = node_id
    first = _action(
        "package_search",
        {"rows": PAGE_SIZE, "start": 0, "q": "*:*", "sort": "metadata_created asc", "fl": FL},
    )
    count = first["count"]
    if count <= 0:
        raise RuntimeError("package_search reported 0 datasets — API shape changed")

    starts = list(range(PAGE_SIZE, count + 1, PAGE_SIZE))
    if len(starts) + 1 > MAX_PAGES_ABS:
        raise RuntimeError(
            f"portal reports {count} packages → {len(starts) + 1} pages exceeds "
            f"MAX_PAGES_ABS={MAX_PAGES_ABS}; raise the ceiling deliberately"
        )

    pages = [first["results"]]
    if starts:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            pages.extend(ex.map(_fetch_page, starts))

    rows = {}
    for page in pages:
        for rec in page:
            pid = rec.get("id")
            if pid:
                rows[pid] = _normalize_dataset(rec)
    if not rows:
        raise RuntimeError("no dataset records collected")
    log.info("open-government-canada datasets: %d packages (reported %d)", len(rows), count)
    save_raw_ndjson(list(rows.values()), asset)


def fetch_organizations(node_id: str) -> None:
    asset = node_id
    orgs = _action("organization_list", {"all_fields": "true"})
    if not isinstance(orgs, list) or not orgs:
        raise RuntimeError("organization_list returned no organizations")
    rows = []
    for o in orgs:
        rows.append({
            "org_id": o.get("id"),
            "name": o.get("name"),
            "title": _clean_text(o.get("title")),
            "package_count": o.get("package_count"),
            "state": o.get("state"),
            "type": o.get("type"),
            "created": o.get("created"),
        })
    log.info("open-government-canada organizations: %d", len(rows))
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="open-government-canada-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="open-government-canada-organizations", fn=fetch_organizations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="open-government-canada-datasets-transform",
        deps=["open-government-canada-datasets"],
        sql='''
            SELECT
                CAST(dataset_id AS VARCHAR)              AS dataset_id,
                CAST(name AS VARCHAR)                    AS name,
                CAST(title AS VARCHAR)                   AS title,
                CAST(organization AS VARCHAR)            AS organization,
                CAST(subjects AS VARCHAR)                AS subjects,
                CAST(keywords AS VARCHAR)                AS keywords,
                CAST(license_id AS VARCHAR)              AS license_id,
                CAST(resource_formats AS VARCHAR)        AS resource_formats,
                CAST(num_resources AS INTEGER)           AS num_resources,
                CAST(notes AS VARCHAR)                   AS notes,
                TRY_CAST(metadata_created AS TIMESTAMP)  AS metadata_created,
                TRY_CAST(metadata_modified AS TIMESTAMP) AS metadata_modified,
                TRY_CAST(portal_release_date AS DATE)    AS portal_release_date
            FROM "open-government-canada-datasets"
            WHERE dataset_id IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY dataset_id ORDER BY metadata_modified DESC NULLS LAST
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="open-government-canada-organizations-transform",
        deps=["open-government-canada-organizations"],
        sql='''
            SELECT
                CAST(org_id AS VARCHAR)        AS org_id,
                CAST(name AS VARCHAR)          AS name,
                CAST(title AS VARCHAR)         AS title,
                CAST(package_count AS INTEGER) AS package_count,
                CAST(state AS VARCHAR)         AS state,
                CAST(type AS VARCHAR)          AS type,
                TRY_CAST(created AS TIMESTAMP) AS created
            FROM "open-government-canada-organizations"
            WHERE org_id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY org_id ORDER BY package_count DESC NULLS LAST) = 1
        ''',
    ),
]
