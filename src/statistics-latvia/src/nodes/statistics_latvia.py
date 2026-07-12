from __future__ import annotations

from math import prod

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, configure_http, get, save_raw_ndjson


BASE_URL = "https://api.stat.gov.lv/api/v2"
MAX_CELLS = 10_000
MAX_CODES_PER_PARAM = 500
PREFIX = "statistics-latvia-"


def _entity_id_from_spec(spec_id: str) -> str:
    suffix = spec_id.removeprefix(PREFIX)
    for entity_id in ENTITY_IDS:
        spec_entity_id = entity_id.lower().replace("_", "-")
        if spec_entity_id == suffix or spec_entity_id.strip() == suffix.strip():
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


def _has_whitespace_sensitive_codes(values: list[str]) -> bool:
    return any(value != value.strip() for value in values)


def _selected_values(metadata: dict, selection: dict[str, str], dim: str) -> list[str]:
    selected = selection.get(dim)
    if selected and selected != "*":
        return selected.split(",")
    return _dimension_values(metadata, dim)


def _selection_cells(metadata: dict, sizes: dict[str, int], selection: dict[str, str]) -> int:
    return prod(
        (
            len(_selected_values(metadata, selection, dim))
            if selection.get(dim) != "*"
            else size
        )
        for dim, size in sizes.items()
    )


def _build_selections(metadata: dict) -> list[dict[str, str]]:
    sizes = _dimension_sizes(metadata)
    if not sizes:
        return [{}]

    all_selection = {dim: "*" for dim in sizes}
    if _selection_cells(metadata, sizes, all_selection) <= MAX_CELLS:
        return [all_selection]

    time_dims = (metadata.get("role") or {}).get("time") or []
    selections = [all_selection]
    while True:
        oversized = [
            selection
            for selection in selections
            if _selection_cells(metadata, sizes, selection) > MAX_CELLS
        ]
        if not oversized:
            return selections

        next_selections = []
        progressed = False
        for selection in selections:
            current_cells = _selection_cells(metadata, sizes, selection)
            if current_cells <= MAX_CELLS:
                next_selections.append(selection)
                continue

            dim_values_by_dim = {
                dim: _selected_values(metadata, selection, dim) for dim in sizes
            }
            splittable = [
                dim for dim, values in dim_values_by_dim.items() if len(values) > 1
            ]
            if not splittable:
                next_selections.append(selection)
                continue

            def split_plan(candidate: str) -> tuple[int, int]:
                values = dim_values_by_dim[candidate]
                other = max(1, current_cells // len(values))
                size = max(1, min(MAX_CODES_PER_PARAM, MAX_CELLS // other))
                chunks = (len(values) + size - 1) // size
                return chunks, size

            viable = [
                dim
                for dim in splittable
                if split_plan(dim)[1] < len(dim_values_by_dim[dim])
            ]
            if not viable:
                next_selections.append(selection)
                continue

            dim = min(
                viable,
                key=lambda candidate: (
                    _has_whitespace_sensitive_codes(dim_values_by_dim[candidate]),
                    split_plan(candidate)[0],
                    candidate in time_dims,
                    -len(dim_values_by_dim[candidate]),
                ),
            )
            dim_values = dim_values_by_dim[dim]
            other_cells = max(1, current_cells // len(dim_values))
            chunk_size = max(1, min(MAX_CODES_PER_PARAM, MAX_CELLS // other_cells))

            progressed = True
            for values in _chunk_values(dim_values, chunk_size):
                chunk = dict(selection)
                chunk[dim] = ",".join(values)
                next_selections.append(chunk)
        selections = next_selections

        if not progressed:
            too_large = [
                selection
                for selection in selections
                if _selection_cells(metadata, sizes, selection) > MAX_CELLS
            ]
            if too_large:
                raise ValueError(
                    "could not split table below API maxDataCells limit "
                    f"({len(too_large)} oversized selection(s))"
                )
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
