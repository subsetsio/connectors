"""EU Open Data Portal (data.europa.eu) — EU-institution slice.

Mechanism: piveau hub-search REST API (https://data.europa.eu/api/hub/search).
The connector is scoped to the EU institutions' own open data — the genuine
"EU Open Data Portal" — via the dataset index `country=eu` facet (~48k datasets
across ~113 catalogs: Eurostat, ECB, JRC, EU agencies). The ~1.69M national
datasets mirrored from member-state portals are out of scope.

We redistribute harmonised DCAT-AP *metadata*, not the underlying data files
(those live in heterogeneous, externally-hosted distributions). Two publishable
tables:

  - eu-open-data-portal-datasets : one row per EU-institution dataset (corpus).
  - eu-open-data-portal-catalogs : the EU-institution source-catalog taxonomy.

Fetch shape: stateless full re-pull every run (corpus is small and the source
publishes revisions in place — no watermark to trust). Pagination strategy:
the search index uses page+limit, but Elasticsearch caps the page window at
~10k results and the public gateway WAF-blocks the scroll cursor. So we
partition the corpus by catalog (each EU catalog facet is a bounded window) and
page within it. Only one catalog (zenodo, ~27k) exceeds the 10k window; it is
capped at 10k with a logged warning. Every other catalog paginates to
completion.

No incremental query, no documented/observed rate limit, no whole-corpus bulk
dump (the per-catalog paged stream is the bulk path). No auth.
"""

import json
import logging
import urllib.parse

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
    transient_retry,
)

log = logging.getLogger(__name__)

BASE = "https://data.europa.eu/api/hub/search"
PAGE_SIZE = 1000
MAX_PAGES_PER_CATALOG = 10  # Elasticsearch from+size window cap (~10k results)

CATALOGS_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("title", pa.string()),
    ("publisher", pa.string()),
    ("country", pa.string()),
    ("source_type", pa.string()),
    ("issued", pa.string()),
    ("modified", pa.string()),
    ("dataset_count", pa.int64()),
    ("description", pa.string()),
])


@transient_retry()
def _search(params: dict) -> dict:
    resp = get(f"{BASE}/search", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()["result"]


@transient_retry()
def _catalogue(cid: str) -> dict:
    resp = get(f"{BASE}/catalogues/{urllib.parse.quote(cid)}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    return body.get("result", body) if isinstance(body, dict) else {}


def _en(value, default=None):
    """Pick an English (or any) value from a multilingual dict / scalar."""
    if isinstance(value, dict):
        return value.get("en") or next(iter(value.values()), default)
    return value if value not in (None, "") else default


def _eu_catalog_counts() -> dict:
    """Map of EU-institution catalog id -> dataset count, from the catalog
    sub-facet under the country=eu dataset filter (one request)."""
    # Pass raw JSON — httpx url-encodes params once. Do NOT pre-quote (double
    # encoding makes the server silently ignore the facet and return the whole
    # ~1.7M-row federation instead of the ~48k EU-institution slice).
    facets = json.dumps({"country": ["eu"]})
    res = _search({"filter": "dataset", "facets": facets, "limit": 0})
    items = next((f["items"] for f in res.get("facets", []) if f.get("id") == "catalog"), [])
    counts = {it["id"]: it.get("count", 0) for it in items if it.get("id")}
    if not counts:
        raise RuntimeError("country=eu catalog facet returned no catalogs — API shape changed")
    return counts


def _iter_catalog_datasets(cid: str):
    """Yield raw dataset records for one EU-institution catalog, paging within
    the bounded country=eu + catalog facet window."""
    facets = json.dumps({"country": ["eu"], "catalog": [cid]})
    for page in range(MAX_PAGES_PER_CATALOG):
        res = _search({"filter": "dataset", "facets": facets,
                       "limit": PAGE_SIZE, "page": page})
        rows = res.get("results", [])
        if not rows:
            return
        yield from rows
        if len(rows) < PAGE_SIZE:
            return
    log.warning(
        "catalog %s exceeded %d pages (%d total datasets reported) — capped at %d records",
        cid, MAX_PAGES_PER_CATALOG, res.get("count"), MAX_PAGES_PER_CATALOG * PAGE_SIZE,
    )


def _normalize_dataset(d: dict) -> dict:
    pub = d.get("publisher") or {}
    dists = d.get("distributions") or []
    fmts = []
    for di in dists:
        f = di.get("format")
        fid = f.get("id") if isinstance(f, dict) else f
        if fid and fid not in fmts:
            fmts.append(fid)
    cats = [c.get("id") for c in (d.get("categories") or []) if isinstance(c, dict) and c.get("id")]
    kws = []
    for k in (d.get("keywords") or []):
        kid = k.get("id") if isinstance(k, dict) else k
        if kid and kid not in kws:
            kws.append(kid)
    lp = d.get("landing_page")
    if isinstance(lp, list):
        lp = (lp[0].get("resource") if lp and isinstance(lp[0], dict) else None)
    elif isinstance(lp, dict):
        lp = lp.get("resource")
    rec = d.get("catalog_record") or {}
    return {
        "id": d.get("id"),
        "title": _en(d.get("title")),
        "description": _en(d.get("description")),
        "catalog": (d.get("catalog") or {}).get("id") if isinstance(d.get("catalog"), dict) else d.get("catalog"),
        "country": (d.get("country") or {}).get("id") if isinstance(d.get("country"), dict) else d.get("country"),
        "publisher": pub.get("name") if isinstance(pub, dict) else pub,
        "categories": ",".join(cats),
        "keywords": ",".join(kws),
        "modified": _en(d.get("modified")),
        "issued": rec.get("issued") if isinstance(rec, dict) else None,
        "landing_page": lp,
        "num_distributions": len(dists),
        "distribution_formats": ",".join(fmts),
        "is_hvd": bool(d.get("is_hvd")),
    }


def fetch_datasets(node_id: str) -> None:
    asset = node_id
    counts = _eu_catalog_counts()
    log.info("EU-institution catalogs: %d, datasets reported: %d",
             len(counts), sum(counts.values()))
    rows = []
    seen = set()
    for cid in sorted(counts):
        n = 0
        for d in _iter_catalog_datasets(cid):
            did = d.get("id")
            if not did or did in seen:
                continue
            seen.add(did)
            rows.append(_normalize_dataset(d))
            n += 1
        log.info("catalog %s: %d datasets (reported %d)", cid, n, counts[cid])
    if not rows:
        raise RuntimeError("no EU-institution datasets fetched")
    log.info("total EU-institution datasets fetched: %d", len(rows))
    save_raw_ndjson(rows, asset)


def fetch_catalogs(node_id: str) -> None:
    asset = node_id
    counts = _eu_catalog_counts()
    rows = []
    for cid in sorted(counts):
        rec = _catalogue(cid)
        title = _en(rec.get("title"), cid)
        country = rec.get("country") or {}
        pub = rec.get("publisher") or {}
        rows.append({
            "id": rec.get("id") or cid,
            "title": title,
            "publisher": pub.get("name") if isinstance(pub, dict) else pub,
            "country": country.get("label") if isinstance(country, dict) else country,
            "source_type": rec.get("source_type"),
            "issued": _en(rec.get("issued")),
            "modified": _en(rec.get("modified")),
            "dataset_count": int(counts[cid]),
            "description": _en(rec.get("description")),
        })
    if not rows:
        raise RuntimeError("no EU-institution catalogs fetched")
    table = pa.Table.from_pylist(rows, schema=CATALOGS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="eu-open-data-portal-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="eu-open-data-portal-catalogs", fn=fetch_catalogs, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="eu-open-data-portal-datasets-transform",
        deps=["eu-open-data-portal-datasets"],
        sql='''
            SELECT
                CAST(id AS VARCHAR)                  AS dataset_id,
                CAST(title AS VARCHAR)               AS title,
                CAST(description AS VARCHAR)         AS description,
                CAST(catalog AS VARCHAR)             AS catalog,
                CAST(country AS VARCHAR)             AS country,
                CAST(publisher AS VARCHAR)           AS publisher,
                CAST(categories AS VARCHAR)          AS categories,
                CAST(keywords AS VARCHAR)            AS keywords,
                TRY_CAST(modified AS DATE)           AS modified,
                TRY_CAST(issued AS DATE)             AS issued,
                CAST(landing_page AS VARCHAR)        AS landing_page,
                CAST(num_distributions AS INTEGER)   AS num_distributions,
                CAST(distribution_formats AS VARCHAR) AS distribution_formats,
                CAST(is_hvd AS BOOLEAN)              AS is_hvd
            FROM "eu-open-data-portal-datasets"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY modified DESC NULLS LAST) = 1
        ''',
    ),
    SqlNodeSpec(
        id="eu-open-data-portal-catalogs-transform",
        deps=["eu-open-data-portal-catalogs"],
        sql='''
            SELECT
                CAST(id AS VARCHAR)            AS catalog_id,
                CAST(title AS VARCHAR)         AS title,
                CAST(publisher AS VARCHAR)     AS publisher,
                CAST(country AS VARCHAR)       AS country,
                CAST(source_type AS VARCHAR)   AS source_type,
                TRY_CAST(issued AS DATE)       AS issued,
                TRY_CAST(modified AS DATE)     AS modified,
                CAST(dataset_count AS BIGINT)  AS dataset_count,
                CAST(description AS VARCHAR)   AS description
            FROM "eu-open-data-portal-catalogs"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY modified DESC NULLS LAST) = 1
        ''',
    ),
]
