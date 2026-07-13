import json
from typing import Any

from constants import ENTITY_IDS, LIMIT_BY_ENTITY, PERIOD_PATHS, SPECIAL_PATHS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    load_state,
    raw_asset_exists,
    raw_writer,
    save_state,
)


BASE_URL = "https://apidadosabertos.saude.gov.br"
PREFIX = "datasus-"
DEFAULT_LIMIT = 1000
TIMEOUT = (10.0, 180.0)
RAW_EXT = "ndjson.gz"
PAGINATION_VERSION = 2

ENTITY_BY_SPEC_ID = {
    f"{PREFIX}{entity_id.lower().replace('_', '-')}": entity_id
    for entity_id in ENTITY_IDS
}


def _paths_for(entity_id: str) -> list[str]:
    paths = PERIOD_PATHS.get(entity_id)
    if paths:
        return paths
    return [SPECIAL_PATHS.get(entity_id, f"/{entity_id}")]


def _records_from_response(payload: Any, path: str) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ValueError(f"{path} returned {type(payload).__name__}, expected JSON object")

    list_keys = [key for key, value in payload.items() if isinstance(value, list)]
    if len(list_keys) != 1:
        raise ValueError(f"{path} returned {len(list_keys)} list fields, expected exactly one")

    rows = payload[list_keys[0]]
    records: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            records.append(row)
        else:
            records.append({"value": row})
    return records


def fetch_one(spec_id: str) -> None:
    entity_id = ENTITY_BY_SPEC_ID[spec_id]
    limit = LIMIT_BY_ENTITY.get(entity_id, DEFAULT_LIMIT)
    total = 0

    with raw_writer(spec_id, RAW_EXT, mode="wt", compression="gzip") as out:
        for path in _paths_for(entity_id):
            offset = 0
            while True:
                response = get(
                    f"{BASE_URL}{path}",
                    params={"limit": limit, "offset": offset},
                    timeout=TIMEOUT,
                )
                response.raise_for_status()
                records = _records_from_response(response.json(), path)

                for record in records:
                    enriched = dict(record)
                    enriched["_datasus_entity_id"] = entity_id
                    enriched["_datasus_path"] = path
                    out.write(json.dumps(enriched, ensure_ascii=False, separators=(",", ":")))
                    out.write("\n")

                total += len(records)
                if len(records) < limit:
                    break
                offset += len(records)

    save_state(spec_id, {"pagination_version": PAGINATION_VERSION})
    print(f"  -> Fetched {total:,} rows for {spec_id}")


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one)
    for spec_id in sorted(ENTITY_BY_SPEC_ID)
]


def _fresh_enough(spec_id: str) -> bool:
    state = load_state(spec_id)
    return (
        state.get("pagination_version") == PAGINATION_VERSION
        and raw_asset_exists(spec_id, RAW_EXT, max_age_days=30)
    )


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec_id,
        description=(
            "DEMAS API has no incremental cursor or validators; refresh full "
            "endpoint at least every 30 days (inferred from open-data API behavior)."
        ),
        check=_fresh_enough,
    )
    for spec_id in sorted(ENTITY_BY_SPEC_ID)
]
