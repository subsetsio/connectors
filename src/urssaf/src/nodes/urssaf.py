"""URSSAF open-data connector.

Mechanism: Opendatasoft/Huwise Explore API v2.1 at open.urssaf.fr. Each
accepted catalog dataset is fetched as a complete Parquet export from
/catalog/datasets/{dataset_id}/exports/parquet. The connector is a stateless
full re-pull: each run fetches complete current snapshots so upstream revisions
are naturally reflected in the raw layer.
"""
import io

import pyarrow.parquet as pq

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, raw_parquet_writer

BASE = "https://open.urssaf.fr/api/explore/v2.1"

SPEC_TO_DATASET = {
    f"urssaf-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}
assert len(SPEC_TO_DATASET) == len(ENTITY_IDS), "spec id collision in ENTITY_IDS"


def _fetch_parquet(dataset_id: str) -> bytes:
    url = f"{BASE}/catalog/datasets/{dataset_id}/exports/parquet"
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    dataset_id = SPEC_TO_DATASET[node_id]
    content = _fetch_parquet(dataset_id)
    parquet_file = pq.ParquetFile(io.BytesIO(content))

    with raw_parquet_writer(node_id, parquet_file.schema_arrow) as writer:
        for batch in parquet_file.iter_batches():
            writer.write_batch(batch)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"urssaf-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
