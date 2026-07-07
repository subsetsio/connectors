import json
from itertools import product

import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, configure_http, get, post, save_raw_parquet


SLUG = "statistics-slovenia"
PREFIX = f"{SLUG}-"
BASE_URL = "https://pxweb.stat.si/SiStatData/api/v1/en/Data"

RAW_SCHEMA = pa.schema(
    [
        ("table_id", pa.string()),
        ("table_label", pa.string()),
        ("source", pa.string()),
        ("updated", pa.string()),
        ("period", pa.string()),
        ("period_label", pa.string()),
        ("dimension_codes", pa.string()),
        ("dimension_labels", pa.string()),
        ("value", pa.float64()),
        ("value_text", pa.string()),
        ("status", pa.string()),
        ("observation_index", pa.int64()),
    ]
)


def _source_table_id(entity_id: str) -> str:
    return f"{entity_id.upper()}.px"


def _entity_from_node_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(PREFIX) :].lower()


def _all_values_query(metadata: dict) -> dict:
    return {
        "query": [
            {
                "code": variable["code"],
                "selection": {"filter": "all", "values": ["*"]},
            }
            for variable in metadata["variables"]
        ],
        "response": {"format": "JSON-stat"},
    }


def _ordered_category_ids(dimension: dict) -> list[str]:
    index = dimension.get("category", {}).get("index", {})
    return [code for code, _ in sorted(index.items(), key=lambda item: item[1])]


def _value_at(values, index: int):
    if isinstance(values, list):
        return values[index] if index < len(values) else None
    if isinstance(values, dict):
        return values.get(str(index))
    return None


def _status_at(statuses, index: int):
    if isinstance(statuses, list):
        return statuses[index] if index < len(statuses) else None
    if isinstance(statuses, dict):
        return statuses.get(str(index))
    if isinstance(statuses, str):
        return statuses
    return None


def _flatten_jsonstat(table_id: str, dataset: dict) -> list[dict]:
    dim_ids = dataset["dimension"]["id"]
    sizes = dataset["dimension"]["size"]
    dim_codes = [_ordered_category_ids(dataset["dimension"][dim_id]) for dim_id in dim_ids]
    dim_labels = [
        dataset["dimension"][dim_id].get("category", {}).get("label", {})
        for dim_id in dim_ids
    ]
    time_dims = dataset["dimension"].get("role", {}).get("time", [])
    time_dim = time_dims[0] if time_dims else None
    values = dataset.get("value", [])
    statuses = dataset.get("status")

    rows = []
    for obs_index, positions in enumerate(product(*[range(size) for size in sizes])):
        code_map = {}
        label_map = {}
        period = None
        period_label = None
        for dim_id, pos, codes, labels in zip(dim_ids, positions, dim_codes, dim_labels):
            code = codes[pos]
            label = labels.get(code, code)
            code_map[dim_id] = code
            label_map[dim_id] = label
            if dim_id == time_dim:
                period = code
                period_label = label

        raw_value = _value_at(values, obs_index)
        value = raw_value if isinstance(raw_value, (int, float)) else None
        value_text = None if raw_value is None or isinstance(raw_value, (int, float)) else str(raw_value)
        rows.append(
            {
                "table_id": table_id,
                "table_label": dataset.get("label"),
                "source": dataset.get("source"),
                "updated": dataset.get("updated"),
                "period": period,
                "period_label": period_label,
                "dimension_codes": json.dumps(code_map, ensure_ascii=False, sort_keys=True),
                "dimension_labels": json.dumps(label_map, ensure_ascii=False, sort_keys=True),
                "value": value,
                "value_text": value_text,
                "status": _status_at(statuses, obs_index),
                "observation_index": obs_index,
            }
        )
    return rows


def fetch_table(node_id: str) -> None:
    configure_http(timeout=120.0)
    entity_id = _entity_from_node_id(node_id)
    table_id = _source_table_id(entity_id)
    url = f"{BASE_URL}/{table_id}"

    metadata_response = get(url)
    metadata_response.raise_for_status()
    metadata = metadata_response.json()

    data_response = post(url, json=_all_values_query(metadata), timeout=180.0)
    data_response.raise_for_status()
    payload = data_response.json()
    dataset = payload.get("dataset", payload)
    rows = _flatten_jsonstat(table_id, dataset)
    if not rows:
        raise ValueError(f"{node_id}: JSON-stat response produced no rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=RAW_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]
