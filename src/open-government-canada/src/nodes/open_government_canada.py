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

Mechanism / sources:
  - datasets: the portal's full-catalogue bulk dump
    (https://open.canada.ca/static/od-do-canada.jsonl.gz) — one gzipped JSONL of
    every package with COMPLETE records. We use this rather than the `package_search`
    action because the Solr index drops the bilingual `fluent` fields: ~28% of
    packages come back with null `title`/`notes` via package_search, but the dump
    carries `title_translated`/`notes_translated` for all of them. The dump is
    ~70MB and the server's keep-alive is flaky on a single long GET, so we pull it
    in retryable HTTP Range chunks and decompress in-process.
  - organizations: a single `organization_list?all_fields=true` action call.

Stateless full re-pull every run — the corpus is small, revisions land in place,
and there is no trustworthy whole-corpus watermark.
"""

import gzip
import io
import json
import logging

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

log = logging.getLogger(__name__)

ACTION = "https://open.canada.ca/data/api/3/action"
DUMP_URL = "https://open.canada.ca/static/od-do-canada.jsonl.gz"
CHUNK = 8 * 1024 * 1024  # 8 MiB Range chunks
MAX_BYTES_ABS = 600 * 1024 * 1024  # safety ceiling on dump size


def _en(value):
    """Pick the English (or any) value from a fluent multilingual dict / scalar."""
    if isinstance(value, dict):
        return value.get("en") or next((v for v in value.values() if v), None)
    return value


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


@transient_retry()
def _range(lo, hi):
    resp = get(DUMP_URL, headers={"Range": f"bytes={lo}-{hi}"}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    if resp.status_code != 206:
        raise RuntimeError(f"expected 206 partial content for Range, got {resp.status_code}")
    return resp


def _download_dump() -> bytes:
    first = _range(0, CHUNK - 1)
    content_range = first.headers.get("content-range", "")
    try:
        total = int(content_range.split("/")[-1])
    except ValueError:
        raise RuntimeError(f"could not parse total size from content-range {content_range!r}")
    if total <= 0 or total > MAX_BYTES_ABS:
        raise RuntimeError(f"dump size {total} bytes outside sane bounds (max {MAX_BYTES_ABS})")

    chunks = [first.content]
    lo = len(first.content)
    while lo < total:
        hi = min(lo + CHUNK - 1, total - 1)
        chunks.append(_range(lo, hi).content)
        lo = hi + 1
    raw = b"".join(chunks)
    if len(raw) != total:
        raise RuntimeError(f"downloaded {len(raw)} bytes != expected {total}")
    return raw


def _normalize_dataset(rec):
    org = rec.get("organization") or {}
    org_name = org.get("name") if isinstance(org, dict) else org
    resources = rec.get("resources") or []
    fmts = sorted({(r.get("format") or "").upper() for r in resources if r.get("format")})
    kw = rec.get("keywords")
    if isinstance(kw, dict):
        kw = _en(kw)
    kw = kw if isinstance(kw, list) else ([] if kw in (None, "") else [kw])
    title = _en(rec.get("title_translated")) or rec.get("title")
    notes = _en(rec.get("notes_translated")) or rec.get("notes")
    return {
        "dataset_id": rec.get("id"),
        "name": rec.get("name"),
        "title": _clean_text(title),
        "organization": org_name,
        "subjects": ", ".join(rec.get("subject") or []) or None,
        "keywords": ", ".join(str(k) for k in kw[:40]) or None,
        "license_id": rec.get("license_id"),
        "resource_formats": ", ".join(fmts) or None,
        "num_resources": len(resources),
        "notes": _clean_text(notes),
        "metadata_created": rec.get("metadata_created"),
        "metadata_modified": rec.get("metadata_modified"),
        "portal_release_date": rec.get("portal_release_date"),
    }


def fetch_datasets(node_id: str) -> None:
    asset = node_id
    raw = _download_dump()
    rows = {}
    bad = 0
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as gz:
        for line in gz:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            pid = rec.get("id")
            if pid:
                rows[pid] = _normalize_dataset(rec)
    if bad:
        log.warning("open-government-canada datasets: skipped %d unparseable lines", bad)
    if len(rows) < 30000:
        raise RuntimeError(f"only {len(rows)} packages parsed from dump — expected ~47k")
    log.info("open-government-canada datasets: %d packages from bulk dump", len(rows))
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
