import json

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson


SLUG = "statistics-lithuania"
PREFIX = f"{SLUG}-"
JSON_DATA_BASE = "https://osp-rs.stat.gov.lt/rest_json/data"


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


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(entity_id), fn=fetch_one)
    for entity_id in ENTITY_IDS
]
