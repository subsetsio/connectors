"""Statistics Sweden PxWebApi v2 download nodes."""
from __future__ import annotations

import json
from itertools import product

from subsets_utils import MaintainSpec, NodeSpec, get, post, raw_asset_exists, raw_writer

from constants import ENTITY_IDS

BASE_URL = "https://statistikdatabasen.scb.se/api/v2"
PREFIX = "statistics-sweden-"
MAX_CELLS_PER_REQUEST = 100_000


def _table_id_from_asset(asset_id: str) -> str:
    return asset_id.removeprefix(PREFIX).upper()


def _fetch_json(path: str, params: dict | None = None) -> dict:
    resp = get(f"{BASE_URL}{path}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _post_json(path: str, body: dict, params: dict | None = None) -> dict:
    resp = post(f"{BASE_URL}{path}", json=body, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _codes_for_dimension(dim: dict) -> list[str]:
    index = dim.get("category", {}).get("index", {})
    return [code for code, _pos in sorted(index.items(), key=lambda item: item[1])]


def _product_size(selection: dict[str, list[str]]) -> int:
    total = 1
    for codes in selection.values():
        total *= len(codes)
    return total


def _split_selection(selection: dict[str, list[str]], max_cells: int) -> list[dict[str, list[str]]]:
    if _product_size(selection) <= max_cells:
        return [selection]

    dim = max(selection, key=lambda key: len(selection[key]))
    codes = selection[dim]
    other_size = max(1, _product_size(selection) // max(1, len(codes)))
    chunk_size = max(1, max_cells // other_size)

    chunks: list[dict[str, list[str]]] = []
    for start in range(0, len(codes), chunk_size):
        chunk = {key: list(value) for key, value in selection.items()}
        chunk[dim] = codes[start : start + chunk_size]
        chunks.extend(_split_selection(chunk, max_cells))
    return chunks


def _period_start(period: str | None) -> str | None:
    if not period:
        return None
    text = str(period)
    year = text[:4]
    if not year.isdigit():
        return None
    if "M" in text:
        month = text.split("M", 1)[1][:2]
        if month.isdigit():
            return f"{year}-{int(month):02d}-01"
    if "K" in text:
        quarter = text.split("K", 1)[1][:1]
        if quarter.isdigit() and 1 <= int(quarter) <= 4:
            month = (int(quarter) - 1) * 3 + 1
            return f"{year}-{month:02d}-01"
    return f"{year}-01-01"


def _value_at(values, offset: int):
    if isinstance(values, dict):
        return values.get(str(offset))
    if isinstance(values, list) and offset < len(values):
        return values[offset]
    return None


def _selection_body(selection: dict[str, list[str]]) -> dict:
    return {
        "selection": [
            {"variableCode": dim_name, "valueCodes": codes}
            for dim_name, codes in selection.items()
        ]
    }


def _flatten_dataset(table_id: str, dataset: dict):
    ids = dataset["id"]
    sizes = dataset["size"]
    dims = dataset["dimension"]
    strides = []
    for idx in range(len(sizes)):
        stride = 1
        for size in sizes[idx + 1 :]:
            stride *= size
        strides.append(stride)

    code_lists = [_codes_for_dimension(dims[dim]) for dim in ids]
    values = dataset.get("value", [])
    statuses = dataset.get("status") or {}
    time_dims = set((dataset.get("role") or {}).get("time") or [])
    metric_dims = set((dataset.get("role") or {}).get("metric") or [])

    for positions in product(*[range(len(codes)) for codes in code_lists]):
        offset = sum(pos * stride for pos, stride in zip(positions, strides))
        row = {
            "table_id": table_id,
            "table_label": dataset.get("label"),
            "source": dataset.get("source"),
            "updated": dataset.get("updated"),
            "value": _value_at(values, offset),
            "status": statuses.get(str(offset)) if isinstance(statuses, dict) else None,
        }
        for dim_name, codes, pos in zip(ids, code_lists, positions):
            dim = dims[dim_name]
            code = codes[pos]
            category = dim.get("category", {})
            unit = (category.get("unit") or {}).get(code) or {}
            role = "time" if dim_name in time_dims else "metric" if dim_name in metric_dims else "dimension"
            row[f"{dim_name}_code"] = code
            row[f"{dim_name}_label"] = (category.get("label") or {}).get(code)
            row[f"{dim_name}_role"] = role
            if dim_name in time_dims:
                row["period"] = code
                row["period_start"] = _period_start(code)
            if unit:
                row["unit"] = unit.get("base")
                row["decimals"] = unit.get("decimals")
        yield row


def fetch_table(asset_id: str) -> None:
    table_id = _table_id_from_asset(asset_id)
    metadata = _fetch_json(f"/tables/{table_id}/metadata", {"lang": "en"})
    selection = {
        dim_name: _codes_for_dimension(metadata["dimension"][dim_name])
        for dim_name in metadata["id"]
    }

    row_count = 0
    chunks = _split_selection(selection, MAX_CELLS_PER_REQUEST)
    with raw_writer(asset_id, "ndjson", compression="gzip", mode="wt") as out:
        for chunk in chunks:
            dataset = _post_json(
                f"/tables/{table_id}/data",
                _selection_body(chunk),
                {"lang": "en", "outputFormat": "json-stat2"},
            )
            for row in _flatten_dataset(table_id, dataset):
                out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                row_count += 1

    if row_count == 0:
        raise RuntimeError(f"{asset_id}: fetched zero rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower()}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "SCB Statistical Database updates on table-specific schedules; "
            "re-fetch at least every 30 days per connector maintenance cadence "
            "and SCB database update guidance."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.gz", max_age_days=30),
    )
    for spec in DOWNLOAD_SPECS
]
