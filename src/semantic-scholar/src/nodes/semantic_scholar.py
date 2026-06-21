"""Semantic Scholar connector — Academic Graph Datasets API (bulk).

Mechanism (datasets_bulk): the Datasets API exposes the corpus as a fixed set
of named datasets, each a dated release sharded into ~30 gzipped JSON-Lines
files. We fetch the two rank-accepted reference tables:

  - publication-venues : small journal/conference reference table.
  - authors            : ~75M author records (~3GB gz) with bibliometric stats.

For each, GET /datasets/v1/release/latest/dataset/{name} with the S2_API_KEY in
the `x-api-key` header to obtain `files` — a list of pre-signed shard URLs (the
links are time-limited, so we download them immediately). Each shard is gzipped
JSON-Lines; we stream the lines verbatim into one combined `<asset>.ndjson.gz`,
overwriting on every run. The SQL transforms project the stable scalar columns.

Strategy: stateless full re-pull. The corpus is a point-in-time snapshot that
fully supersedes the prior release, and the accepted datasets are small enough
to re-fetch each refresh, so there is no watermark/cursor state — we always
pull the latest release and overwrite. (The much larger datasets — papers,
citations, embeddings — were deliberately left below the publish threshold.)
"""

from __future__ import annotations

import gzip
import io
import os


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

_DATASETS_BASE = "https://api.semanticscholar.org/datasets/v1"

# entity ids in the rank-accepted entity union (work/entity_union.json).
ENTITY_IDS = ["authors", "publication-venues"]


@transient_retry()
def _get_dataset_files(entity: str, api_key: str) -> list[str]:
    """Resolve the pre-signed shard URLs for a dataset's latest release."""
    url = f"{_DATASETS_BASE}/release/latest/dataset/{entity}"
    resp = get(url, headers={"x-api-key": api_key}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    doc = resp.json()
    files = doc.get("files")
    if not isinstance(files, list) or not files:
        raise RuntimeError(
            f"dataset {entity!r}: response had no 'files' list (keys: "
            f"{sorted(doc)[:10]})"
        )
    return files


@transient_retry()
def _download_shard(url: str) -> bytes:
    """Download one gzipped JSON-Lines shard (pre-signed S3/CloudFront URL).

    No api-key header here — the URL is already pre-signed; extra auth headers
    are unnecessary and can confuse S3 signature validation."""
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("semantic-scholar-") :]

    api_key = os.environ.get("S2_API_KEY")
    if not api_key:
        raise RuntimeError(
            "S2_API_KEY is not set; the Semantic Scholar Datasets API requires "
            "an API key (x-api-key header) to obtain dataset download links. "
            "Request one at https://www.semanticscholar.org/product/api"
        )

    files = _get_dataset_files(entity, api_key)
    print(f"[{asset}] {len(files)} shard(s) for latest release")

    total_lines = 0
    # Stream every shard's lines verbatim into one combined ndjson.gz asset,
    # overwriting any prior release. Bounded memory: one shard in flight.
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for i, url in enumerate(files):
            content = _download_shard(url)
            shard_lines = 0
            with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz:
                for raw_line in gz:
                    line = raw_line.decode("utf-8")
                    if not line.strip():
                        continue
                    if not line.endswith("\n"):
                        line += "\n"
                    out.write(line)
                    shard_lines += 1
            total_lines += shard_lines
            print(f"[{asset}] shard {i + 1}/{len(files)}: {shard_lines} records")

    if total_lines == 0:
        # Safety ceiling: a non-empty file list that yields zero records means
        # the shard format changed or every download was truncated.
        raise RuntimeError(f"{asset}: downloaded {len(files)} shards but 0 records")
    print(f"[{asset}] total records: {total_lines}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"semantic-scholar-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --- transforms: one published Delta table per accepted dataset ----------------
#
# Raw is the source's verbatim JSON-Lines; each transform projects the stable,
# well-documented scalar columns and casts them. Nested fields (externalids,
# affiliations, aliases, alternate_names) are intentionally dropped — the
# published tables are clean reference/statistics tables.

_AUTHORS_SQL = '''
    SELECT
        CAST(authorid AS VARCHAR)        AS author_id,
        CAST(name AS VARCHAR)            AS name,
        CAST(url AS VARCHAR)             AS url,
        TRY_CAST(papercount AS BIGINT)   AS paper_count,
        TRY_CAST(citationcount AS BIGINT) AS citation_count,
        TRY_CAST(hindex AS BIGINT)       AS h_index
    FROM "semantic-scholar-authors"
    WHERE authorid IS NOT NULL
'''

_VENUES_SQL = '''
    SELECT
        CAST(id AS VARCHAR)   AS venue_id,
        CAST(name AS VARCHAR) AS name,
        CAST(type AS VARCHAR) AS type,
        CAST(issn AS VARCHAR) AS issn,
        CAST(url AS VARCHAR)  AS url
    FROM "semantic-scholar-publication-venues"
    WHERE id IS NOT NULL
'''

_TRANSFORM_SQL = {
    "semantic-scholar-authors": _AUTHORS_SQL,
    "semantic-scholar-publication-venues": _VENUES_SQL,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id],
    )
    for s in DOWNLOAD_SPECS
]
