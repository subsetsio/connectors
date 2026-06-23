"""Hugging Face Hub connector.

Publishes the Hub's catalog metadata as four Delta tables — one per artifact
type (models, datasets, spaces) plus the curated daily-papers feed. Each is a
homogeneous corpus (one row per repo / paper), so each is ONE table; the
pipeline_tag / library_name / sdk / tags fields are column VALUES, never a
basis for splitting.

Fetch strategy — stateless full re-pull (the default shape). The three list
endpoints are paged in full every run via the RFC-5988 Link `rel="next"`
cursor (`?full=true&limit=1000`) and streamed straight to a single
`<asset>.ndjson.gz` (memory-bounded; the file is overwritten each run, so
revisions and deletions are picked up for free). There is no server-side
`since` filter (only a `sort=lastModified` ordering), so a delta pull cannot
compose with the overwrite-publish model — full re-pull is correct here. The
corpus is large (~2M models, ~450k datasets, ~700k spaces) so a full run makes
a few thousand requests; an HF_TOKEN bearer (read opportunistically from the
env) raises the anonymous 500-req/300s rate limit substantially. 429/5xx are
ridden out by transient_retry's backoff.

Raw is NDJSON (records carry list/optional fields); the SQL transforms re-type
and dedup on read. daily_papers is small enough to buffer in memory.
"""

from __future__ import annotations

import json
import os

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
    save_raw_ndjson,
)

BASE = "https://huggingface.co/api"

# Per-endpoint projection: the scalar catalog fields we publish, kept verbatim
# under the source's own key names. Every row emits the full key set (None when
# the field is absent on that repo) so read_json_auto sees stable columns.
LIST_FIELDS = {
    "models": [
        "id", "author", "downloads", "likes", "trendingScore",
        "pipeline_tag", "library_name", "gated", "private",
        "createdAt", "lastModified", "sha",
    ],
    "datasets": [
        "id", "author", "downloads", "likes", "trendingScore",
        "gated", "private", "createdAt", "lastModified", "sha",
    ],
    "spaces": [
        "id", "author", "likes", "trendingScore", "sdk", "private",
        "createdAt", "lastModified", "sha",
    ],
}

# Safety ceiling — detects runaway pagination / unexpected source growth and
# RAISES (never silently truncates). ~2M models / 1000 per page ≈ 2000 pages,
# so 50k is comfortable headroom.
MAX_PAGES = 50_000


def _auth_headers() -> dict:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


@transient_retry(attempts=10, min_wait=4, max_wait=300)
def _get(url: str, params: dict | None = None):
    resp = get(url, params=params, headers=_auth_headers(), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _project_list_row(row: dict, fields: list[str]) -> dict:
    out = {k: row.get(k) for k in fields}
    g = out.get("gated")
    out["gated"] = None if g is None else str(g)  # bool | "auto" | "manual" -> str
    tags = row.get("tags")
    out["tags"] = [t for t in tags if isinstance(t, str)] if isinstance(tags, list) else []
    return out


def fetch_list(node_id: str) -> None:
    """Full cursor-paged pull of one list endpoint (models/datasets/spaces)."""
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    endpoint = node_id[len("hugging-face-hub-"):]
    fields = LIST_FIELDS[endpoint]

    pages = 0
    n_rows = 0
    next_url = None
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        while True:
            if next_url:
                resp = _get(next_url)
            else:
                resp = _get(f"{BASE}/{endpoint}", params={"limit": 1000, "full": "true"})
            for row in resp.json():
                f.write(json.dumps(_project_list_row(row, fields), ensure_ascii=False) + "\n")
                n_rows += 1

            pages += 1
            if pages > MAX_PAGES:
                raise RuntimeError(
                    f"{endpoint}: exceeded MAX_PAGES={MAX_PAGES} (source grew past "
                    "expectations or pagination is looping) — investigate before raising the cap"
                )
            next_url = resp.links.get("next", {}).get("url")
            if not next_url:
                break
    print(f"  {endpoint}: {n_rows} rows across {pages} pages")


def fetch_daily_papers(node_id: str) -> None:
    """Pull the curated daily-papers feed, flattening the nested `paper` object."""
    asset = node_id
    rows = []
    pages = 0
    next_url = None
    while True:
        if next_url:
            resp = _get(next_url)
        else:
            resp = _get(f"{BASE}/daily_papers", params={"limit": 100})
        for item in resp.json():
            paper = item.get("paper") or {}
            rows.append({
                "paper_id": paper.get("id") or item.get("paper_id"),
                "title": item.get("title") or paper.get("title"),
                "summary": item.get("summary") or paper.get("summary"),
                "published_at": item.get("publishedAt") or paper.get("publishedAt"),
                "submitted_on_daily_at": paper.get("submittedOnDailyAt") or item.get("submittedOnDailyAt"),
                "upvotes": paper.get("upvotes"),
                "num_comments": item.get("numComments"),
            })
        pages += 1
        if pages > MAX_PAGES:
            raise RuntimeError(f"daily_papers: exceeded MAX_PAGES={MAX_PAGES}")
        next_url = resp.links.get("next", {}).get("url")
        if not next_url:
            break
    save_raw_ndjson(rows, asset)
    print(f"  daily_papers: {len(rows)} rows across {pages} pages")


DOWNLOAD_SPECS = [
    NodeSpec(id="hugging-face-hub-models", fn=fetch_list, kind="download"),
    NodeSpec(id="hugging-face-hub-datasets", fn=fetch_list, kind="download"),
    NodeSpec(id="hugging-face-hub-spaces", fn=fetch_list, kind="download"),
    NodeSpec(id="hugging-face-hub-daily-papers", fn=fetch_daily_papers, kind="download"),
]


_MODELS_SQL = '''
    SELECT
        id,
        author,
        TRY_CAST(downloads AS BIGINT)      AS downloads,
        TRY_CAST(likes AS BIGINT)          AS likes,
        TRY_CAST(trendingScore AS BIGINT)  AS trending_score,
        pipeline_tag,
        library_name,
        gated,
        TRY_CAST(private AS BOOLEAN)       AS private,
        TRY_CAST(createdAt AS TIMESTAMP)   AS created_at,
        TRY_CAST(lastModified AS TIMESTAMP) AS last_modified,
        tags
    FROM "hugging-face-hub-models"
    WHERE id IS NOT NULL
    QUALIFY row_number() OVER (PARTITION BY id ORDER BY lastModified DESC) = 1
'''

_DATASETS_SQL = '''
    SELECT
        id,
        author,
        TRY_CAST(downloads AS BIGINT)      AS downloads,
        TRY_CAST(likes AS BIGINT)          AS likes,
        TRY_CAST(trendingScore AS BIGINT)  AS trending_score,
        gated,
        TRY_CAST(private AS BOOLEAN)       AS private,
        TRY_CAST(createdAt AS TIMESTAMP)   AS created_at,
        TRY_CAST(lastModified AS TIMESTAMP) AS last_modified,
        tags
    FROM "hugging-face-hub-datasets"
    WHERE id IS NOT NULL
    QUALIFY row_number() OVER (PARTITION BY id ORDER BY lastModified DESC) = 1
'''

_SPACES_SQL = '''
    SELECT
        id,
        author,
        TRY_CAST(likes AS BIGINT)          AS likes,
        TRY_CAST(trendingScore AS BIGINT)  AS trending_score,
        sdk,
        TRY_CAST(private AS BOOLEAN)       AS private,
        TRY_CAST(createdAt AS TIMESTAMP)   AS created_at,
        TRY_CAST(lastModified AS TIMESTAMP) AS last_modified,
        tags
    FROM "hugging-face-hub-spaces"
    WHERE id IS NOT NULL
    QUALIFY row_number() OVER (PARTITION BY id ORDER BY lastModified DESC) = 1
'''

_DAILY_PAPERS_SQL = '''
    SELECT
        paper_id,
        title,
        summary,
        TRY_CAST(published_at AS TIMESTAMP)         AS published_at,
        TRY_CAST(submitted_on_daily_at AS TIMESTAMP) AS submitted_on_daily_at,
        TRY_CAST(upvotes AS BIGINT)                  AS upvotes,
        TRY_CAST(num_comments AS BIGINT)             AS num_comments
    FROM "hugging-face-hub-daily-papers"
    WHERE paper_id IS NOT NULL
    QUALIFY row_number() OVER (PARTITION BY paper_id ORDER BY submitted_on_daily_at DESC NULLS LAST) = 1
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="hugging-face-hub-models-transform",
                deps=["hugging-face-hub-models"], sql=_MODELS_SQL),
    SqlNodeSpec(id="hugging-face-hub-datasets-transform",
                deps=["hugging-face-hub-datasets"], sql=_DATASETS_SQL),
    SqlNodeSpec(id="hugging-face-hub-spaces-transform",
                deps=["hugging-face-hub-spaces"], sql=_SPACES_SQL),
    SqlNodeSpec(id="hugging-face-hub-daily-papers-transform",
                deps=["hugging-face-hub-daily-papers"], sql=_DAILY_PAPERS_SQL),
]
