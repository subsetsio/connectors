"""nflfastR / nflverse connector.

Mechanism: bulk parquet assets published on the nflverse/nflverse-data GitHub
releases (one release tag per dataset family). For each entity we list the
release's assets, keep the parquet files whose season-stripped stem equals the
entity id (one per season, or a single whole-corpus file), download them, and
union them by name into a single combined raw parquet.

Schemas drift slightly across seasons (columns added in later years, an int
column that became a double), so the files are unioned with DuckDB
`union_by_name=true`, which aligns columns by name and promotes numeric types.
The union is streamed in bounded batches to keep memory flat even for the
372-column play-by-play corpus (~1.3M rows).

Fetch shape: stateless full re-pull. The whole corpus is a few GB and the
nflverse releases are rebuilt nightly during the season with revisions to prior
weeks; trusting a stored watermark would silently skip those revisions. Each run
re-downloads every season and overwrites — freshness gating is the maintain
step's job, not ours.
"""

from __future__ import annotations

import os
import re
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS, ENTITY_TAGS, REPO

_API = f"https://api.github.com/repos/{REPO}/releases/tags"
_DL = f"https://github.com/{REPO}/releases/download"
_BATCH_ROWS = 20_000  # cap rows per streamed batch → bounded memory


def _stem(asset_name: str) -> str:
    """Filename stem with the season-year token removed — must match the entity
    ids produced by collect (e.g. 'play_by_play_2025.parquet' -> 'play_by_play',
    'ngs_2021_passing.parquet' -> 'ngs_passing')."""
    n = asset_name[:-len(".parquet")] if asset_name.endswith(".parquet") else asset_name
    n = re.sub(r"_?(?:19|20)\d\d", "", n)
    n = re.sub(r"__+", "_", n).strip("_")
    return n


def _gh_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


@transient_retry()
def _release_parquet_assets(tag: str) -> list[str]:
    """Parquet asset filenames for a release tag (via the GitHub releases API)."""
    resp = get(f"{_API}/{tag}", headers=_gh_headers(), timeout=(10.0, 60.0))
    resp.raise_for_status()
    return [a["name"] for a in resp.json().get("assets", []) if a["name"].endswith(".parquet")]


@transient_retry()
def _download_to(path: str, url: str) -> None:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    with open(path, "wb") as fh:
        fh.write(resp.content)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = node_id[len("nflfastr-"):].replace("-", "_")
    tag = ENTITY_TAGS[entity]

    all_assets = _release_parquet_assets(tag)
    files = sorted(name for name in all_assets if _stem(name) == entity)
    if not files:
        # A missing entity means the release layout changed — fail loudly so the
        # run records it rather than silently publishing nothing.
        raise AssertionError(
            f"{node_id}: no parquet assets with stem '{entity}' in release "
            f"'{tag}' (saw {all_assets[:8]})"
        )

    with tempfile.TemporaryDirectory() as tmp:
        local = []
        for name in files:
            dst = os.path.join(tmp, name)
            _download_to(dst, f"{_DL}/{tag}/{name}")
            local.append(dst)

        con = duckdb.connect()
        try:
            rel = con.sql(f"SELECT * FROM read_parquet({local!r}, union_by_name=true)")
            reader = rel.fetch_record_batch(rows_per_batch=_BATCH_ROWS)
            with raw_parquet_writer(asset, reader.schema) as writer:
                for batch in reader:
                    if batch.num_rows:
                        writer.write_batch(batch)
        finally:
            con.close()


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nflfastr-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
