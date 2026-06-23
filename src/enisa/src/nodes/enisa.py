"""ENISA — European Union Vulnerability Database (EUVD) connector.

Source: ENISA's NIS2-mandated public vulnerability database, exposed via a
REST search API (https://euvdservices.enisa.europa.eu/api/search). The whole
corpus (~360k vulnerability records as of mid-2026) is reachable only by
paginating that one endpoint: {total, items:[...]}, page-style pagination with
a server-side cap of 100 records/page regardless of the requested size.

Fetch shape: stateless full re-pull (decision shape 1). The corpus is bounded
(~3.6k pages) and re-pullable in one run, so each refresh walks every page and
overwrites — revisions and late corrections are picked up for free. We stream
pages straight to a gzipped NDJSON file (records are nested/drifty: some carry
no CVSS vector, products/vendors are nested arrays), so memory stays flat.

The API orders newest-first and the corpus grows at the front, so a record can
in principle shift across the page we are currently reading mid-crawl. We dedup
by id in the transform (keep the most-recently-updated row) to absorb the
duplicates that overlap produces; a missed record is possible but rare over a
~15-minute crawl of a database that adds tens of entries per day, and the next
refresh re-pulls in full.

Two published subsets, two independent full crawls (download nodes can't share
state): `vulnerabilities` (one row per EUVD id, scalar fields) and
`affected_products` (one row per vulnerability x affected product, exploded
from each record's nested enisaIdProduct array).
"""

import json

from subsets_utils import get, transient_retry, raw_writer

BASE = "https://euvdservices.enisa.europa.eu/api"
PAGE_SIZE = 100
# Safety ceiling: ~3.6k pages today; raise (not silently truncate) if the
# corpus ever blows past ~2x that, which would mean our termination broke.
MAX_PAGES = 8000


@transient_retry()
def _fetch_page(page: int) -> dict:
    resp = get(
        f"{BASE}/search",
        params={
            "fromScore": 0,
            "toScore": 10,
            "fromEpss": 0,
            "toEpss": 100,
            "exploited": "false",
            "page": page,
            "size": PAGE_SIZE,
        },
        headers={"accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _iter_records():
    """Yield every vulnerability record by walking the search endpoint.

    Termination: stop when a page returns no items. `total` (pinned on the
    first response) drives the expected page count and the safety cap.
    """
    first = _fetch_page(0)
    total = int(first.get("total", 0))
    expected_pages = (total // PAGE_SIZE) + 2  # +slack for growth during crawl
    items = first.get("items", [])
    yield from items
    page = 1
    while items:
        if page > MAX_PAGES:
            raise RuntimeError(
                f"EUVD pagination exceeded MAX_PAGES={MAX_PAGES} "
                f"(total reported {total}, expected ~{expected_pages} pages); "
                "termination logic likely broke."
            )
        payload = _fetch_page(page)
        items = payload.get("items", [])
        yield from items
        page += 1


def _vuln_row(rec: dict) -> dict:
    return {
        "id": rec.get("id"),
        "enisa_uuid": rec.get("enisaUuid"),
        "description": rec.get("description"),
        "date_published": rec.get("datePublished"),
        "date_updated": rec.get("dateUpdated"),
        "base_score": rec.get("baseScore"),
        "base_score_version": rec.get("baseScoreVersion") or None,
        "base_score_vector": rec.get("baseScoreVector") or None,
        "epss": rec.get("epss"),
        "assigner": rec.get("assigner") or None,
        "aliases": rec.get("aliases") or None,
        "references": rec.get("references") or None,
        "n_products": len(rec.get("enisaIdProduct") or []),
    }


def fetch_vulnerabilities(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rec in _iter_records():
            fh.write(json.dumps(_vuln_row(rec), ensure_ascii=False) + "\n")


def fetch_affected_products(node_id: str) -> None:
    asset = node_id
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rec in _iter_records():
            euvd_id = rec.get("id")
            for prod in rec.get("enisaIdProduct") or []:
                product = prod.get("product") or {}
                vendor = product.get("vendor") or {}
                row = {
                    "euvd_id": euvd_id,
                    "product_name": product.get("name") or None,
                    "vendor_name": vendor.get("name") or None,
                    "product_version": prod.get("product_version") or None,
                }
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")


from subsets_utils import NodeSpec, SqlNodeSpec  # noqa: E402

DOWNLOAD_SPECS = [
    NodeSpec(id="enisa-vulnerabilities", fn=fetch_vulnerabilities, kind="download"),
    NodeSpec(id="enisa-affected-products", fn=fetch_affected_products, kind="download"),
]

_TS_FMT = "%b %-d, %Y, %-I:%M:%S %p"

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="enisa-vulnerabilities-transform",
        deps=["enisa-vulnerabilities"],
        sql=f'''
            WITH ranked AS (
                SELECT
                    *,
                    row_number() OVER (
                        PARTITION BY id
                        ORDER BY try_strptime(date_updated, '{_TS_FMT}') DESC NULLS LAST
                    ) AS rn
                FROM "enisa-vulnerabilities"
                WHERE id IS NOT NULL
            )
            SELECT
                id,
                enisa_uuid,
                description,
                CAST(try_strptime(date_published, '{_TS_FMT}') AS TIMESTAMP) AS date_published,
                CAST(try_strptime(date_updated,   '{_TS_FMT}') AS TIMESTAMP) AS date_updated,
                CAST(base_score AS DOUBLE)         AS base_score,
                base_score_version,
                base_score_vector,
                CAST(epss AS DOUBLE)               AS epss,
                assigner,
                aliases,
                references,
                CAST(n_products AS INTEGER)        AS n_products
            FROM ranked
            WHERE rn = 1
        ''',
    ),
    SqlNodeSpec(
        id="enisa-affected-products-transform",
        deps=["enisa-affected-products"],
        sql='''
            SELECT DISTINCT
                euvd_id,
                product_name,
                vendor_name,
                product_version
            FROM "enisa-affected-products"
            WHERE euvd_id IS NOT NULL
              AND product_name IS NOT NULL
        ''',
    ),
]
