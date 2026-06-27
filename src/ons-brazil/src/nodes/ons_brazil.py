"""ONS (Brazil grid) open-data connector.

Source: the ONS CKAN portal at https://dados.ons.org.br (mechanism `ckan`,
anonymous). Each rank-accepted package is one publishable dataset. A package's
resources are direct-download files on the public S3 bucket
`ons-aws-prod-opendata`, shipped as one CSV + one XLSX + one Parquet per year
(plus PDF/JSON data dictionaries we ignore). We pull the Parquet variant of
every data resource and union the years into one raw asset per dataset.

Shape: stateless full re-pull (shape 1). No incremental filter exists on CKAN
package data, so each refresh re-reads the full corpus and picks up the
source's recurring revisions for free.

A dataset is the union of its yearly/daily Parquet resources. Some datasets
(hourly/semi-hourly: dados_hidrologicos_ho, programacao_*, disponibilidade_usina)
span hundreds of files and are far too large to concatenate in memory. So we:

  1. download each resource to a local temp file (httpx, retried) — reliable,
     and avoids DuckDB httpfs range-read flakiness on S3;
  2. let DuckDB read the local files with `union_by_name=true` (unifying the
     per-year schemas: columns added over time, occasional type drift) and
     stream the result to one raw Parquet via the streaming writer.

Memory is bounded regardless of dataset size — the per-year files live on disk,
DuckDB streams batches, and only one download sits in RAM at a time. A single
output file keeps the SQL transform's `read_parquet([...])` happy (it does not
union by name).
"""

import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "ons-brazil"
CKAN_BASE = "https://dados.ons.org.br/api/3/action"

# spec id (lowercased, underscores->hyphens) -> original CKAN package id.
# The CKAN id is needed verbatim to query package_show, and is not always
# recoverable from the spec id (some ids contain genuine hyphens).
SPEC_TO_PKG = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/transient network
def _parquet_urls(pkg_id: str) -> list[str]:
    """The S3 Parquet resource URLs for one CKAN package."""
    resp = get(
        f"{CKAN_BASE}/package_show",
        params={"id": pkg_id},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"package_show {pkg_id}: success=false")
    return [
        r["url"]
        for r in body["result"]["resources"]
        if (r.get("format") or "").upper() == "PARQUET" and r.get("url")
    ]


@transient_retry()
def _download_to(url: str, path: str) -> None:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    with open(path, "wb") as f:  # local scratch file, not a raw asset
        f.write(resp.content)


def fetch_one(node_id: str) -> None:
    """Download every Parquet resource of one CKAN package to local scratch,
    union the per-year schemas via DuckDB, and stream a single raw parquet
    asset named after the spec id."""
    asset = node_id
    pkg_id = SPEC_TO_PKG[node_id]

    urls = _parquet_urls(pkg_id)
    if not urls:
        # Every rank-accepted package advertised a PARQUET variant at collect
        # time; none here means the source changed shape — fail loudly.
        raise RuntimeError(f"{pkg_id}: no PARQUET resources found")

    with tempfile.TemporaryDirectory(prefix=f"{asset}-") as tmp:
        local_files = [os.path.join(tmp, f"{i:05d}.parquet") for i in range(len(urls))]
        # The pooled httpx client is thread-safe; S3 per-request latency
        # dominates, so fetch in parallel. Exceptions propagate (fail the spec).
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda pair: _download_to(*pair), zip(urls, local_files)))

        con = duckdb.connect()
        file_list = "[" + ",".join("'" + p + "'" for p in local_files) + "]"
        rel = con.sql(
            f"SELECT * FROM read_parquet({file_list}, union_by_name=true)"
        )

        reader = rel.fetch_record_batch()
        wrote = False
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(batch)
                    wrote = True
        if not wrote:
            raise RuntimeError(
                f"{pkg_id}: union of {len(urls)} parquet(s) was empty"
            )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Thin publish pass: each dataset's raw parquet already carries the source's
# own typed schema, so the transform is a straight projection. Heterogeneous
# per-dataset columns make a generic cast impractical; the raw schema is the
# contract. A 0-row result fails the node by design.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
