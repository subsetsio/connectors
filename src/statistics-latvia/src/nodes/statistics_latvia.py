from __future__ import annotations

from math import prod

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, configure_http, get, save_raw_ndjson


BASE_URL = "https://api.stat.gov.lv/api/v2"
MAX_CELLS = 10_000
PREFIX = "statistics-latvia-"


def _entity_id_from_spec(spec_id: str) -> str:
    suffix = spec_id.removeprefix(PREFIX)
    for entity_id in ENTITY_IDS:
        if entity_id.lower().replace("_", "-") == suffix:
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


def _chunk_values(values: list[str], chunk_size: int) -> list[list[str]]:
    return [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]


def _build_selections(metadata: dict) -> list[dict[str, str]]:
    sizes = _dimension_sizes(metadata)
    if not sizes:
        return [{}]

    all_selection = {dim: "*" for dim in sizes}
    total_cells = prod(sizes.values())
    if total_cells <= MAX_CELLS:
        return [all_selection]

    time_dims = (metadata.get("role") or {}).get("time") or []
    split_dims = [dim for dim in time_dims if dim in sizes]
    if not split_dims:
        split_dims = [
            dim for dim, _size in sorted(sizes.items(), key=lambda item: item[1], reverse=True)
        ]

    selections = [all_selection]
    for dim in split_dims:
        next_selections = []
        dim_values = _dimension_values(metadata, dim)
        if not dim_values:
            continue
        for selection in selections:
            current_cells = prod(
                (sizes[d] if selection.get(d) == "*" else len(selection[d].split(",")))
                for d in sizes
            )
            if current_cells <= MAX_CELLS:
                next_selections.append(selection)
                continue
            other_cells = max(1, current_cells // sizes[dim])
            chunk_size = max(1, MAX_CELLS // other_cells)
            for values in _chunk_values(dim_values, chunk_size):
                chunk = dict(selection)
                chunk[dim] = ",".join(values)
                next_selections.append(chunk)
        selections = next_selections
        if all(
            prod(
                (sizes[d] if selection.get(d) == "*" else len(selection[d].split(",")))
                for d in sizes
            )
            <= MAX_CELLS
            for selection in selections
        ):
            break

    return selections


def _params(selection: dict[str, str]) -> list[tuple[str, str]]:
    params = [("lang", "en"), ("outputFormat", "json-stat2")]
    for dim, value in selection.items():
        params.append((f"valueCodes[{dim}]", value))
    return params


def fetch_table(spec_id: str) -> None:
    configure_http(timeout=(10.0, 120.0))
    entity_id = _entity_id_from_spec(spec_id)

    metadata_resp = get(f"{BASE_URL}/tables/{entity_id}/metadata", params={"lang": "en"})
    metadata_resp.raise_for_status()
    metadata = metadata_resp.json()

    rows = []
    selections = _build_selections(metadata)
    for index, selection in enumerate(selections):
        data_resp = get(
            f"{BASE_URL}/tables/{entity_id}/data",
            params=_params(selection),
            timeout=(10.0, 240.0),
        )
        data_resp.raise_for_status()
        rows.append(
            {
                "table_id": entity_id,
                "chunk_index": index,
                "chunk_count": len(selections),
                "selection": selection,
                "metadata": metadata if index == 0 else None,
                "payload": data_resp.json(),
            }
        )

    save_raw_ndjson(rows, spec_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]
