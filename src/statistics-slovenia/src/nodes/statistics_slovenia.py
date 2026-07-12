import json
from itertools import product

import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    configure_http,
    delete_raw_file,
    get,
    post,
    raw_asset_exists,
    save_raw_parquet,
)


SLUG = "statistics-slovenia"
PREFIX = f"{SLUG}-"
BASE_URL = "https://pxweb.stat.si/SiStatData/api/v1/en/Data"
MAINTAIN_MAX_AGE_DAYS = 7
MAX_CELLS_PER_REQUEST = 75_000
MAINTAIN_DESCRIPTION = (
    f"Full re-pull when raw is older than {MAINTAIN_MAX_AGE_DAYS}d. SURS PxWeb "
    "does not expose a table-level since/modifiedAfter query parameter, so due "
    "refreshes re-fetch whole tables; the window also lets continuation legs "
    "skip raw committed earlier in the same run. Release calendar: "
    "https://www.stat.si/StatWeb/en/ReleaseCal"
)

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
    spec_entity_id = node_id[len(PREFIX) :].lower()
    if spec_entity_id == "aa-synonims":
        return "aa_synonims"
    return spec_entity_id


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


def _variable_values(variable: dict) -> list[str]:
    return [str(value) for value in variable.get("values", [])]


def _selection_query(metadata: dict, chunk_code: str | None, chunk_values: list[str]) -> dict:
    query = []
    for variable in metadata["variables"]:
        code = variable["code"]
        if code == chunk_code:
            selection = {"filter": "item", "values": chunk_values}
        else:
            selection = {"filter": "all", "values": ["*"]}
        query.append({"code": code, "selection": selection})
    return {"query": query, "response": {"format": "JSON-stat"}}


def _chunked_queries(metadata: dict) -> list[tuple[str | None, dict]]:
    variables = metadata["variables"]
    sizes = [max(1, len(_variable_values(variable))) for variable in variables]
    total_cells = 1
    for size in sizes:
        total_cells *= size
    if total_cells <= MAX_CELLS_PER_REQUEST:
        return [("full", _all_values_query(metadata))]

    chunk_index = max(range(len(variables)), key=lambda index: sizes[index])
    chunk_variable = variables[chunk_index]
    chunk_code = chunk_variable["code"]
    other_cells = max(1, total_cells // sizes[chunk_index])
    chunk_size = max(1, MAX_CELLS_PER_REQUEST // other_cells)
    values = _variable_values(chunk_variable)

    chunks = []
    for start in range(0, len(values), chunk_size):
        stop = min(start + chunk_size, len(values))
        label = f"chunk-{chunk_index:02d}-{start:05d}-{stop - 1:05d}"
        chunks.append((label, _selection_query(metadata, chunk_code, values[start:stop])))
    return chunks


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
        status = _status_at(statuses, obs_index)
        if raw_value is None and status is None:
            continue
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
                "status": status,
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

    chunks = _chunked_queries(metadata)
    wrote_rows = 0
    if len(chunks) > 1:
        delete_raw_file(node_id, "parquet")

    for chunk_label, query in chunks:
        data_response = post(url, json=query, timeout=180.0)
        data_response.raise_for_status()
        payload = data_response.json()
        dataset = payload.get("dataset", payload)
        rows = _flatten_jsonstat(table_id, dataset)
        if not rows:
            continue
        fragment = None if chunk_label == "full" else chunk_label
        save_raw_parquet(pa.Table.from_pylist(rows, schema=RAW_SCHEMA), node_id, fragment=fragment)
        wrote_rows += len(rows)

    if not wrote_rows:
        raise ValueError(f"{node_id}: JSON-stat response produced no rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id.replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]


def _is_fresh(asset_id: str) -> bool:
    return raw_asset_exists(asset_id, "parquet", max_age_days=MAINTAIN_MAX_AGE_DAYS)


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=MAINTAIN_DESCRIPTION,
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
