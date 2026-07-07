import json
from datetime import datetime, timezone

from subsets_utils import NodeSpec, get, raw_writer

from constants import ENTITY_IDS, SUBJECT_NAMES


BASE_URL = "https://sdb.socialstyrelsen.se/api/v1/sv"
PAGE_SIZE = 5000
SLUG = "socialstyrelsen"


def _fetched_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_json(url: str, *, params: dict | None = None):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


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


def _result_url(entity_id: str, metric_id: str | None) -> str:
    if metric_id is None:
        return f"{BASE_URL}/{entity_id}/resultat"
    return f"{BASE_URL}/{entity_id}/resultat/matt/{metric_id}"


def _enrich_row(
    row: dict,
    *,
    entity_id: str,
    subject_name: str,
    dimensions: list[dict],
    label_maps: dict[str, dict[str, str]],
    fetched_at: str,
) -> dict:
    out = {
        "subject_id": entity_id,
        "subject_name": subject_name,
        "fetched_at": fetched_at,
    }
    out.update(row)
    for dim in dimensions:
        dim_id = dim.get("namn")
        if not dim_id:
            continue
        key = _value_key(dim_id)
        value = row.get(key)
        if value is None:
            continue
        label = label_maps.get(dim_id, {}).get(str(value))
        if label is not None:
            out[f"{dim_id}Text"] = label
    return out


def fetch_subject(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    if entity_id not in ENTITY_IDS:
        raise ValueError(f"{node_id}: unknown entity {entity_id!r}")

    subject_name = SUBJECT_NAMES.get(entity_id, entity_id)
    dimensions, label_maps = _build_dimension_maps(entity_id)
    fetched_at = _fetched_at()
    total_rows = 0

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for metric_id in _metric_ids(entity_id, label_maps):
            page = 1
            while True:
                data = _get_json(
                    _result_url(entity_id, metric_id),
                    params={"per_sida": PAGE_SIZE, "sida": page},
                )
                rows = data.get("data")
                if not isinstance(rows, list):
                    raise ValueError(f"{entity_id}: page {page} returned no data list")
                for row in rows:
                    enriched = _enrich_row(
                        row,
                        entity_id=entity_id,
                        subject_name=subject_name,
                        dimensions=dimensions,
                        label_maps=label_maps,
                        fetched_at=fetched_at,
                    )
                    out.write(json.dumps(enriched, ensure_ascii=False, separators=(",", ":")))
                    out.write("\n")
                    total_rows += 1
                if not rows or page >= int(data.get("sidor") or page):
                    break
                page += 1

    if total_rows == 0:
        raise AssertionError(f"{node_id}: fetched zero result rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_subject,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
