"""Maven Central (Sonatype) connector — the artifact catalog corpus.

One subset: `artifacts` — the full Maven Central artifact catalog, one row per
unique groupId:artifactId (~662k as of 2026-06-27). Enumerated by deep-paging
the public Solr search API (search.maven.org/solrsearch/select, q=*:*, default
core), which is the only verified machine-readable enumeration surface for the
public Central catalog (the bulk .index is a JVM-only Lucene binary; see
research).

Fetch shape: stateless full re-pull. The corpus is bounded (~662k rows, ~50MB
parquet) and fully enumerable in one run, so there is no watermark/cursor — we
walk `start` from 0 to numFound every refresh and overwrite. Revisions and new
artifacts are picked up for free.

Pagination: offset (`start`) only. This Solr instance does NOT support
`cursorMark` (probed 2026-06-27 — no `nextCursorMark` in the response), so the
efficient cursor path is unavailable; plain offset paging is verified to work
across the whole corpus (start=660000 returns rows). We sort by `id asc` so the
page window is stable against the rare insert during the crawl; any boundary
duplicate from offset drift is de-duplicated in the transform.

Rate limits: search.maven.org has no documented limit but is aggressively
throttled behind Cloudflare (observed multi-minute connection drops after a
burst). We page serially with a polite inter-page sleep and lean on
`transient_retry()` (handles 429/5xx/connect+read timeouts with exponential
backoff).
"""
import time

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, raw_parquet_writer

BASE_URL = "https://search.maven.org/solrsearch/select"
PAGE_SIZE = 200                 # verified working page size (rows=200 -> 200 docs)
INTER_PAGE_SLEEP = 0.5          # politeness: serial paging with a small gap
# Safety ceiling: ~662k/200 ~= 3310 pages today. 8000 pages = ~1.6M artifacts;
# if we ever cross it, the corpus grew far past expectation OR pagination is
# looping — fail loudly rather than crawl forever.
MAX_PAGES = 8000

SCHEMA = pa.schema([
    ("group_id",       pa.string()),
    ("artifact_id",    pa.string()),
    ("latest_version", pa.string()),
    ("packaging",      pa.string()),
    ("version_count",  pa.int64()),
    ("repository_id",  pa.string()),
    ("last_updated",   pa.timestamp("ms")),
])


@transient_retry()
def _fetch_page(start: int) -> dict:
    """One page of the Solr catalog at offset `start`. raise_for_status inside
    the retry so 429/5xx are retried with backoff."""
    resp = get(
        BASE_URL,
        params={
            "q": "*:*",
            "wt": "json",
            "rows": PAGE_SIZE,
            "start": start,
            "sort": "id asc",   # stable ordering for offset paging
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _rows_to_batch(docs: list[dict]) -> pa.RecordBatch:
    group_id, artifact_id, latest_version, packaging = [], [], [], []
    version_count, repository_id, last_updated = [], [], []
    for d in docs:
        group_id.append(d.get("g"))
        artifact_id.append(d.get("a"))
        latest_version.append(d.get("latestVersion"))
        packaging.append(d.get("p"))
        vc = d.get("versionCount")
        version_count.append(int(vc) if vc is not None else None)
        repository_id.append(d.get("repositoryId"))
        # Solr `timestamp` is epoch milliseconds of the latest version.
        last_updated.append(d.get("timestamp"))
    return pa.RecordBatch.from_arrays(
        [
            pa.array(group_id, pa.string()),
            pa.array(artifact_id, pa.string()),
            pa.array(latest_version, pa.string()),
            pa.array(packaging, pa.string()),
            pa.array(version_count, pa.int64()),
            pa.array(repository_id, pa.string()),
            pa.array(last_updated, pa.int64()).cast(pa.timestamp("ms")),
        ],
        schema=SCHEMA,
    )


def fetch_artifacts(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    first = _fetch_page(0)
    num_found = first["response"]["numFound"]
    if num_found <= 0:
        raise AssertionError(f"{asset}: solrsearch returned numFound={num_found}")

    with raw_parquet_writer(asset, SCHEMA) as writer:
        start = 0
        pages = 0
        seen = 0
        while True:
            page = first if start == 0 else _fetch_page(start)
            docs = page["response"]["docs"]
            if not docs:
                break
            writer.write_batch(_rows_to_batch(docs))
            seen += len(docs)
            pages += 1
            start += PAGE_SIZE
            if start >= num_found:
                break
            if pages >= MAX_PAGES:
                raise AssertionError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} at start={start} "
                    f"(numFound={num_found}); corpus grew unexpectedly or paging looped"
                )
            time.sleep(INTER_PAGE_SLEEP)

    print(f"  {asset}: wrote {seen} artifact rows ({pages} pages, numFound={num_found})")


DOWNLOAD_SPECS = [
    NodeSpec(id="maven-central-artifacts", fn=fetch_artifacts, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="maven-central-artifacts-transform",
        deps=["maven-central-artifacts"],
        sql='''
            SELECT
                group_id,
                artifact_id,
                latest_version,
                packaging,
                version_count,
                CAST(last_updated AS TIMESTAMP) AS last_updated
            FROM "maven-central-artifacts"
            WHERE group_id IS NOT NULL AND artifact_id IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY group_id, artifact_id
                ORDER BY last_updated DESC NULLS LAST
            ) = 1
        ''',
    ),
]
