"""ONS (Brazil grid) open-data connector.

Source: the ONS CKAN portal at https://dados.ons.org.br (mechanism `ckan`,
anonymous). Each rank-accepted package is one publishable dataset. A package's
resources are direct-download files on the public S3 bucket
`ons-aws-prod-opendata`, shipped as one CSV + one XLSX + one Parquet per year
(plus PDF/JSON data dictionaries we ignore). We pull the Parquet variant of
every data resource and union the years into one raw asset per dataset.

Shape: stateless full re-pull (shape 1). The yearly Parquet files are small
(tens of KB each; whole datasets are at most tens of MB), so re-fetching the
full corpus each refresh is cheap and picks up the source's recurring
revisions for free. No incremental filter exists on CKAN package data.
"""

import io

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
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
def _package_show(pkg_id: str) -> list[dict]:
    resp = get(
        f"{CKAN_BASE}/package_show",
        params={"id": pkg_id},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"package_show {pkg_id}: success=false")
    return body["result"]["resources"]


@transient_retry()
def _download_parquet(url: str) -> pa.Table:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return pq.read_table(io.BytesIO(resp.content))


def fetch_one(node_id: str) -> None:
    """Pull every Parquet resource of one CKAN package and union the years
    into a single raw parquet asset named after the spec id."""
    asset = node_id
    pkg_id = SPEC_TO_PKG[node_id]

    resources = _package_show(pkg_id)
    parquet_urls = [
        r["url"]
        for r in resources
        if (r.get("format") or "").upper() == "PARQUET" and r.get("url")
    ]
    if not parquet_urls:
        # Every rank-accepted package advertised a PARQUET variant at collect
        # time; none here means the source changed shape — fail loudly.
        raise RuntimeError(f"{pkg_id}: no PARQUET resources found")

    tables = [_download_parquet(url) for url in parquet_urls]
    combined = pa.concat_tables(tables, promote_options="permissive")
    save_raw_parquet(combined, asset)


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
