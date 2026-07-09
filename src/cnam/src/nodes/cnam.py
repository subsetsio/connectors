"""CNAM (Caisse nationale de l'Assurance Maladie) — data.ameli.fr connector.

Mechanism: Opendatasoft (ODS) Explore API v2.1 (chosen mechanism `ods_explore_v21`).
Each rank-active dataset is pulled WHOLE via the per-dataset bulk export endpoint
`/api/explore/v2.1/catalog/datasets/{dataset_id}/exports/parquet`, which returns the
entire dataset as one typed parquet file (no pagination). No auth, no documented rate
limit. These are annual/periodic snapshot series with no incremental query for export,
so the shape is a STATELESS FULL RE-PULL each refresh (overwrite) — revisions and
back-corrections are picked up for free. The parquet is streamed row-group by row-group
into the raw layer so multi-million-row datasets (e.g. `effectifs` ~5.2M rows) stay
within bounded memory.

Transform: one thin SQL pass-through per dataset publishing the export verbatim. Each
ODS dataset has its own (flat, scalar-typed: text/int/double/date) column schema, so
there is no cross-dataset normalization to do here — `SELECT *` republishes the typed
export as the Delta table.
"""
import io

import pyarrow.parquet as pq

from subsets_utils import NodeSpec, get, raw_parquet_writer
from constants import ENTITY_IDS

BASE = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"


def _download_export(url: str) -> bytes:
    # ODS bulk export: the full dataset in one parquet payload, no pagination.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = node_id[len("cnam-"):]  # recover the ODS dataset_id
    url = f"{BASE}/{dataset_id}/exports/parquet"

    raw = _download_export(url)
    pf = pq.ParquetFile(io.BytesIO(raw))
    schema = pf.schema_arrow

    # Stream row groups straight to the raw layer — bounded memory for the
    # large datasets, and the export schema is the contract for every batch.
    with raw_parquet_writer(asset, schema) as writer:
        for batch in pf.iter_batches():
            writer.write_batch(batch)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cnam-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
