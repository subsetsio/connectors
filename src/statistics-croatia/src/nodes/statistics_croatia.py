"""Statistics Croatia PxWeb downloads."""

from __future__ import annotations

import time
from itertools import product
from urllib.parse import quote

from constants import ENTITY_METADATA
from subsets_utils import MaintainSpec, NodeSpec, get, post, raw_asset_exists, save_raw_ndjson


BASE_URL = "https://web.dzs.hr/PxWeb/api/v1/en"
SPEC_PREFIX = "statistics-croatia-"
MAX_CELLS_PER_POST = 50_000
MAX_VALUES_PER_POST = 50
POST_THROTTLE_SECONDS = 0.2
FRESH_RAW_MAX_AGE_DAYS = 14
UNAVAILABLE_ENTITY_IDS = {
    "robna-razmjena-s-inozemstvom-od-2010-do-2012-godine-fld-country2-eng",
    "robna-razmjena-s-inozemstvom-od-2010-do-2012-godine-fld-country4-eng",
}
UNAVAILABLE_SPEC_IDS = {f"{SPEC_PREFIX}{entity_id}" for entity_id in UNAVAILABLE_ENTITY_IDS}


def _table_url(meta: dict) -> str:
    parts = list(meta["category_path"]) + [meta["id"]]
    return BASE_URL + "/" + "/".join(quote(part, safe="") for part in parts)


def _entity_id_from_spec(spec_id: str) -> str:
    if not spec_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected spec id: {spec_id}")
    return spec_id[len(SPEC_PREFIX) :]


def _query(metadata: dict, *, split_code: str | None = None, split_values: list[str] | None = None) -> dict:
    return {
        "query": [
            {
                "code": variable["code"],
                "selection": {
                    "filter": "item",
                    "values": split_values
                    if variable["code"] == split_code and split_values is not None
                    else variable.get("values", []),
                },
            }
            for variable in metadata.get("variables", [])
        ],
        "response": {"format": "JSON-stat2"},
    }


def _query_all(metadata: dict) -> dict:
    return _query(metadata)


def _labels_by_code(dimension: dict) -> dict:
    category = dimension.get("category") or {}
    return category.get("label") or {}


def _codes_by_position(dimension: dict) -> list[str]:
    category = dimension.get("category") or {}
    index = category.get("index") or {}
    if isinstance(index, list):
        return list(index)
    codes = [None] * len(index)
    for code, pos in index.items():
        if isinstance(pos, int) and 0 <= pos < len(codes):
            codes[pos] = code
    return [code for code in codes if code is not None]


def _value_at(values, offset: int):
    if isinstance(values, list):
        return values[offset] if offset < len(values) else None
    if isinstance(values, dict):
        return values.get(str(offset), values.get(offset))
    return None


def _jsonstat_rows(dataset: dict, *, entity_id: str, source_meta: dict, include_nulls: bool = False):
    ids = dataset.get("id") or []
    sizes = dataset.get("size") or []
    dimensions = dataset.get("dimension") or {}
    values = dataset.get("value") or []
    statuses = dataset.get("status") or {}

    dim_codes = []
    dim_labels = {}
    for dim_id in ids:
        dim = dimensions.get(dim_id) or {}
        dim_codes.append(_codes_by_position(dim))
        dim_labels[dim_id] = _labels_by_code(dim)

    eliminated = {}
    for dim_id, dim in dimensions.items():
        if dim_id in ids:
            continue
        extension = dim.get("extension") or {}
        if extension.get("elimination"):
            labels = _labels_by_code(dim)
            eliminated[dim_id] = labels

    multipliers = []
    running = 1
    for size in reversed(sizes):
        multipliers.insert(0, running)
        running *= size

    for coords in product(*[range(size) for size in sizes]):
        offset = sum(coord * multiplier for coord, multiplier in zip(coords, multipliers))
        value = _value_at(values, offset)
        if value is None and not include_nulls:
            continue

        dimension_codes = {}
        dimension_labels = {}
        for dim_id, coord, codes in zip(ids, coords, dim_codes):
            code = codes[coord] if coord < len(codes) else str(coord)
            dimension_codes[dim_id] = code
            dimension_labels[dim_id] = dim_labels.get(dim_id, {}).get(code)

        yield {
            "entity_id": entity_id,
            "table_id": source_meta["id"],
            "table_title": dataset.get("label") or source_meta.get("text"),
            "source_updated": dataset.get("updated") or source_meta.get("updated"),
            "category_path": source_meta.get("category_path") or [],
            "dimension_codes": dimension_codes,
            "dimension_labels": dimension_labels,
            "eliminated_dimensions": eliminated,
            "value": value,
            "status": _value_at(statuses, offset),
        }


def _post_jsonstat(url: str, query: dict) -> dict:
    time.sleep(POST_THROTTLE_SECONDS)
    response = post(url, json=query, timeout=(10.0, 300.0))
    response.raise_for_status()
    return response.json()


def _post_split_jsonstat(
    url: str,
    metadata: dict,
    *,
    split_code: str,
    split_values: list[str],
) -> list[dict]:
    query = _query(metadata, split_code=split_code, split_values=split_values)
    time.sleep(POST_THROTTLE_SECONDS)
    response = post(url, json=query, timeout=(10.0, 300.0))
    if response.status_code in {400, 403} and len(split_values) > 1:
        midpoint = len(split_values) // 2
        return [
            *_post_split_jsonstat(
                url,
                metadata,
                split_code=split_code,
                split_values=split_values[:midpoint],
            ),
            *_post_split_jsonstat(
                url,
                metadata,
                split_code=split_code,
                split_values=split_values[midpoint:],
            ),
        ]
    if response.status_code == 400 and len(split_values) == 1:
        return []
    response.raise_for_status()
    return [response.json()]


def _chunked_datasets(url: str, metadata: dict) -> list[dict]:
    variables = metadata.get("variables", [])
    if not variables:
        return [_post_jsonstat(url, _query_all(metadata))]

    split_variable = max(variables, key=lambda variable: len(variable.get("values", [])))
    split_values = list(split_variable.get("values", []))
    if not split_values:
        return [_post_jsonstat(url, _query_all(metadata))]

    other_cell_count = 1
    for variable in variables:
        if variable["code"] != split_variable["code"]:
            other_cell_count *= max(1, len(variable.get("values", [])))

    chunk_size = max(1, min(MAX_VALUES_PER_POST, MAX_CELLS_PER_POST // other_cell_count))
    datasets = []
    for start in range(0, len(split_values), chunk_size):
        chunk = split_values[start : start + chunk_size]
        datasets.extend(
            _post_split_jsonstat(
                url,
                metadata,
                split_code=split_variable["code"],
                split_values=chunk,
            )
        )
    return datasets


def fetch_one(spec_id: str) -> None:
    entity_id = _entity_id_from_spec(spec_id)
    source_meta = ENTITY_METADATA[entity_id]
    url = _table_url(source_meta)

    metadata_resp = get(url, timeout=(10.0, 120.0))
    metadata_resp.raise_for_status()
    metadata = metadata_resp.json()

    datasets = _chunked_datasets(url, metadata)
    rows = [
        row
        for dataset in datasets
        for row in _jsonstat_rows(dataset, entity_id=entity_id, source_meta=source_meta)
    ]
    if not rows:
        rows = [
            row
            for dataset in datasets
            for row in _jsonstat_rows(
                dataset,
                entity_id=entity_id,
                source_meta=source_meta,
                include_nulls=True,
            )
        ]
    if not rows:
        raise ValueError(f"{spec_id}: PxWeb response produced no non-null observations")
    save_raw_ndjson(rows, spec_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SPEC_PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_one)
    for entity_id in ENTITY_METADATA
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "PxWeb tables are refreshed on the DZS statistical database; reuse a "
            f"successful raw pull for up to {FRESH_RAW_MAX_AGE_DAYS} days because "
            "the 885-table corpus exceeds one GitHub Actions chain when fully "
            "refetched. Two legacy 2010-2012 foreign-trade tables are permanently "
            "unavailable via PxWeb despite live metadata and are covered by spec "
            "waivers."
        ),
        check=lambda asset_id: asset_id in UNAVAILABLE_SPEC_IDS
        or raw_asset_exists(asset_id, "ndjson.zst", max_age_days=FRESH_RAW_MAX_AGE_DAYS),
    )
    for spec in DOWNLOAD_SPECS
]
