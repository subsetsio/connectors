"""Docker Hub pull stats connector.

Publishes engagement statistics for the Docker Official Images — the curated
'library' namespace (~179 actively-maintained base images: nginx, ubuntu, redis,
postgres, ...). Two subsets:

  - docker-hub-official-images : reference catalog (one row per official image)
  - docker-hub-pull-stats      : pull/star statistics snapshot (one row per image)

The Docker Hub REST API (mechanism 'rest_v2') exposes only CURRENT cumulative
pull/star totals — there is no historical/time-series endpoint — so each refresh
captures a full snapshot of the namespace and stamps pull-stats rows with the
fetch date. The whole namespace is ~179 repos across 2 pages, so the correct
shape is a stateless full re-pull every run (no watermark, no cursor).
"""

from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)

LIBRARY_URL = "https://hub.docker.com/v2/repositories/library/"
PAGE_SIZE = 100
MAX_PAGES = 50  # safety ceiling: ~179 repos = 2 pages; a runaway means the API changed


@transient_retry()  # 6 attempts, exponential backoff over 429/5xx/transient network errors
def _get_page(url: str, params: dict | None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_library_repos() -> list[dict]:
    """Page through the entire 'library' namespace and return every repo record."""
    rows: list[dict] = []
    url: str | None = LIBRARY_URL
    params: dict | None = {"page_size": PAGE_SIZE, "page": 1}
    pages = 0
    while url:
        pages += 1
        if pages > MAX_PAGES:
            raise RuntimeError(
                f"library namespace exceeded {MAX_PAGES} pages; "
                "the API shape or namespace size changed unexpectedly"
            )
        data = _get_page(url, params)
        rows.extend(data.get("results", []))
        url = data.get("next")  # absolute next-page URL, already carries page/page_size
        params = None
    return rows


def fetch_official_images(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    repos = _fetch_library_repos()
    rows = [
        {
            "namespace": r.get("namespace"),
            "repo": r.get("name"),
            "description": r.get("description"),
            "repository_type": r.get("repository_type"),
            "status": r.get("status"),
            "status_description": r.get("status_description"),
            "date_registered": r.get("date_registered"),
            "last_updated": r.get("last_updated"),
            "storage_size": r.get("storage_size"),
            "categories": ",".join(
                c["slug"] for c in (r.get("categories") or []) if isinstance(c, dict) and c.get("slug")
            ),
        }
        for r in repos
    ]
    schema = pa.schema(
        [
            ("namespace", pa.string()),
            ("repo", pa.string()),
            ("description", pa.string()),
            ("repository_type", pa.string()),
            ("status", pa.int64()),
            ("status_description", pa.string()),
            ("date_registered", pa.string()),
            ("last_updated", pa.string()),
            ("storage_size", pa.int64()),
            ("categories", pa.string()),
        ]
    )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), asset)


def fetch_pull_stats(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    snapshot_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    repos = _fetch_library_repos()
    rows = [
        {
            "snapshot_date": snapshot_date,
            "namespace": r.get("namespace"),
            "repo": r.get("name"),
            "pull_count": r.get("pull_count"),
            "star_count": r.get("star_count"),
            "last_updated": r.get("last_updated"),
        }
        for r in repos
    ]
    schema = pa.schema(
        [
            ("snapshot_date", pa.string()),
            ("namespace", pa.string()),
            ("repo", pa.string()),
            ("pull_count", pa.int64()),
            ("star_count", pa.int64()),
            ("last_updated", pa.string()),
        ]
    )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="docker-hub-official-images", fn=fetch_official_images, kind="download"),
    NodeSpec(id="docker-hub-pull-stats", fn=fetch_pull_stats, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="docker-hub-official-images-transform",
        deps=["docker-hub-official-images"],
        sql='''
            SELECT
                namespace,
                repo,
                description,
                repository_type,
                CAST(status AS INTEGER)               AS status,
                status_description,
                CAST(date_registered AS TIMESTAMP)    AS date_registered,
                CAST(last_updated AS TIMESTAMP)       AS last_updated,
                CAST(storage_size AS BIGINT)          AS storage_size_bytes,
                NULLIF(categories, '')                AS categories
            FROM "docker-hub-official-images"
            WHERE repo IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="docker-hub-pull-stats-transform",
        deps=["docker-hub-pull-stats"],
        sql='''
            SELECT
                CAST(snapshot_date AS DATE)      AS snapshot_date,
                namespace,
                repo,
                CAST(pull_count AS BIGINT)       AS pull_count,
                CAST(star_count AS BIGINT)       AS star_count,
                CAST(last_updated AS TIMESTAMP)  AS last_updated
            FROM "docker-hub-pull-stats"
            WHERE repo IS NOT NULL
              AND pull_count IS NOT NULL
        ''',
    ),
]
