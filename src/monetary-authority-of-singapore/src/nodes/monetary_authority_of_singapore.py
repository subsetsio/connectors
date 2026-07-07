"""Monetary Authority of Singapore datasets mirrored on data.gov.sg."""

import time

from subsets_utils import NodeSpec, get, save_raw_ndjson

BASE_URL = "https://data.gov.sg/api/action/datastore_search"
SPEC_PREFIX = "monetary-authority-of-singapore-"

ENTITY_IDS = [
    "d_0239d0d67315994c63a04e6f7bdc08cc",
    "d_046ff8d521a218d9178178cfbfc45c2c",
    "d_2d2ca1bcac71713d2c02deca871ebe98",
    "d_6cb7c12d5f25f0a04e70657dfebcb514",
    "d_7762c172b186ae213d02089bc1e247ee",
    "d_7a747bbf23166674020989ce7af0e72e",
    "d_a103140a9fc430ab3d3e3598ecd8109f",
    "d_bb14bb541fc1e60b29fa021ffa462429",
    "d_c2e116320c9d36f6ea6cdd82fb763de2",
]


def _spec_id(entity_id: str) -> str:
    return f"{SPEC_PREFIX}{entity_id.lower().replace('_', '-')}"


def _entity_id_from_spec_id(node_id: str) -> str:
    if not node_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected spec id: {node_id}")
    return node_id.removeprefix(SPEC_PREFIX).replace("-", "_")


def _stagger_seconds(entity_id: str) -> float:
    return (ENTITY_IDS.index(entity_id) % 9) * 0.75


def fetch_dataset(node_id: str) -> None:
    entity_id = _entity_id_from_spec_id(node_id)
    if entity_id not in ENTITY_IDS:
        raise ValueError(f"unsupported entity id: {entity_id}")

    time.sleep(_stagger_seconds(entity_id))

    limit = 5000
    offset = 0
    rows = []
    total = None

    while total is None or offset < total:
        resp = get(
            BASE_URL,
            params={"resource_id": entity_id, "limit": limit, "offset": offset},
            timeout=(10.0, 120.0),
        )
        resp.raise_for_status()
        result = resp.json()["result"]
        total = int(result.get("total") or 0)
        batch = result.get("records") or []
        rows.extend({"source_resource_id": entity_id, **record} for record in batch)
        if not batch:
            break
        offset += len(batch)

    if not rows:
        raise AssertionError(f"{entity_id}: datastore_search returned no rows")

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(entity_id), fn=fetch_dataset, kind="download")
    for entity_id in ENTITY_IDS
]
