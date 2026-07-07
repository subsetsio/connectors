"""SDES DiDo connector.

One download node per rank-accepted DiDo datafile. DiDo datafiles are
heterogeneous tabular exports, so the raw stage preserves the source CSV bytes
instead of forcing type inference in Python. The transform stage profiles each
CSV and authors explicit typed SQL per table.
"""

from constants import ENTITY_IDS, ENTITY_MILLESIMES
from subsets_utils import NodeSpec, get, record_source_signature, save_raw_file

BASE = "https://data.statistiques.developpement-durable.gouv.fr/dido/api/v1"
PREFIX = "sdes-"

SPEC_TO_RID = {f"{PREFIX}{rid.lower().replace('_', '-')}": rid for rid in ENTITY_IDS}
assert len(SPEC_TO_RID) == len(ENTITY_IDS), "spec id collision in ENTITY_IDS"


def fetch_one(node_id: str) -> None:
    rid = SPEC_TO_RID[node_id]
    millesime = ENTITY_MILLESIMES[rid]
    url = f"{BASE}/datafiles/{rid}/csv"
    resp = get(url, params={"millesime": millesime}, timeout=(10.0, 900.0))
    resp.raise_for_status()
    save_raw_file(resp.content, node_id, extension="csv")
    record_source_signature(node_id, str(resp.url), response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{rid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for rid in ENTITY_IDS
]
