"""DARES (French Ministry of Labour statistics directorate) connector.

Source: the DARES Opendatasoft Explore API v2.1 portal at
data.dares.travail-emploi.gouv.fr. Each catalog dataset is a self-contained,
heterogeneous statistical table; we fetch each one's full parquet export in a
single request and republish it 1:1 as a Delta table.

Shape: stateless full re-pull. The corpus is tiny (~33 datasets, the largest
~2M rows / ~24MB parquet), so every refresh re-fetches each dataset in full and
overwrites — late revisions and rebased series are picked up for free. No
watermark, no cursor, no incremental.
"""
import io

import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)
from constants import ENTITY_IDS

BASE = "https://data.dares.travail-emploi.gouv.fr/api/explore/v2.1"

# spec id -> ODS dataset_id. The harness derives spec ids via
# f"dares-{eid.lower().replace('_','-')}", which is lossy (both '_' and '-' map
# to '-'), and several dataset ids carry native hyphens
# (e.g. dares_defm_communales-brutes), so we keep an explicit reverse map rather
# than trying to invert the transform.
SPEC_TO_DATASET = {
    f"dares-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


def _fetch_parquet(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = SPEC_TO_DATASET[node_id]
    url = f"{BASE}/catalog/datasets/{dataset_id}/exports/parquet"
    content = _fetch_parquet(url)
    table = pq.read_table(io.BytesIO(content))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"dares-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
