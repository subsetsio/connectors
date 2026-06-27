"""Maven Central (Sonatype) connector — the artifact catalog corpus.

One subset: `artifacts` — the full Maven Central artifact catalog, one row per
unique groupId:artifactId (~662k as of 2026-06-27). Enumerated by paging the
public Solr search API (search.maven.org/solrsearch/select, q=*:*, default
core), which is the only verified machine-readable enumeration surface for the
public Central catalog (the bulk .index is a JVM-only Lucene binary; see
research).

Fetch shape: stateless full re-pull. The corpus is bounded (~662k rows, ~50MB
parquet) and fully enumerable in one run, so there is no watermark/cursor — we
walk `start` from 0 to numFound every refresh and overwrite. Revisions and new
artifacts are picked up for free.

Pagination constraints (probed 2026-06-27):
  * `rows` is server-capped: values above ~200 silently fall back to the default
    20, so PAGE_SIZE is pinned at 200 (verified to return 200 docs/page).
  * `cursorMark` is NOT supported (no nextCursorMark in the response) and a
    custom `sort` is silently IGNORED (the endpoint always returns its default
    score+timestamp order). So neither cursor nor id-range paging is possible —
    plain `start` offset paging is the only option, verified to work across the
    whole corpus (start=660000 returns rows). Because the default order is
    timestamp-based and not stable against inserts, a long crawl can see a few
    boundary duplicates as new artifacts shift the window; the transform
    de-duplicates by (group_id, artifact_id).

Rate limits: search.maven.org sits behind Cloudflare with no documented limit
but aggressive bot/rate mitigation — a default Python User-Agent from a
datacenter IP gets 403'd within tens of requests. We therefore send a browser
User-Agent and page serially with a polite gap, and retry 403/429/5xx/network
errors with exponential backoff (a Cloudflare 403 here is a rate-block, not a
true permanent error).
"""
import time

import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    is_transient,
    raw_parquet_writer,
)

BASE_URL = "https://search.maven.org/solrsearch/select"
PAGE_SIZE = 200                 # server cap; larger values silently fall back to 20
INTER_PAGE_SLEEP = 1.0          # politeness gap between successful pages
# Safety ceiling: ~662k/200 ~= 3310 pages today. 8000 pages = ~1.6M artifacts;
# crossing it means the corpus grew far past expectation OR paging looped —
# fail loudly rather than crawl forever.
MAX_PAGES = 8000

# A real browser UA — Cloudflare 403s obvious non-browser agents from
# datacenter IPs. ASCII only (httpx requires it).
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

SCHEMA = pa.schema([
    ("group_id",       pa.string()),
    ("artifact_id",    pa.string()),
    ("latest_version", pa.string()),
    ("packaging",      pa.string()),
    ("version_count",  pa.int64()),
    ("repository_id",  pa.string()),
    ("last_updated",   pa.timestamp("ms")),
])


def _is_retryable(exc: BaseException) -> bool:
    """Standard transient classification PLUS Cloudflare 403 (a rate-block on
    this host, not a genuine authorization failure)."""
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 403
    return False


@retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=5, max=120),
    reraise=True,
)
def _fetch_page(start: int) -> dict:
    """One page of the Solr catalog at offset `start`. raise_for_status inside
    the retry so 403/429/5xx are retried with backoff."""
    resp = get(
        BASE_URL,
        params={"q": "*:*", "wt": "json", "rows": PAGE_SIZE, "start": start},
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
    configure_http(headers={"User-Agent": USER_AGENT})

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
