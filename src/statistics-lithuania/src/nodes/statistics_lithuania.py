import json
import os
import time
from datetime import datetime

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, list_raw_fragments, load_state, save_raw_ndjson, save_state


SLUG = "statistics-lithuania"
PREFIX = f"{SLUG}-"
JSON_DATA_BASE = "https://osp-rs.stat.gov.lt/rest_json/data"
NDJSON_EXT = "ndjson.zst"
WINDOW_START_YEAR = 1990
WINDOW_END_YEAR = datetime.utcnow().year + 1
WINDOW_NODE_BUDGET_S = 45

WINDOWED_FLOW_IDS = {
    "S1R042_M8020431",
    "S1R058_M8010705",
    "S3R0256_M3010103",
    "S3R143_M3110113_1",
    "S3R143_M3110123",
    "S3R147_M3150610_1",
    "S3R147_M3150610_2",
    "S3R147_M3150610_3",
    "S3R147_M3150610_4",
    "S3R147_M3150610_5",
    "S3R147_M3150611",
    "S3R149_M3150605",
    "S3R149_M3150605_2",
    "S3R149_M3150605_3",
    "S3R167_M3010319",
}


def _spec_id(entity_id: str) -> str:
    return f"{PREFIX}{entity_id.lower().replace('_', '-')}"


def _entity_id_from_spec(asset_id: str) -> str:
    if not asset_id.startswith(PREFIX):
        raise ValueError(f"unexpected asset id {asset_id!r}")
    return asset_id.removeprefix(PREFIX).replace("-", "_").upper()


def _value_lookup(values):
    out = []
    for value in values or []:
        out.append(
            {
                "id": value.get("id"),
                "name": value.get("name"),
            }
        )
    return out


def _attribute_values(attribute_defs, indexes):
    attrs = {}
    for pos, idx in enumerate(indexes or []):
        if idx is None or pos >= len(attribute_defs):
            continue
        definition = attribute_defs[pos]
        values = definition.get("values") or []
        if idx >= len(values):
            continue
        value = values[idx]
        attr_id = definition.get("id") or f"attr_{pos}"
        attrs[attr_id] = {
            "id": value.get("id"),
            "name": value.get("name"),
        }
    return attrs


def _rows_from_sdmx_json(flow_id: str, payload: dict):
    structure = payload.get("structure") or {}
    dimensions = ((structure.get("dimensions") or {}).get("observation")) or []
    attributes = ((structure.get("attributes") or {}).get("observation")) or []
    data_sets = payload.get("dataSets") or []
    source_name = structure.get("name")
    source_description = structure.get("description")

    for data_set in data_sets:
        observations = data_set.get("observations") or {}
        for obs_key, obs_values in observations.items():
            key_parts = [int(part) for part in obs_key.split(":") if part != ""]
            dim_codes = {}
            dim_labels = {}
            period = None

            for pos, value_idx in enumerate(key_parts):
                if pos >= len(dimensions):
                    continue
                dim = dimensions[pos]
                dim_id = dim.get("id") or f"dim_{pos}"
                values = _value_lookup(dim.get("values"))
                dim_value = values[value_idx] if value_idx < len(values) else {}
                dim_codes[dim_id] = dim_value.get("id")
                dim_labels[dim_id] = dim_value.get("name")
                if dim_id.upper() in {"LAIKOTARPIS", "TIME_PERIOD", "TIME"}:
                    period = dim_value.get("id") or dim_value.get("name")

            yield {
                "flow_id": flow_id,
                "observation_key": obs_key,
                "period": period,
                "value": obs_values[0] if obs_values else None,
                "dimension_codes": dim_codes,
                "dimension_labels": dim_labels,
                "attributes": _attribute_values(attributes, obs_values[1:]),
                "source_name": source_name,
                "source_description": source_description,
                "dataset_action": data_set.get("action"),
            }


def fetch_one(asset_id: str) -> None:
    flow_id = _entity_id_from_spec(asset_id)
    if flow_id in WINDOWED_FLOW_IDS:
        return _fetch_one_windowed(asset_id, flow_id)

    url = f"{JSON_DATA_BASE}/{flow_id}"
    response = get(
        url,
        headers={"Accept": "application/vnd.sdmx.data+json, application/json"},
        timeout=(10.0, 180.0),
    )
    response.raise_for_status()
    payload = response.json()
    rows = list(_rows_from_sdmx_json(flow_id, payload))
    if not rows:
        raise ValueError(f"{flow_id}: SDMX response contained no observations")
    save_raw_ndjson(rows, asset_id)


def _fetch_one_windowed(asset_id: str, flow_id: str) -> bool | None:
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        fragment
        for fragment, meta in list_raw_fragments(asset_id, NDJSON_EXT).items()
        if meta.get("run_id") == run_id
    }
    years = [str(year) for year in range(WINDOW_START_YEAR, WINDOW_END_YEAR + 1)]
    remaining = [year for year in years if year not in done]
    if not remaining:
        return None

    state = load_state(asset_id)
    if state.get("run_id") != run_id:
        state = {"run_id": run_id, "windowed_row_count": 0}

    deadline = time.monotonic() + WINDOW_NODE_BUDGET_S
    for year in remaining:
        if time.monotonic() >= deadline:
            return True

        url = f"{JSON_DATA_BASE}/{flow_id}"
        response = get(
            url,
            params={"startPeriod": year, "endPeriod": year},
            headers={"Accept": "application/vnd.sdmx.data+json, application/json"},
            timeout=(10.0, 120.0),
        )
        response.raise_for_status()
        rows = list(_rows_from_sdmx_json(flow_id, response.json()))
        if rows:
            state["windowed_row_count"] = int(state.get("windowed_row_count") or 0) + len(rows)
            save_state(asset_id, state)
        save_raw_ndjson(rows, asset_id, fragment=year)

    if int(state.get("windowed_row_count") or 0) == 0:
        raise ValueError(f"{flow_id}: SDMX period windows contained no observations")
    return None


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(entity_id), fn=fetch_one)
    for entity_id in ENTITY_IDS
]
