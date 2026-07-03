"""NuGet connector.

Two published subsets, each built from exactly one download asset (single-dep
transforms — a two-dep SQL transform over R2 trips an s3fs directory-listing
cache bug where resolving the first dep's prefix glob hides the second dep's
files):

- ``package_versions`` — the full version-publication history, harvested from
  the V3 **catalog** (the append-only event log). Every catalog page carries
  ``nuget:id`` / ``nuget:version`` / ``commitTimeStamp`` / ``@type`` inline, so
  the whole ~12M-event corpus is reachable by fetching the ~22,700 pages with
  no per-leaf fetch. One row per (package_id, version) publish event; the
  transform dedups to the latest event per version and drops deletes. This is
  the publication time-series and the complete package-id universe.

- ``packages`` — the most-downloaded packages from the **search** service
  (download-weighted default ranking, up to the ~10k ``skip`` cap). Search is
  the only public source of download counts, and it cannot enumerate the full
  ~505k corpus, so this is the popular head — which holds essentially all
  download volume. One row per package with totals, verification, tags and
  version count.

The catalog harvest is a stateless full re-pull every run (~22.7k immutable
CDN-served pages, fetched concurrently, ~6 min). Raw is not retained across
runs and every run re-executes every spec, so there is no incremental state to
keep; deterministic page-range batch ids overwrite cleanly. The final,
still-growing catalog page is re-pulled every run for free.
"""
import concurrent.futures as cf

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)

CATALOG_INDEX = "https://api.nuget.org/v3/catalog0/index.json"
SEARCH_URL = "https://azuresearch-usnc.nuget.org/query"

PAGES_PER_BATCH = 500
PAGE_FETCH_WORKERS = 32
SEARCH_PAGE_SIZE = 1000
SEARCH_SKIP_CAP = 10000  # Azure Search hard limit; full corpus is not enumerable via search.

VERSIONS_SCHEMA = pa.schema([
    ("package_id", pa.string()),
    ("version", pa.string()),
    ("commit_timestamp", pa.string()),  # ISO-8601; cast in the transform
    ("is_delete", pa.bool_()),
])

PACKAGES_SCHEMA = pa.schema([
    ("package_id", pa.string()),
    ("latest_version", pa.string()),
    ("total_downloads", pa.int64()),
    ("verified", pa.bool_()),
    ("version_count", pa.int64()),
    ("authors", pa.string()),
    ("tags", pa.string()),
])


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_pages(urls):
    rows = []
    with cf.ThreadPoolExecutor(max_workers=PAGE_FETCH_WORKERS) as ex:
        for page in ex.map(_get_json, urls):
            for it in page.get("items", []):
                rows.append({
                    "package_id": it["nuget:id"],
                    "version": it["nuget:version"],
                    "commit_timestamp": it["commitTimeStamp"],
                    "is_delete": it.get("@type") == "nuget:PackageDelete",
                })
    return rows


def fetch_package_versions(node_id: str) -> None:
    """Harvest the full NuGet V3 catalog into batched parquet (stateless full
    re-pull; immutable pages fetched concurrently)."""
    index = _get_json(CATALOG_INDEX)
    page_urls = [it["@id"] for it in index["items"]]
    total = len(page_urls)
    if total == 0:
        raise AssertionError("catalog index returned 0 pages")

    start = 0
    while start < total:
        end = min(start + PAGES_PER_BATCH, total)
        rows = _fetch_pages(page_urls[start:end])
        if not rows:
            raise AssertionError(f"catalog pages [{start}:{end}] yielded 0 items")
        table = pa.Table.from_pylist(rows, schema=VERSIONS_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{start:06d}-{end - 1:06d}")
        start = end


def fetch_packages(node_id: str) -> None:
    """Most-downloaded packages from the search service (the only public source
    of download counts; capped at ~10k by the skip limit)."""
    rows = []
    seen = set()
    for skip in range(0, SEARCH_SKIP_CAP, SEARCH_PAGE_SIZE):
        data = _get_json(
            SEARCH_URL,
            q="",
            skip=skip,
            take=SEARCH_PAGE_SIZE,
            prerelease="true",
            semVerLevel="2.0.0",
        )
        items = data.get("data", [])
        if not items:
            break
        for p in items:
            pid = p["id"]
            key = pid.lower()
            if key in seen:
                continue
            seen.add(key)
            authors = p.get("authors")
            tags = p.get("tags")
            rows.append({
                "package_id": pid,
                "latest_version": p.get("version"),
                "total_downloads": int(p.get("totalDownloads") or 0),
                "verified": bool(p.get("verified")),
                "version_count": len(p.get("versions") or []),
                "authors": ", ".join(authors) if isinstance(authors, list) else (authors or ""),
                "tags": ", ".join(tags) if isinstance(tags, list) else (tags or ""),
            })
    if not rows:
        raise AssertionError("search returned 0 packages")
    table = pa.Table.from_pylist(rows, schema=PACKAGES_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nuget-packages", fn=fetch_packages, kind="download"),
    NodeSpec(id="nuget-package-versions", fn=fetch_package_versions, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nuget-package-versions-transform",
        deps=["nuget-package-versions"],
        sql='''
            WITH ranked AS (
                SELECT
                    package_id,
                    version,
                    commit_timestamp,
                    is_delete,
                    row_number() OVER (
                        PARTITION BY lower(package_id), version
                        ORDER BY commit_timestamp DESC
                    ) AS rn
                FROM "nuget-package-versions"
            )
            SELECT
                package_id,
                version,
                CAST(commit_timestamp AS TIMESTAMP) AS published,
                (version LIKE '%-%') AS is_prerelease
            FROM ranked
            WHERE rn = 1 AND is_delete = FALSE
        ''',
        key=("package_id", "version"),
        temporal="published",
    ),
    SqlNodeSpec(
        id="nuget-packages-transform",
        deps=["nuget-packages"],
        sql='''
            SELECT
                package_id,
                latest_version,
                total_downloads,
                verified,
                version_count,
                authors,
                tags
            FROM "nuget-packages"
            WHERE package_id IS NOT NULL
        ''',
        key=("package_id",),
    ),
]
