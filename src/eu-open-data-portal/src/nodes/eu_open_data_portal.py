"""EU Open Data Portal (data.europa.eu) — DCAT-AP catalog metadata.

data.europa.eu is a metadata *redistributor*: the piveau hub-search REST API
harmonises DCAT-AP dataset descriptions from ~210 federated catalogs into one
schema. The full federation holds ~1.8M datasets, but the overwhelming majority
is national data mirrored from member-state portals. This connector is scoped to
the `country=eu` slice — the EU institutions' own open data (Eurostat, JRC, EEA,
Zenodo, the DGs; ~48k datasets across ~112 catalogs), which is what "EU Open Data
Portal" names.

We redistribute the harmonised *metadata*, not the underlying tables: each
dataset's data lives in externally-hosted distributions of heterogeneous format.
The EU has waived copyright on portal metadata via CC0 1.0.

Three assets, one per accepted collect entity:

  datasets    one row per EU-institution dataset (the corpus)
  catalogs    the source-provider taxonomy (joins datasets.catalog_id)
  categories  the DCAT-AP data-theme taxonomy (joins datasets.categories)

Two properties of the API drive the code below.

1. Deep paging silently truncates. `/search?page=N&limit=1000` returns HTTP 200
   with an EMPTY `results` list once the offset passes 10,000 (Elasticsearch's
   `max_result_window`), while still reporting `count: 47699`. A page loop that
   stops on a short page would ship 10k of 48k rows and report success. We use
   the scroll API instead (`scroll=true` -> `/search/scroll?scrollId=...`), which
   is snapshot-consistent, and assert the drained id count against the `count`
   the first response declared.

2. Records are enormous and mostly translation. Every label is carried in up to
   27 languages, so the mean raw record is ~30KB and the untouched corpus is
   ~1.4GB, of which the English content is a few percent. We normalise in the
   fetch fn: scalars promoted to typed columns, labels resolved to English
   (falling back to whatever language exists), nested code lists reduced to their
   authority ids. Upstream fields are sparse — only ~62% of datasets carry a
   `title` at all — so nearly every column is nullable by design.

No incremental query: the API exposes no `since`/`modifiedAfter` filter, so every
run re-scrolls the full EU slice. That is ~50 requests and a couple of minutes.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://data.europa.eu/api/hub/search"

# The EU-institution slice. `country` here is the portal's own provenance facet
# ("EU institutions"), not a geography of what the data describes.
EU_FACETS = '{"country":["eu"]}'

PAGE_SIZE = 1000  # the server rejects limit>1000 with HTTP 400
# Safety ceiling: ~48 pages are expected. This trips only if the corpus grows 4x
# or the scroll cursor stops advancing. It raises; it never returns quietly.
MAX_SCROLL_PAGES = 200

DATASET_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("resource", pa.string()),
    ("title", pa.string()),
    ("title_language", pa.string()),
    ("description", pa.string()),
    ("catalog_id", pa.string()),
    ("catalog_title", pa.string()),
    ("catalog_source_type", pa.string()),
    ("country_id", pa.string()),
    ("publisher_name", pa.string()),
    ("publisher_resource", pa.string()),
    ("issued", pa.timestamp("s")),
    ("modified", pa.timestamp("s")),
    ("catalog_record_issued", pa.timestamp("s")),
    ("catalog_record_modified", pa.timestamp("s")),
    ("temporal_start", pa.timestamp("s")),
    ("temporal_end", pa.timestamp("s")),
    ("categories", pa.list_(pa.string())),
    ("keywords", pa.list_(pa.string())),
    ("languages", pa.list_(pa.string())),
    ("access_right", pa.string()),
    ("accrual_periodicity", pa.string()),
    ("version_info", pa.string()),
    ("landing_page", pa.string()),
    ("is_hvd", pa.bool_()),
    ("quality_score", pa.int32()),
    ("distribution_count", pa.int32()),
    ("distribution_formats", pa.list_(pa.string())),
    ("distribution_licenses", pa.list_(pa.string())),
    ("distribution_byte_size", pa.int64()),
])

CATALOG_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("source_type", pa.string()),
    ("country_id", pa.string()),
    ("publisher_name", pa.string()),
    ("publisher_resource", pa.string()),
    ("issued", pa.timestamp("s")),
    ("modified", pa.timestamp("s")),
    ("dataset_count", pa.int32()),
])

CATEGORY_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("resource", pa.string()),
    ("label", pa.string()),
    ("in_scheme", pa.string()),
])


# --- normalisation ---------------------------------------------------------

def _label(value, prefer: str = "en") -> tuple[str | None, str | None]:
    """Resolve a multilingual label dict to (text, language).

    Upstream carries the same string in up to 27 languages. Prefer English;
    otherwise take the first non-empty language, so a record published only in
    its native language still gets a title rather than a null.
    """
    if not isinstance(value, dict) or not value:
        return None, None
    text = value.get(prefer)
    if text:
        return text, prefer
    for lang, text in value.items():
        if text:
            return text, lang
    return None, None


def _text(value, prefer: str = "en") -> str | None:
    """English text out of either a multilingual dict or an already-plain string."""
    if isinstance(value, str):
        return value or None
    return _label(value, prefer)[0]


def _ts(value) -> datetime | None:
    """Parse an ISO-8601 instant to naive UTC; None when unusable.

    Dates are self-reported by 200-odd publishers and are not validated
    upstream, so a malformed one must not sink the whole scroll page.
    """
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _ids(items) -> list[str]:
    """Authority ids from a list of code records, order preserved, deduped."""
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for item in items:
        code = item.get("id") if isinstance(item, dict) else None
        if code and code not in out:
            out.append(code)
    return out


def _first_resource(items) -> str | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get("resource"):
            return item["resource"]
    return None


def _normalize_dataset(rec: dict) -> dict:
    title, title_language = _label(rec.get("title"))
    catalog = rec.get("catalog") or {}
    publisher = rec.get("publisher") or {}
    # quality_meas is explicitly null on ~3% of records, not merely absent.
    quality = rec.get("quality_meas") or {}
    temporal = (rec.get("temporal") or [{}])[0]
    dists = rec.get("distributions") or []

    formats: list[str] = []
    licenses: list[str] = []
    for dist in dists:
        for key, sink in (("format", formats), ("license", licenses)):
            value = dist.get(key)
            code = value.get("id") if isinstance(value, dict) else None
            if code and code not in sink:
                sink.append(code)
    sizes = [d["byte_size"] for d in dists if isinstance(d.get("byte_size"), int)]

    return {
        "id": rec["id"],
        "resource": rec.get("resource"),
        "title": title,
        "title_language": title_language,
        "description": _text(rec.get("description")),
        "catalog_id": catalog.get("id"),
        "catalog_title": _text(catalog.get("title")),
        "catalog_source_type": catalog.get("source_type"),
        "country_id": (rec.get("country") or {}).get("id"),
        "publisher_name": publisher.get("name"),
        "publisher_resource": publisher.get("resource"),
        "issued": _ts(rec.get("issued")),
        "modified": _ts(rec.get("modified")),
        "catalog_record_issued": _ts((rec.get("catalog_record") or {}).get("issued")),
        "catalog_record_modified": _ts((rec.get("catalog_record") or {}).get("modified")),
        "temporal_start": _ts(temporal.get("gte")),
        "temporal_end": _ts(temporal.get("lte")),
        "categories": _ids(rec.get("categories")),
        "keywords": _ids(rec.get("keywords")),
        "languages": _ids(rec.get("language")),
        "access_right": _text((rec.get("access_right") or {}).get("label")),
        "accrual_periodicity": _text((rec.get("accrual_periodicity") or {}).get("label")),
        "version_info": rec.get("version_info"),
        "landing_page": _first_resource(rec.get("landing_page")),
        "is_hvd": rec.get("is_hvd"),
        "quality_score": quality.get("scoring"),
        "distribution_count": len(dists),
        "distribution_formats": formats,
        "distribution_licenses": licenses,
        "distribution_byte_size": sum(sizes) if sizes else None,
    }


@transient_retry()
def _get_json(url: str, **params) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


# --- fetch fns -------------------------------------------------------------

def fetch_datasets(node_id: str) -> None:
    """Scroll the whole EU slice, normalising each page into one parquet file.

    Deliberately not page+limit: past offset 10,000 the paged endpoint returns
    200 with an empty result list rather than an error, which is indistinguishable
    from a completed crawl.
    """
    asset = node_id

    first = _get_json(
        f"{BASE}/search",
        filter="dataset", facets=EU_FACETS, limit=PAGE_SIZE, scroll="true",
    )["result"]
    expected = first["count"]
    scroll_id = first["scrollId"]
    print(f"  scroll opened: {expected} datasets declared")

    seen: set[str] = set()
    page = first["results"]
    with raw_parquet_writer(asset, DATASET_SCHEMA) as writer:
        for page_no in range(MAX_SCROLL_PAGES):
            if not page:
                break
            rows = [_normalize_dataset(r) for r in page if r.get("id") not in seen]
            seen.update(row["id"] for row in rows)
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=DATASET_SCHEMA))
            print(f"  page {page_no}: +{len(rows)} rows ({len(seen)}/{expected})")

            nxt = _get_json(f"{BASE}/scroll", scrollId=scroll_id)["result"]
            scroll_id = nxt.get("scrollId", scroll_id)
            page = nxt.get("results") or []

    if page:
        raise RuntimeError(
            f"{asset}: scroll did not drain within {MAX_SCROLL_PAGES} pages "
            f"({len(seen)}/{expected} fetched) - corpus grew or cursor stalled"
        )

    # "The run succeeded" and "we got everything" are different claims. The scroll
    # is snapshot-consistent, so anything short of `count` is silent partial loss.
    if len(seen) < expected:
        raise RuntimeError(
            f"{asset}: scroll drained {len(seen)} of {expected} declared datasets"
        )
    print(f"  drained {len(seen)} datasets")


def _eu_catalog_ids() -> list[str]:
    """Catalog ids holding EU-institution datasets, from the live search facet.

    /catalogues lists all ~210 federated catalogs including purely national ones;
    the facet on an EU-filtered search names exactly the catalogs `datasets`
    joins against.
    """
    facets = _get_json(
        f"{BASE}/search", filter="dataset", facets=EU_FACETS, limit=0,
    )["result"]["facets"]
    return [
        item["id"]
        for facet in facets if facet.get("id") == "catalog"
        for item in facet.get("items", []) if item.get("id")
    ]


def fetch_catalogs(node_id: str) -> None:
    """The EU-institution source catalogs, one detail request each."""
    asset = node_id

    catalog_ids = _eu_catalog_ids()
    if not catalog_ids:
        raise RuntimeError(f"{asset}: catalog facet is empty - the EU filter changed shape")
    print(f"  {len(catalog_ids)} EU-institution catalogs")

    rows = []
    for cid in catalog_ids:
        body = _get_json(f"{BASE}/catalogues/{cid}")
        rec = body.get("result", body)
        publisher = rec.get("publisher") or {}
        rows.append({
            "id": rec.get("id") or cid,
            "title": _text(rec.get("title")),
            "description": _text(rec.get("description")),
            "source_type": rec.get("source_type"),
            "country_id": (rec.get("country") or {}).get("id"),
            "publisher_name": publisher.get("name"),
            "publisher_resource": publisher.get("resource"),
            "issued": _ts(rec.get("issued")),
            "modified": _ts(rec.get("modified")),
            "dataset_count": rec.get("count"),
        })

    save_raw_parquet(pa.Table.from_pylist(rows, schema=CATALOG_SCHEMA), asset)


def fetch_categories(node_id: str) -> None:
    """The 14-term DCAT-AP data-theme vocabulary that `datasets.categories` cites."""
    asset = node_id

    items = _get_json(f"{BASE}/vocabularies/data-theme")["result"]["results"]
    rows = [
        {
            "id": item["id"],
            "resource": item.get("resource"),
            "label": _text(item.get("pref_label")),
            "in_scheme": item.get("in_scheme"),
        }
        for item in items
    ]
    if not rows:
        raise RuntimeError(f"{asset}: data-theme vocabulary returned no terms")

    save_raw_parquet(pa.Table.from_pylist(rows, schema=CATEGORY_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="eu-open-data-portal-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="eu-open-data-portal-catalogs", fn=fetch_catalogs, kind="download"),
    NodeSpec(id="eu-open-data-portal-categories", fn=fetch_categories, kind="download"),
]
