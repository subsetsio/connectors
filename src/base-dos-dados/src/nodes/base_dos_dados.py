"""Base dos Dados connector — public one-click-download GCS path.

Mechanism (from research, id 'gcs_one_click'): the anonymous public bucket
`basedosdados-public` holds one gzipped CSV per curated table under
`one-click-download/<gcp_dataset_id>/<gcp_table_id>/<file>.csv.gz`. Each object
is one full table in a single request — the optimal whole-table snapshot shape.

Shape: stateless full re-pull (decision shape 1). Every table is a single small
csv.gz (<=~27MB compressed); we re-fetch the whole object each run and overwrite.
There is no incremental filter on the GCS path and no per-run budget concern, so
no state/watermark logic. Freshness (whether a node runs at all) is the maintain
step's concern, not ours.

Raw format: the gz bytes are saved through verbatim as `<asset>.csv.gz`
(`save_raw_file`). The SQL transform reads it directly — DuckDB's `read_csv_auto`
handles the `.gz` and sniffs the heterogeneous per-table schema, so each subset
is a thin `SELECT *` passthrough (this is a heterogeneous catalog: 238 tables,
238 distinct column lists).
"""

from __future__ import annotations

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_file,
    transient_retry,
)

from constants import GCS_OBJECTS

BUCKET_BASE = "https://storage.googleapis.com/basedosdados-public/"


@transient_retry()  # 6 attempts, exp backoff over transient net errors + 429/5xx
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    """Download one table's public one-click csv.gz and store it verbatim.

    The runtime passes the spec id, which is both the lookup key and the asset
    name. The gz is saved through untouched so the transform sees a real
    `.csv.gz` (DuckDB reads it natively).
    """
    asset = node_id
    obj = GCS_OBJECTS[node_id]  # KeyError here = a spec/constants drift bug
    content = _download(BUCKET_BASE + obj)
    save_raw_file(content, asset, extension="csv.gz")


DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in GCS_OBJECTS
]

# One published Delta table per table. Schemas are heterogeneous and curated
# upstream, so each transform is a straight typed passthrough; the transform
# still acts as the correctness gate (0 rows / unreadable csv fails the node).
TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
