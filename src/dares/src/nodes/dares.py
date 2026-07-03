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
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
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


@transient_retry()  # 6 attempts, exponential backoff; retries 429/5xx/transport
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

# Datasets whose published table carries a `date` observation-period column
# (every dataset except dares-jint-depuis2005, whose source ships a single
# merged column). Keys are left undeclared: these are heterogeneous SELECT *
# pass-throughs of long panels with per-dataset grains, none proven unique.
_TEMPORAL_DATE = frozenset({
    "dares-dares-defm-age-detaille-mens",
    "dares-dares-defm-age-detaille-trim",
    "dares-dares-defm-communales-brutes",
    "dares-dares-defm-entrees-stage-formation-mens",
    "dares-dares-defm-entrees-stages-formation-trim",
    "dares-dares-defm-flux-france-region-brut-mens",
    "dares-dares-defm-flux-france-region-brut-trim",
    "dares-dares-defm-flux-france-region-cvs-mens",
    "dares-dares-defm-flux-france-region-cvs-trim",
    "dares-dares-defm-stock-france-brut-mens",
    "dares-dares-defm-stock-france-brut-trim",
    "dares-dares-defm-stock-france-cvs",
    "dares-dares-defm-stock-france-cvs-trim",
    "dares-dares-defm-stock-region-cvs-trim",
    "dares-dares-defm-stock-regions-brut-mens",
    "dares-dares-defm-stock-regions-brut-trim",
    "dares-dares-defm-stock-regions-cvs-cjo-mens",
    "dares-dares-defm-zone-emploi-mens",
    "dares-dares-defm-zoneeemploi-brut-trim",
    "dares-dares-emploivacants-brut-emploisoccupes",
    "dares-dares-emploivacants-brut-emploisvacants",
    "dares-dares-emploivacants-cvs-emploisoccupes",
    "dares-dares-emploivacants-cvs-emploisvacants",
    "dares-dares-emploivacants-cvs-typevacance",
    "dares-dares-jint-1975-2004",
    "dares-dares-offres-collectees-satisfaites-france-travail-brutes-mens",
    "dares-dares-offres-collectees-satisfaites-france-travail-brutes-trim",
    "dares-dares-offres-collectees-satisfaites-france-travail-cvs-cjo-mens",
    "dares-dares-offres-collectees-satisfaites-france-travail-cvs-cjo-trim",
    "dares-dares-tempspartiel-annuelles",
    "dares-dares-tempspartiel-detail-annuelles",
})

# One published Delta table per dataset. The ODS parquet export is already a
# clean, typed table, so each transform is a straight pass-through republish;
# heterogeneous per-dataset schemas rule out any shared projection. A 0-row
# result fails the node, which is the empty-payload guard we want.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        temporal="date" if s.id in _TEMPORAL_DATE else None,
    )
    for s in DOWNLOAD_SPECS
]
