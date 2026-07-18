import csv
import io
import json
import re
from itertools import product

import httpx
import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import (
    TRANSIENT_EXC,
    MaintainSpec,
    NodeSpec,
    configure_http,
    delete_raw_file,
    get,
    post,
    raw_asset_exists,
    save_raw_file,
    save_raw_parquet,
)


SLUG = "statistics-slovenia"
PREFIX = f"{SLUG}-"
BASE_URL = "https://pxweb.stat.si/SiStatData/api/v1/en/Data"
MAINTAIN_MAX_AGE_DAYS = 7
MAX_CELLS_PER_REQUEST = 750_000

# SURS's JSON-stat serializer stalls server-side on some large tables (0701060S:
# every JSON-stat query, down to a single cell, is dropped after ~60s), while the
# same selection in csv3 returns in seconds. csv3 is the fallback: long format,
# one row per observation, dimension CODES in the metadata's variable order and
# the value in the last column. It carries no dataset-level label/source/updated
# and no status markers, so it is a fallback, not the default. Its cells are
# cheaper server-side, hence the larger per-request budget.
CSV3_MAX_CELLS_PER_REQUEST = 1_500_000
COMPLETE_EXT = "complete.json"
PERIOD_RE = re.compile(r"^\d{4}([A-Z]\d{1,2})?$")
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


def _chunk_specs(metadata: dict, max_cells: int) -> list[tuple[str, str | None, list[str]]]:
    """Split a table into `(label, chunk_code, chunk_values)` requests along its
    widest variable, so no single request exceeds `max_cells`. `chunk_code` is
    None for a table that fits in one request (label "full")."""
    variables = metadata["variables"]
    sizes = [max(1, len(_variable_values(variable))) for variable in variables]
    total_cells = 1
    for size in sizes:
        total_cells *= size
    if total_cells <= max_cells:
        return [("full", None, [])]

    chunk_index = max(range(len(variables)), key=lambda index: sizes[index])
    chunk_variable = variables[chunk_index]
    chunk_code = chunk_variable["code"]
    other_cells = max(1, total_cells // sizes[chunk_index])
    chunk_size = max(1, max_cells // other_cells)
    values = _variable_values(chunk_variable)

    chunks = []
    for start in range(0, len(values), chunk_size):
        stop = min(start + chunk_size, len(values))
        label = f"chunk-{chunk_index:02d}-{start:05d}-{stop - 1:05d}"
        chunks.append((label, chunk_code, values[start:stop]))
    return chunks


def _chunked_queries(metadata: dict) -> list[tuple[str | None, dict]]:
    return [
        (
            label,
            _all_values_query(metadata)
            if chunk_code is None
            else _selection_query(metadata, chunk_code, chunk_values),
        )
        for label, chunk_code, chunk_values in _chunk_specs(metadata, MAX_CELLS_PER_REQUEST)
    ]


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


def _time_variable_code(metadata: dict) -> str | None:
    """The period variable, by shape of its values (2024, 2024M03, 2024Q1) —
    the metadata endpoint carries no time role, only JSON-stat does."""
    for variable in metadata["variables"]:
        values = _variable_values(variable)
        if values and all(PERIOD_RE.match(value) for value in values):
            return variable["code"]
    return None


def _flatten_csv3(table_id: str, metadata: dict, text: str) -> list[dict]:
    variables = metadata["variables"]
    codes = [variable["code"] for variable in variables]
    label_maps = [
        dict(zip(_variable_values(v), [str(t) for t in v.get("valueTexts", [])]))
        for v in variables
    ]
    time_code = _time_variable_code(metadata)
    table_label = metadata.get("title")

    rows = []
    reader = csv.reader(io.StringIO(text))
    next(reader, None)  # header: dimension columns then the value column
    for obs_index, record in enumerate(reader):
        if len(record) < len(codes) + 1:
            continue
        cells = [cell.strip() for cell in record[: len(codes)]]
        raw_value = record[len(codes)].strip()
        if not raw_value:
            continue
        code_map = dict(zip(codes, cells))
        label_map = {
            code: label_maps[index].get(cells[index], cells[index])
            for index, code in enumerate(codes)
        }
        try:
            value = float(raw_value)
            value_text = None
        except ValueError:
            value = None
            value_text = raw_value
        period = code_map.get(time_code) if time_code else None
        rows.append(
            {
                "table_id": table_id,
                "table_label": table_label,
                "source": None,
                "updated": None,
                "period": period,
                "period_label": label_map.get(time_code) if time_code else None,
                "dimension_codes": json.dumps(code_map, ensure_ascii=False, sort_keys=True),
                "dimension_labels": json.dumps(label_map, ensure_ascii=False, sort_keys=True),
                "value": value,
                "value_text": value_text,
                "status": None,
                "observation_index": obs_index,
            }
        )
    return rows


def _fetch_jsonstat(node_id: str, url: str, table_id: str, metadata: dict) -> int:
    chunks = _chunked_queries(metadata)
    if len(chunks) > 1:
        delete_raw_file(node_id, "parquet")
    delete_raw_file(node_id, COMPLETE_EXT)

    wrote_rows = 0
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
    return wrote_rows


def _fetch_csv3(node_id: str, url: str, table_id: str, metadata: dict) -> int:
    delete_raw_file(node_id, "parquet")  # drop whatever the JSON-stat leg wrote
    delete_raw_file(node_id, COMPLETE_EXT)
    wrote_rows = 0
    for chunk_label, chunk_code, chunk_values in _chunk_specs(
        metadata, CSV3_MAX_CELLS_PER_REQUEST
    ):
        query = (
            _all_values_query(metadata)
            if chunk_code is None
            else _selection_query(metadata, chunk_code, chunk_values)
        )
        query["response"] = {"format": "csv3"}
        data_response = post(url, json=query, timeout=300.0)
        data_response.raise_for_status()
        rows = _flatten_csv3(table_id, metadata, data_response.text)
        if not rows:
            continue
        fragment = None if chunk_label == "full" else chunk_label
        save_raw_parquet(pa.Table.from_pylist(rows, schema=RAW_SCHEMA), node_id, fragment=fragment)
        wrote_rows += len(rows)
    return wrote_rows


def _is_server_side(exc: Exception) -> bool:
    if isinstance(exc, TRANSIENT_EXC):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code >= 500


def fetch_table(node_id: str) -> None:
    configure_http(timeout=120.0)
    entity_id = _entity_from_node_id(node_id)
    table_id = _source_table_id(entity_id)
    url = f"{BASE_URL}/{table_id}"

    metadata_response = get(url)
    metadata_response.raise_for_status()
    metadata = metadata_response.json()

    try:
        wrote_rows = _fetch_jsonstat(node_id, url, table_id, metadata)
    except Exception as exc:
        if not _is_server_side(exc):
            raise
        print(
            f"[{node_id}] JSON-stat leg failed ({type(exc).__name__}: {exc}) — "
            f"refetching the whole table as csv3"
        )
        wrote_rows = _fetch_csv3(node_id, url, table_id, metadata)

    if not wrote_rows:
        raise ValueError(f"{node_id}: response produced no rows")
    save_raw_file(
        json.dumps({"table_id": table_id, "rows": wrote_rows}, sort_keys=True),
        node_id,
        COMPLETE_EXT,
    )


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id.replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]


def _is_fresh(asset_id: str) -> bool:
    return raw_asset_exists(asset_id, COMPLETE_EXT, max_age_days=MAINTAIN_MAX_AGE_DAYS)


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=MAINTAIN_DESCRIPTION,
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
