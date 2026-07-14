from __future__ import annotations

from math import prod

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    configure_http,
    get,
    post,
    raw_asset_exists,
    save_raw_ndjson,
)


BASE_URL = "https://api.stat.gov.lv/api/v2"
V1_BASE_URL = "https://data.stat.gov.lv/api/v1/en/OSP_PUB/START"
MAX_CELLS = 10_000
V1_MAX_CELLS = 100_000
MAX_CODES_PER_PARAM = 500
PREFIX = "statistics-latvia-"
SPEC_ENTITY_IDS = {
    entity_id.lower().replace("_", "-").strip(): entity_id for entity_id in ENTITY_IDS
}


def _entity_id_from_spec(spec_id: str) -> str:
    suffix = spec_id.removeprefix(PREFIX)
    entity_id = SPEC_ENTITY_IDS.get(suffix.strip())
    if entity_id:
        return entity_id
    raise ValueError(f"unknown Statistics Latvia spec id: {spec_id}")


def _dimension_sizes(metadata: dict) -> dict[str, int]:
    ids = metadata.get("id") or []
    sizes = metadata.get("size") or []
    return {dim: int(size) for dim, size in zip(ids, sizes)}


def _dimension_values(metadata: dict, dim: str) -> list[str]:
    category = (metadata.get("dimension") or {}).get(dim, {}).get("category") or {}
    index = category.get("index") or {}
    if isinstance(index, dict):
        return [
            code
            for code, _pos in sorted(index.items(), key=lambda item: int(item[1]))
        ]
    if isinstance(index, list):
        return list(index)
    return []


def _product_size(selection: dict[str, list[str]]) -> int:
    return prod(len(values) for values in selection.values())


def _split_selection(
    selection: dict[str, list[str]], max_cells: int
) -> list[dict[str, list[str]]]:
    if _product_size(selection) <= max_cells:
        return [selection]

    dim = max(selection, key=lambda key: len(selection[key]))
    values = selection[dim]
    if len(values) <= 1:
        raise ValueError("could not split table below API maxDataCells limit")

    other_cells = max(1, _product_size(selection) // len(values))
    chunk_size = max(1, min(MAX_CODES_PER_PARAM, max_cells // other_cells))

    chunks: list[dict[str, list[str]]] = []
    for start in range(0, len(values), chunk_size):
        chunk = {key: list(codes) for key, codes in selection.items()}
        chunk[dim] = values[start : start + chunk_size]
        chunks.extend(_split_selection(chunk, max_cells))
    return chunks


def _build_selections(metadata: dict, max_cells: int = MAX_CELLS) -> list[dict[str, str]]:
    dim_ids = metadata.get("id") or []
    if not dim_ids:
        return [{}]

    full = {dim: _dimension_values(metadata, dim) for dim in dim_ids}
    if _product_size(full) <= max_cells:
        return [{dim: "*" for dim in dim_ids}]

    selections = []
    for chunk in _split_selection(full, max_cells):
        selection = {}
        for dim in dim_ids:
            full_values = full[dim]
            chunk_values = chunk[dim]
            selection[dim] = "*" if chunk_values == full_values else ",".join(chunk_values)
        selections.append(selection)
    return selections


def _params(selection: dict[str, str]) -> list[tuple[str, str]]:
    params = [("lang", "en"), ("outputFormat", "json-stat2")]
    for dim, value in selection.items():
        params.append((f"valueCodes[{dim}]", value))
    return params


def _v1_url(entity_id: str) -> str:
    catalog_resp = get(
        f"{BASE_URL}/tables",
        params={"lang": "en", "query": entity_id, "pageSize": 20},
        timeout=(10.0, 60.0),
    )
    catalog_resp.raise_for_status()
    matches = [
        table for table in (catalog_resp.json().get("tables") or []) if table.get("id") == entity_id
    ]
    if not matches:
        raise ValueError(f"could not find Statistics Latvia catalog path for {entity_id}")

    paths = matches[0].get("paths") or []
    if not paths:
        raise ValueError(f"Statistics Latvia catalog entry has no path for {entity_id}")
    path_ids = [str(part["id"]) for part in paths[0] if part.get("id")]
    return "/".join([V1_BASE_URL, *path_ids, entity_id])


def _v1_body(selection: dict[str, str], metadata: dict) -> dict:
    query = []
    for dim in metadata.get("id") or []:
        selected = selection.get(dim)
        values = _dimension_values(metadata, dim) if selected == "*" else (selected or "").split(",")
        query.append({"code": dim, "selection": {"filter": "item", "values": values}})
    return {"query": query, "response": {"format": "JSON-stat2"}}


def _fetch_v1_chunks(entity_id: str, metadata: dict, spec_id: str) -> None:
    table_url = _v1_url(entity_id)
    selections = _build_selections(metadata, max_cells=V1_MAX_CELLS)
    for index, selection in enumerate(selections):
        data_resp = post(
            table_url,
            json=_v1_body(selection, metadata),
            timeout=(10.0, 240.0),
        )
        data_resp.raise_for_status()
        save_raw_ndjson(
            [
                {
                    "table_id": entity_id,
                    "chunk_index": index,
                    "chunk_count": len(selections),
                    "selection": selection,
                    "metadata": metadata if index == 0 else None,
                    "payload": data_resp.json(),
                }
            ],
            spec_id,
            fragment=f"{index:04d}",
        )


def _fetch_v2_chunks(entity_id: str, metadata: dict, spec_id: str) -> None:
    selections = _build_selections(metadata)
    for index, selection in enumerate(selections):
        data_resp = get(
            f"{BASE_URL}/tables/{entity_id}/data",
            params=_params(selection),
            timeout=(10.0, 240.0),
        )
        data_resp.raise_for_status()
        save_raw_ndjson(
            [
                {
                    "table_id": entity_id,
                    "chunk_index": index,
                    "chunk_count": len(selections),
                    "selection": selection,
                    "metadata": metadata if index == 0 else None,
                    "payload": data_resp.json(),
                }
            ],
            spec_id,
            fragment=f"{index:04d}",
        )


def fetch_table(spec_id: str) -> None:
    configure_http(timeout=(10.0, 120.0))
    entity_id = _entity_id_from_spec(spec_id)

    metadata_resp = get(f"{BASE_URL}/tables/{entity_id}/metadata", params={"lang": "en"})
    metadata_resp.raise_for_status()
    metadata = metadata_resp.json()

    sizes = _dimension_sizes(metadata)
    cell_count = prod(sizes.values()) if sizes else 0
    if cell_count > MAX_CELLS:
        _fetch_v1_chunks(entity_id, metadata, spec_id)
    else:
        _fetch_v2_chunks(entity_id, metadata, spec_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Statistics Latvia tables carry table-specific updated timestamps; "
            "the connector refreshes accepted tables at least weekly."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
