"""NuGet connector.

Two published subsets:

- ``package_versions`` — the full version-publication history, harvested from
  the V3 **catalog** (the append-only event log). Every catalog page carries
  ``nuget:id`` / ``nuget:version`` / ``commitTimeStamp`` / ``@type`` inline, so
  the whole ~12M-event corpus is reachable by fetching the ~22,700 pages, with
  no per-leaf fetch. One row per (package_id, version) publish event; the
  transform dedups to the latest event per version and drops deletes. This is
  the authoritative complete package-id universe and the publication
  time-series.

- ``packages`` — a per-package aggregate over the full catalog universe
  (~505k packages: version_count + first/last publish date) LEFT JOINed to
  download/popularity stats from the **search** service. Download counts are
  only exposed by search, which hard-caps ``skip`` at ~10,000, so
  ``total_downloads`` / ``verified`` / ``tags`` are populated for the
  most-downloaded ~10k packages (which hold essentially all download volume)
  and null for the long tail.

Catalog harvest is a firehose: batched by catalog-page-position range, state
watermark = pages permanently completed, fetched concurrently (immutable
CDN-served JSON). The final, still-growing catalog page is always reprocessed;
duplicate version events that result are dedup'd in the transform.
"""
import concurrent.futures as cf

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

STATE_VERSION = 1

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
    """Harvest the full NuGet V3 catalog into batched parquet (firehose)."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "pages_done": 0}

    index = _get_json(CATALOG_INDEX)
    page_urls = [it["@id"] for it in index["items"]]
    total = len(page_urls)
    if total == 0:
        raise AssertionError("catalog index returned 0 pages")

    start = state.get("pages_done", 0)
    while start < total:
        # Loop until the catalog is drained; no self-imposed time/record cap.
        end = min(start + PAGES_PER_BATCH, total)
        rows = _fetch_pages(page_urls[start:end])
        if not rows:
            raise AssertionError(f"catalog pages [{start}:{end}] yielded 0 items")
        table = pa.Table.from_pylist(rows, schema=VERSIONS_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{start:06d}-{end - 1:06d}")
        start = end
        # Write raw before state; never permanently advance past the last
        # (still-growing) page — it is reprocessed every run.
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "pages_done": min(end, total - 1),
        })


def fetch_packages(node_id: str) -> None:
    """Most-downloaded packages from the search service (download-weighted
    default ranking, up to the ~10k skip cap). Only public source of download
    counts."""
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


_VERSIONS_RANKED = '''
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
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nuget-package-versions-transform",
        deps=["nuget-package-versions"],
        sql=f'''
            WITH ranked AS ({_VERSIONS_RANKED})
            SELECT
                package_id,
                version,
                CAST(commit_timestamp AS TIMESTAMP) AS published,
                (version LIKE '%-%') AS is_prerelease
            FROM ranked
            WHERE rn = 1 AND is_delete = FALSE
        ''',
    ),
    SqlNodeSpec(
        id="nuget-packages-transform",
        deps=["nuget-package-versions", "nuget-packages"],
        sql=f'''
            WITH ranked AS ({_VERSIONS_RANKED}),
            live AS (
                SELECT
                    lower(package_id) AS pkg_key,
                    package_id,
                    CAST(commit_timestamp AS TIMESTAMP) AS published
                FROM ranked
                WHERE rn = 1 AND is_delete = FALSE
            ),
            agg AS (
                SELECT
                    pkg_key,
                    any_value(package_id) AS catalog_id,
                    count(*) AS version_count,
                    min(published) AS first_published,
                    max(published) AS last_published
                FROM live
                GROUP BY pkg_key
            )
            SELECT
                COALESCE(s.package_id, a.catalog_id) AS package_id,
                a.version_count,
                a.first_published,
                a.last_published,
                s.total_downloads,
                s.verified,
                s.latest_version,
                s.authors,
                s.tags
            FROM agg a
            LEFT JOIN "nuget-packages" s ON lower(s.package_id) = a.pkg_key
        ''',
    ),
]
