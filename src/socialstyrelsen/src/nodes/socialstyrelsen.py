import json
import os
import time
from datetime import datetime, timezone

from subsets_utils import NodeSpec, get, list_raw_fragments, raw_writer

from constants import ENTITY_IDS, SUBJECT_NAMES


BASE_URL = "https://sdb.socialstyrelsen.se/api/v1/sv"
PAGE_SIZE = 5000
SLUG = "socialstyrelsen"
EXT = "ndjson.gz"
DEFAULT_TIME_BUDGET_S = 20_700.0
MAX_LEG_SECONDS = 3_600.0
DAG_SHUTDOWN_MARGIN_S = 900.0


def _fetched_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_json(url: str, *, params: dict | None = None):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _leg_seconds() -> float:
    try:
        budget = float(os.environ.get("DAG_TIME_BUDGET", "")) or DEFAULT_TIME_BUDGET_S
    except ValueError:
        budget = DEFAULT_TIME_BUDGET_S
    return min(MAX_LEG_SECONDS, max(300.0, budget - DAG_SHUTDOWN_MARGIN_S))


def _entity_from_node_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id.removeprefix(prefix).replace("-", "_")


def _dimension_values(entity_id: str, dimension_id: str) -> list[dict]:
    values = _get_json(f"{BASE_URL}/{entity_id}/{dimension_id}")
    if not isinstance(values, list):
        raise ValueError(f"{entity_id}/{dimension_id}: expected list, got {type(values).__name__}")
    return values


def _value_key(dimension_id: str) -> str:
    return "ar" if dimension_id == "ar" else f"{dimension_id}Id"


def _build_dimension_maps(entity_id: str) -> tuple[list[dict], dict[str, dict[str, str]]]:
    dimensions = _get_json(f"{BASE_URL}/{entity_id}")
    if not isinstance(dimensions, list) or not dimensions:
        raise ValueError(f"{entity_id}: expected non-empty dimension list")

    label_maps: dict[str, dict[str, str]] = {}
    for dim in dimensions:
        dim_id = dim.get("namn")
        if not dim_id:
            continue
        values = _dimension_values(entity_id, dim_id)
        labels = {}
        for value in values:
            key = value.get("id", value.get("kod", value.get("text")))
            if key is None:
                continue
            labels[str(key)] = value.get("text")
        label_maps[dim_id] = labels
    return dimensions, label_maps


def _metric_ids(entity_id: str, label_maps: dict[str, dict[str, str]]) -> list[str | None]:
    metric_map = label_maps.get("matt")
    if not metric_map:
        return [None]
    return list(metric_map.keys())


def _metric_fragment(metric_id: str | None, page: int) -> str:
    metric = "all" if metric_id is None else str(metric_id)
    return f"m{metric}-p{page:05d}"


def _result_url(entity_id: str, metric_id: str | None) -> str:
    if metric_id is None:
        return f"{BASE_URL}/{entity_id}/resultat"
    return f"{BASE_URL}/{entity_id}/resultat/matt/{metric_id}"


def _enrich_row(
    row: dict,
    *,
    entity_id: str,
    subject_name: str,
    label_specs: list[tuple[str, str, dict[str, str]]],
    fetched_at: str,
) -> dict:
    out = {
        "subject_id": entity_id,
        "subject_name": subject_name,
        "fetched_at": fetched_at,
    }
    out.update(row)
    for key, text_key, labels in label_specs:
        value = row.get(key)
        if value is None:
            continue
        label = labels.get(str(value))
        if label is not None:
            out[text_key] = label
    return out


def _label_specs(dimensions: list[dict], label_maps: dict[str, dict[str, str]]) -> list[tuple[str, str, dict[str, str]]]:
    specs = []
    for dim in dimensions:
        dim_id = dim.get("namn")
        if not dim_id:
            continue
        labels = label_maps.get(dim_id) or {}
        if labels:
            specs.append((_value_key(dim_id), f"{dim_id}Text", labels))
    return specs


def _write_rows(
    node_id: str,
    fragment: str,
    rows: list[dict],
    *,
    entity_id: str,
    subject_name: str,
    label_specs: list[tuple[str, str, dict[str, str]]],
    fetched_at: str,
) -> int:
    count = 0
    with raw_writer(node_id, EXT, mode="wt", compression="gzip", fragment=fragment) as out:
        for row in rows:
            enriched = _enrich_row(
                row,
                entity_id=entity_id,
                subject_name=subject_name,
                label_specs=label_specs,
                fetched_at=fetched_at,
            )
            out.write(json.dumps(enriched, ensure_ascii=False, separators=(",", ":")))
            out.write("\n")
            count += 1
    return count


def fetch_subject(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    if entity_id not in ENTITY_IDS:
        raise ValueError(f"{node_id}: unknown entity {entity_id!r}")

    subject_name = SUBJECT_NAMES.get(entity_id, entity_id)
    dimensions, label_maps = _build_dimension_maps(entity_id)
    label_specs = _label_specs(dimensions, label_maps)
    fetched_at = _fetched_at()
    run_id = os.environ.get("RUN_ID", "unknown")
    committed = {
        frag
        for frag, meta in list_raw_fragments(node_id, EXT).items()
        if meta.get("run_id") == run_id
    }
    deadline = time.monotonic() + _leg_seconds()
    rows_this_leg = 0

    for metric_id in _metric_ids(entity_id, label_maps):
        url = _result_url(entity_id, metric_id)
        first = _get_json(url, params={"per_sida": PAGE_SIZE, "sida": 1})
        first_rows = first.get("data")
        if not isinstance(first_rows, list):
            raise ValueError(f"{entity_id}: page 1 returned no data list")

        total_pages = int(first.get("sidor") or 1)
        if not first_rows:
            continue

        for page in range(1, total_pages + 1):
            fragment = _metric_fragment(metric_id, page)
            if fragment in committed:
                continue

            if rows_this_leg and time.monotonic() >= deadline:
                print(
                    f"  -> {node_id}: leg budget spent after {rows_this_leg:,} rows; "
                    "committing fragments and requesting continuation"
                )
                return True

            if page == 1:
                rows = first_rows
            else:
                data = _get_json(url, params={"per_sida": PAGE_SIZE, "sida": page})
                rows = data.get("data")
                if not isinstance(rows, list):
                    raise ValueError(f"{entity_id}: page {page} returned no data list")

            if rows:
                rows_this_leg += _write_rows(
                    node_id,
                    fragment,
                    rows,
                    entity_id=entity_id,
                    subject_name=subject_name,
                    label_specs=label_specs,
                    fetched_at=fetched_at,
                )

    if rows_this_leg == 0 and not committed:
        raise AssertionError(f"{node_id}: fetched zero result rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_subject,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
