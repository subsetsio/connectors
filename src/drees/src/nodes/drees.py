"""DREES (Direction de la recherche, des etudes, de l'evaluation et des
statistiques) — French health & social-affairs statistics.

Mechanism: Opendatasoft Explore API v2.1 at
https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1. Each rank-accepted
dataset is fetched in full from its stable per-entity parquet export
(/catalog/datasets/{dataset_id}/exports/parquet), which streams the entire table
in one request — no auth, no pagination. Fetch shape is the default stateless
full re-pull: every run overwrites each raw asset with a complete snapshot, so
DREES's annual revisions are picked up for free. The corpus is ~47 datasets,
each a few rows to ~1.2M; the whole pull is minutes and cents.

Each subset's transform is a straight typed passthrough — the ODS parquet export
already carries clean snake_case columns and proper types, so there is no shared
schema across the heterogeneous portal to normalise to.
"""
import io

import pyarrow.parquet as pq

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

BASE = "https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1"

# spec.id is f"drees-{eid.lower().replace('_','-')}", which is NOT reversible
# back to the upstream dataset_id (case + underscores are lost). Keep the exact
# mapping so fetch_one can rebuild the export URL from the node id it's handed.
SPEC_TO_DATASET = {
    f"drees-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}
assert len(SPEC_TO_DATASET) == len(ENTITY_IDS), "spec id collision in ENTITY_IDS"


@transient_retry()  # 6 attempts, exponential 4..120s backoff, reraise on exhaust
def _fetch_parquet(dataset_id: str) -> bytes:
    url = f"{BASE}/catalog/datasets/{dataset_id}/exports/parquet"
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()  # inside the retry so 5xx/429 are retried
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = SPEC_TO_DATASET[node_id]
    content = _fetch_parquet(dataset_id)
    table = pq.read_table(io.BytesIO(content))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"drees-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. The ODS parquet already has clean types
# and column names, so the transform is a passthrough that simply re-publishes
# the snapshot (and acts as the 0-rows correctness gate).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
