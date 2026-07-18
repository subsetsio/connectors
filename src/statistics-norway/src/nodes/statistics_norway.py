from __future__ import annotations

from datetime import datetime, timedelta, timezone
from itertools import product

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    list_raw_fragments,
    post,
    raw_asset_exists,
    save_raw_ndjson,
)


BASE_URL = "https://data.ssb.no/api/pxwebapi/v2"
PREFIX = "statistics-norway-"
MAX_CELLS_PER_REQUEST = 750_000
MAINTAIN_MAX_AGE_DAYS = 7
RAW_EXT = "ndjson.zst"
CADENCE = (
    "Refreshed weekly by age-based raw cache; Statistics Norway table data is "
    "queried per table through https://data.ssb.no/api/pxwebapi/v2."
)


def _table_id_from_asset(asset_id: str) -> str:
    if not asset_id.startswith(PREFIX):
        raise ValueError(f"unexpected Statistics Norway asset id: {asset_id}")
    return asset_id.removeprefix(PREFIX)


def _json(url: str, *, params: dict[str, str] | None = None) -> dict:
    response = get(url, params=params, timeout=(10.0, 180.0))
    response.raise_for_status()
    return response.json()


def _post_json(url: str, *, params: dict[str, str], body: dict) -> dict:
    response = post(url, params=params, json=body, timeout=(10.0, 180.0))
    response.raise_for_status()
    return response.json()


def _codes_for_dimension(dimension: dict) -> list[str]:
    index = dimension.get("category", {}).get("index", {})
    if isinstance(index, dict):
        return [code for code, _pos in sorted(index.items(), key=lambda item: item[1])]
    if isinstance(index, list):
        return [str(code) for code in index]
    raise ValueError(f"unsupported JSON-stat category index: {type(index).__name__}")


def _product_size(selection: dict[str, list[str]]) -> int:
    total = 1
    for codes in selection.values():
        total *= len(codes)
    return total


def _split_selection(
    selection: dict[str, list[str]],
    max_cells: int = MAX_CELLS_PER_REQUEST,
) -> list[dict[str, list[str]]]:
    if _product_size(selection) <= max_cells:
        return [selection]

    dimension_id = max(selection, key=lambda key: len(selection[key]))
    codes = selection[dimension_id]
    other_size = max(1, _product_size(selection) // max(1, len(codes)))
    chunk_size = max(1, max_cells // other_size)

    chunks: list[dict[str, list[str]]] = []
    for start in range(0, len(codes), chunk_size):
        chunk = {key: list(value) for key, value in selection.items()}
        chunk[dimension_id] = codes[start : start + chunk_size]
        chunks.extend(_split_selection(chunk, max_cells))
    return chunks


def _fresh_fragment_keys(asset_id: str) -> set[str]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAINTAIN_MAX_AGE_DAYS)
    fresh = set()
    for fragment, metadata in list_raw_fragments(asset_id, RAW_EXT).items():
        fetched_at = metadata.get("fetched_at")
        if not fetched_at:
            continue
        try:
            fetched = datetime.fromisoformat(str(fetched_at).replace("Z", "+00:00"))
        except ValueError:
            continue
        if fetched >= cutoff:
            fresh.add(fragment)
    return fresh


def _period_start(period: str | None) -> str | None:
    if not period:
        return None
    text = str(period)
    year = text[:4]
    if not year.isdigit():
        return None
    if "M" in text:
        month = text.split("M", 1)[1][:2]
        if month.isdigit() and 1 <= int(month) <= 12:
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


def _status_at(statuses, offset: int):
    if isinstance(statuses, dict):
        return statuses.get(str(offset))
    if isinstance(statuses, list) and offset < len(statuses):
        return statuses[offset]
    return None


def _flatten_dataset(table_id: str, dataset: dict) -> list[dict]:
    dimension_ids = dataset["id"]
    sizes = dataset["size"]
    dimensions = dataset["dimension"]
    strides = []
    for idx in range(len(sizes)):
        stride = 1
        for size in sizes[idx + 1 :]:
            stride *= size
        strides.append(stride)

    code_lists = [_codes_for_dimension(dimensions[dimension_id]) for dimension_id in dimension_ids]
    values = dataset.get("value", [])
    statuses = dataset.get("status") or {}
    roles = dataset.get("role") or {}
    time_dimensions = set(roles.get("time") or [])
    metric_dimensions = set(roles.get("metric") or [])
    geo_dimensions = set(roles.get("geo") or [])

    rows = []
    for positions in product(*[range(len(codes)) for codes in code_lists]):
        offset = sum(pos * stride for pos, stride in zip(positions, strides))
        row = {
            "table_id": table_id,
            "table_label": dataset.get("label"),
            "source": dataset.get("source"),
            "updated": dataset.get("updated"),
            "observation_index": offset,
            "value": _value_at(values, offset),
            "status": _status_at(statuses, offset),
        }
        for dimension_id, codes, pos in zip(dimension_ids, code_lists, positions):
            dimension = dimensions[dimension_id]
            category = dimension.get("category", {})
            code = codes[pos]
            unit = (category.get("unit") or {}).get(code) or {}
            if dimension_id in time_dimensions:
                role = "time"
            elif dimension_id in metric_dimensions:
                role = "metric"
            elif dimension_id in geo_dimensions:
                role = "geo"
            else:
                role = "dimension"

            row[f"{dimension_id}_code"] = code
            row[f"{dimension_id}_label"] = (category.get("label") or {}).get(code)
            row[f"{dimension_id}_role"] = role
            if dimension_id in time_dimensions:
                row["period"] = code
                row["period_start"] = _period_start(code)
            if unit:
                row["unit"] = unit.get("base")
                row["decimals"] = unit.get("decimals")
        rows.append(row)
    return rows


def fetch_table(asset_id: str) -> None:
    table_id = _table_id_from_asset(asset_id)
    table_url = f"{BASE_URL}/tables/{table_id}"
    metadata_url = f"{table_url}/metadata"
    data_url = f"{table_url}/data"

    metadata = _json(metadata_url, params={"lang": "en"})
    selection = {
        dimension_id: _codes_for_dimension(metadata["dimension"][dimension_id])
        for dimension_id in metadata["id"]
    }

    total_rows = 0
    chunks = _split_selection(selection)
    fresh_fragments = _fresh_fragment_keys(asset_id)
    for idx, chunk in enumerate(chunks):
        fragment = f"{idx:04d}"
        if fragment in fresh_fragments:
            continue

        params = {"lang": "en", "outputFormat": "json-stat2"}
        body = {
            "selection": [
                {"variableCode": dimension_id, "valueCodes": codes}
                for dimension_id, codes in chunk.items()
            ]
        }
        dataset = _post_json(data_url, params=params, body=body)
        rows = _flatten_dataset(table_id, dataset)
        total_rows += len(rows)
        save_raw_ndjson(rows, asset_id, fragment=fragment)

    if total_rows == 0 and len(fresh_fragments) < len(chunks):
        raise RuntimeError(f"{asset_id}: fetched zero rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=CADENCE,
        check=lambda asset_id: raw_asset_exists(asset_id, RAW_EXT, max_age_days=MAINTAIN_MAX_AGE_DAYS),
    )
    for spec in DOWNLOAD_SPECS
]
