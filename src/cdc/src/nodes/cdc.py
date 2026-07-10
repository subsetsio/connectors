"""CDC (data.cdc.gov) connector — Socrata open-data portal.

Catalog connector: each accepted entity is one Socrata dataset, identified by its
stable 4x4 id (e.g. "24w5-nppr"). Raw extraction uses the per-dataset bulk CSV
export (`/api/views/{id}/rows.csv?accessType=DOWNLOAD`) — one stable URL per
dataset returning the entire table in a single request (chosen mechanism:
bulk_csv).

Fetch shape: stateless full re-pull. The portal exposes no changed-since feed, so
each dataset is re-fetched whole and its raw table overwritten; revisions and
late corrections come along for free. Exports are staged as local CSV and
converted to raw Parquet (they range from a few KB to ~28M rows), so downstream
profiling does not repeatedly sniff hundreds of remote gzip CSVs.

Withdrawn (404), login-gated (403), and >50M-row datasets are excluded by the
accept policy, so every id in ENTITY_IDS is expected to export in full.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_writer,
    transient_retry,
)

from constants import ENTITY_IDS

# Per-dataset bulk CSV export. The 4x4 id is the only variable; research verified
# the URL is persistent.
_EXPORT_URL = "https://data.cdc.gov/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"
_RESOURCE_CSV_URL = "https://data.cdc.gov/resource/{dataset_id}.csv"
_RESOURCE_JSON_URL = "https://data.cdc.gov/resource/{dataset_id}.json"

_CHUNK = 1 << 20  # 1 MiB
_PAGE_ROWS = 50_000
_YEAR_PARTITIONED_EXPORTS = {
    # Daily County-Level PM2.5 Concentrations 2001-2022. The single bulk CSV
    # stream is large enough to exceed the safety ceiling, but each year is a
    # bounded Socrata query and preserves the full table.
    "53mz-4zqd": [str(year) for year in range(2001, 2023)],
}

# Safety ceiling, not a run budget. The export is chunked (no Content-Length) and
# Socrata's anonymous pool throttles to ~1 MB/s, so a per-read timeout never fires
# on a slow-but-steady stream — a table that grew past what accept sized would
# otherwise stall the sequential DAG for hours. Sized well above the largest
# accepted table (~28M rows). Breaching it means the source outgrew our estimate:
# raise, so it surfaces as a failed spec rather than a silently truncated one.
_MAX_DOWNLOAD_SECONDS = 2700  # 45 min


def _sql_str(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _csv_to_parquet(csv_path: str, parquet_path: str) -> None:
    # Paths are inlined, not bound: DuckDB numbers `COPY … TO ?` as parameter 1,
    # so a prepared statement silently swaps the source and target paths.
    con = duckdb.connect()
    try:
        con.execute(
            f"""
            COPY (
                SELECT *
                FROM read_csv_auto({_sql_str(csv_path)}, header=true,
                                   all_varchar=true, sample_size=-1)
            )
            TO {_sql_str(parquet_path)} (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )
    finally:
        con.close()


def _csv_files_to_parquet(csv_glob: str, parquet_path: str) -> None:
    con = duckdb.connect()
    try:
        con.execute(
            f"""
            COPY (
                SELECT *
                FROM read_csv_auto({_sql_str(csv_glob)}, header=true,
                                   all_varchar=true, union_by_name=true,
                                   sample_size=-1)
            )
            TO {_sql_str(parquet_path)} (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )
    finally:
        con.close()


def _socrata_count(client, dataset_id: str, where: str) -> int:
    resp = client.get(
        _RESOURCE_JSON_URL.format(dataset_id=dataset_id),
        params={"$select": "count(*)", "$where": where},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return 0
    return int(data[0]["count"])


def _download_csv_page(client, dataset_id: str, where: str, offset: int, path: str) -> None:
    with client.stream(
        "GET",
        _RESOURCE_CSV_URL.format(dataset_id=dataset_id),
        params={
            "$where": where,
            "$limit": str(_PAGE_ROWS),
            "$offset": str(offset),
        },
        timeout=(10.0, 300.0),
    ) as resp:
        resp.raise_for_status()
        with open(path, "wb") as out:
            for chunk in resp.iter_bytes(_CHUNK):
                out.write(chunk)


@transient_retry()
def _download_year_partitioned_parquet(dataset_id: str, asset: str, years: list[str]) -> None:
    """Fetch a very large Socrata table in year partitions and store Parquet."""
    client = get_client()
    tmpdir = tempfile.mkdtemp(prefix=f"{asset}-")
    chunks_dir = os.path.join(tmpdir, "chunks")
    parquet_path = os.path.join(tmpdir, "data.parquet")
    os.makedirs(chunks_dir, exist_ok=True)
    try:
        chunk_index = 0
        for year in years:
            where = f"year='{year}'"
            rows = _socrata_count(client, dataset_id, where)
            for offset in range(0, rows, _PAGE_ROWS):
                chunk_path = os.path.join(chunks_dir, f"chunk-{chunk_index:05d}.csv")
                _download_csv_page(client, dataset_id, where, offset, chunk_path)
                chunk_index += 1

        _csv_files_to_parquet(os.path.join(chunks_dir, "*.csv"), parquet_path)

        with open(parquet_path, "rb") as src, raw_writer(asset, "parquet", mode="wb") as out:
            shutil.copyfileobj(src, out, length=_CHUNK)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@transient_retry()
def _download_parquet(url: str, asset: str) -> None:
    """Fetch one dataset's full CSV export and store it as raw Parquet.

    The source contract is still Socrata's bulk CSV endpoint. Parquet is the
    raw storage format so model verification and transforms can use
    `read_parquet` instead of remote CSV dialect inference. Writing raw inside
    the retried fn is deliberate: a mid-stream transient failure rewrites the
    full asset on retry, so partial bytes never become the manifest entry.
    """
    client = get_client()
    started = time.monotonic()
    tmpdir = tempfile.mkdtemp(prefix=f"{asset}-")
    csv_path = os.path.join(tmpdir, "data.csv")
    parquet_path = os.path.join(tmpdir, "data.parquet")
    try:
        # (connect, read) — a generous read window for multi-MB exports.
        with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
            resp.raise_for_status()
            with open(csv_path, "wb") as out:
                for chunk in resp.iter_bytes(_CHUNK):
                    out.write(chunk)
                    if time.monotonic() - started > _MAX_DOWNLOAD_SECONDS:
                        raise RuntimeError(
                            f"{asset}: bulk CSV export still streaming after "
                            f"{_MAX_DOWNLOAD_SECONDS}s — the table has outgrown the "
                            "size accept sized it at; re-measure and re-decide it"
                        )

        _csv_to_parquet(csv_path, parquet_path)
        os.remove(csv_path)

        with open(parquet_path, "rb") as src, raw_writer(asset, "parquet", mode="wb") as out:
            shutil.copyfileobj(src, out, length=_CHUNK)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def fetch_one(node_id: str) -> None:
    """Fetch one Socrata dataset's full table. The runtime passes the spec id,
    which is also the raw asset name; the dataset's 4x4 id is the id minus the
    "cdc-" prefix."""
    dataset_id = node_id[len("cdc-"):]
    if dataset_id in _YEAR_PARTITIONED_EXPORTS:
        _download_year_partitioned_parquet(dataset_id, node_id, _YEAR_PARTITIONED_EXPORTS[dataset_id])
        return
    _download_parquet(_EXPORT_URL.format(dataset_id=dataset_id), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cdc-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Freshness policy — also the intra-run resume mechanism.
#
# There is no portal-wide changed-since feed, and the bulk CSV export offers no
# HEAD validator to diff against (no ETag, no Last-Modified), so `source_unchanged`
# has nothing to compare and freshness falls back to age.
#
# The window doubles as the DAG's continuation-resume signal: the raw manifest
# spans runs, so when a long sequential run is interrupted and relaunched, every
# dataset an earlier link already fetched reads back as fresh and is skipped,
# letting the corpus accumulate across links instead of restarting each time.
#
# 6 days sits just under the 7-day refresh cadence: a scheduled weekly re-run sees
# the prior run's raw as ~7d old and re-pulls the whole corpus, while any single
# run always skips what it has already fetched. FORCE_REFRESH=1 bypasses this.
_MAINTAIN_MAX_AGE_DAYS = 6

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=s.id,
        description=(
            "Full corpus re-pull on the 7-day cadence (no source changed-since "
            "feed and no HEAD validator on the export); age-gated at 6 days, "
            "which also drives within-run continuation resume."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=_MAINTAIN_MAX_AGE_DAYS),
    )
    for s in DOWNLOAD_SPECS
]
