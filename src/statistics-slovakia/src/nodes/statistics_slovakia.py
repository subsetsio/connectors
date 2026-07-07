import itertools
import json
import math
from functools import lru_cache

import pyarrow as pa
from subsets_utils import NodeSpec, configure_http, get, save_raw_parquet

from constants import ENTITY_IDS


BASE_URL = "https://data.statistics.sk/api/v2"
SLUG = "statistics-slovakia"
MAX_CELLS = 9000
MAX_URL_LEN = 1800

RAW_SCHEMA = pa.schema(
    [
        pa.field("table_code", pa.string()),
        pa.field("table_label", pa.string()),
        pa.field("source_updated", pa.string()),
        pa.field("row_index", pa.int64()),
        pa.field("slice_id", pa.string()),
        pa.field("dimensions_json", pa.string()),
        pa.field("dimension_labels_json", pa.string()),
        pa.field("value_number", pa.float64()),
        pa.field("value_text", pa.string()),
    ]
)


def _json_get(url: str) -> dict:
    configure_http(verify=False, timeout=60)
    resp = get(url, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("status") and data.get("status") != 200:
        raise RuntimeError(f"{url} returned API status {data.get('status')}: {data.get('status_message')}")
    return data


@lru_cache(maxsize=1)
def _collection_by_code() -> dict[str, dict]:
    collection = _json_get(f"{BASE_URL}/collection?lang=en")
    out = {}
    for item in collection.get("link", {}).get("item", []):
        href = item.get("href", "")
        if "/dataset/" not in href:
            continue
        code = href.split("/dataset/", 1)[1].split("/", 1)[0]
        out[code] = item
    return out


@lru_cache(maxsize=None)
def _dimension_codes(table_code: str, dim_code: str) -> tuple[str, ...]:
    data = _json_get(f"{BASE_URL}/dimension/{table_code}/{dim_code}?lang=en")
    category = data.get("category", {})
    index = category.get("index", {})
    if isinstance(index, dict):
        ordered = sorted(index, key=lambda key: index[key])
    else:
        labels = category.get("label", {})
        ordered = list(labels.keys())
    if not ordered:
        raise RuntimeError(f"{table_code}/{dim_code}: dimension has no element codes")
    return tuple(ordered)


def _dataset_url(table_code: str, dim_codes: list[str], selection: dict[str, tuple[str, ...]]) -> str:
    params = []
    for dim_code in dim_codes:
        codes = selection[dim_code]
        params.append("all" if len(codes) == len(_dimension_codes(table_code, dim_code)) else ",".join(codes))
    return f"{BASE_URL}/dataset/{table_code}/{'/'.join(params)}?lang=en&type=json"


def _product(selection: dict[str, tuple[str, ...]]) -> int:
    return math.prod(max(1, len(v)) for v in selection.values())


def _split_selection(table_code: str, dim_codes: list[str], selection: dict[str, tuple[str, ...]]):
    url = _dataset_url(table_code, dim_codes, selection)
    if _product(selection) <= MAX_CELLS and len(url) <= MAX_URL_LEN:
        yield selection
        return

    split_dim = max((d for d in dim_codes if len(selection[d]) > 1), key=lambda d: len(selection[d]), default=None)
    if split_dim is None:
        yield selection
        return

    codes = selection[split_dim]
    mid = max(1, len(codes) // 2)
    for part in (codes[:mid], codes[mid:]):
        child = dict(selection)
        child[split_dim] = part
        yield from _split_selection(table_code, dim_codes, child)


def _ordered_category_codes(dataset: dict, dim_id: str) -> list[str]:
    category = dataset.get("dimension", {}).get(dim_id, {}).get("category", {})
    index = category.get("index", {})
    if isinstance(index, dict):
        return sorted(index, key=lambda key: index[key])
    labels = category.get("label", {})
    return list(labels.keys())


def _category_labels(dataset: dict, dim_id: str) -> dict:
    return dataset.get("dimension", {}).get(dim_id, {}).get("category", {}).get("label", {})


def _iter_rows(table_code: str, dataset: dict, slice_id: str, start_index: int):
    ids = dataset.get("id", [])
    sizes = dataset.get("size", [])
    values = dataset.get("value", [])
    metric_dims = set(dataset.get("role", {}).get("metric", []))
    keep_dims = [dim for dim in ids if dim not in metric_dims]
    dim_values = {dim: _ordered_category_codes(dataset, dim) for dim in ids}
    dim_labels = {dim: _category_labels(dataset, dim) for dim in keep_dims}

    if isinstance(values, dict):
        value_at = lambda idx: values.get(str(idx))
        total = math.prod(sizes)
    else:
        value_at = lambda idx: values[idx] if idx < len(values) else None
        total = len(values)

    for offset, combo in enumerate(itertools.product(*(dim_values[dim] for dim in ids))):
        if offset >= total:
            break
        value = value_at(offset)
        dims = {dim: combo[ids.index(dim)] for dim in keep_dims}
        labels = {
            dim: dim_labels.get(dim, {}).get(code)
            for dim, code in dims.items()
            if dim_labels.get(dim, {}).get(code) is not None
        }
        number = float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
        text = None if value is None or number is not None else str(value)
        yield {
            "table_code": table_code,
            "table_label": dataset.get("label"),
            "source_updated": dataset.get("update"),
            "row_index": start_index + offset,
            "slice_id": slice_id,
            "dimensions_json": json.dumps(dims, ensure_ascii=False, sort_keys=True),
            "dimension_labels_json": json.dumps(labels, ensure_ascii=False, sort_keys=True),
            "value_number": number,
            "value_text": text,
        }


def fetch_one(node_id: str) -> None:
    table_code = node_id.removeprefix(f"{SLUG}-").replace("-", "_")
    item = _collection_by_code().get(table_code)
    if not item:
        raise RuntimeError(f"{table_code}: not present in collection")

    dim_codes = list(item.get("dimension", {}).keys())
    if not dim_codes:
        raise RuntimeError(f"{table_code}: collection record has no dimensions")

    selection = {dim_code: _dimension_codes(table_code, dim_code) for dim_code in dim_codes}
    rows = []
    row_index = 0
    for i, chunk in enumerate(_split_selection(table_code, dim_codes, selection)):
        url = _dataset_url(table_code, dim_codes, chunk)
        dataset = _json_get(url)
        if dataset.get("class") != "dataset":
            raise RuntimeError(f"{table_code}: unexpected response for slice {i}: {dataset}")
        slice_rows = list(_iter_rows(table_code, dataset, f"slice-{i:04d}", row_index))
        row_index += len(slice_rows)
        rows.extend(slice_rows)

    if not rows:
        raise RuntimeError(f"{table_code}: fetched zero rows")

    table = pa.Table.from_pylist(rows, schema=RAW_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id.lower().replace('_', '-')}", fn=fetch_one)
    for entity_id in ENTITY_IDS
]
