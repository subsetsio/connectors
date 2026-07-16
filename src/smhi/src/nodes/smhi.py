import csv
import io
import json
import re
import time
from datetime import datetime, timezone

import httpx

from constants import ENTITY_IDS, FAMILIES
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    list_raw_fragments,
    raw_asset_exists,
    raw_writer,
    save_raw_ndjson,
)


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}(?::\d{2})?)")
SKIPPABLE_DATA_STATUSES = {404, 406, 410}
OBSERVATION_EXT = "ndjson.gz"
OBSERVATION_NODE_BUDGET_S = 90 * 60
FRESH_REFERENCE_MAX_AGE_DAYS = 30
FRESH_OBSERVATION_MAX_AGE_DAYS = 7


def _fetch_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text.lstrip("\ufeff")


def _fetch_data_text(url: str) -> str | None:
    try:
        return _fetch_text(url)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in SKIPPABLE_DATA_STATUSES:
            return None
        raise


def _family_from_entity(entity_id: str) -> str:
    family = entity_id.split("-", 1)[0]
    if family not in FAMILIES:
        raise ValueError(f"Unknown SMHI family in entity id: {entity_id}")
    return family


def _entity_from_node_id(node_id: str) -> str:
    return node_id.removeprefix("smhi-")


def _drop_links(value):
    if isinstance(value, dict):
        return {
            key: _drop_links(item)
            for key, item in value.items()
            if key not in {"link", "href"}
        }
    if isinstance(value, list):
        return [_drop_links(item) for item in value]
    return value


def _version(family: str) -> dict:
    return _fetch_json(f"{FAMILIES[family]['base_url']}/version/1.0.json")


def _parameter_detail(family: str, parameter_key: str) -> dict:
    base_url = FAMILIES[family]["base_url"]
    return _fetch_json(f"{base_url}/version/1.0/parameter/{parameter_key}.json")


def _station_detail(family: str, parameter_key: str, station_key: str) -> dict:
    base_url = FAMILIES[family]["base_url"]
    return _fetch_json(
        f"{base_url}/version/1.0/parameter/{parameter_key}/station/{station_key}.json"
    )


def _iter_parameters(family: str):
    for parameter in _version(family).get("resource", []):
        key = parameter.get("key")
        if key is not None:
            yield str(key), parameter


def _iter_station_refs(family: str):
    seen = set()
    for parameter_key, _parameter in _iter_parameters(family):
        detail = _parameter_detail(family, parameter_key)
        for station in detail.get("station") or []:
            station_key = str(station.get("key") or station.get("id") or "")
            if not station_key:
                continue
            yield parameter_key, station_key, station
            seen.add((parameter_key, station_key))


def _parameter_rows(family: str):
    for parameter_key, parameter in _iter_parameters(family):
        detail = _parameter_detail(family, parameter_key)
        clean_detail = _drop_links(detail)
        clean_detail.pop("station", None)
        clean_detail.pop("stationSet", None)
        yield {
            "family_id": family,
            "parameter_key": parameter_key,
            "parameter": _drop_links(parameter),
            "parameter_detail": clean_detail,
        }


def _station_rows(family: str):
    for parameter_key, station_key, station in _iter_station_refs(family):
        yield {
            "family_id": family,
            "parameter_key": parameter_key,
            "station_key": station_key,
            "station": _drop_links(station),
        }


def _csv_data_rows(text: str, family: str, parameter_key: str, station_key: str, period_key: str):
    reader = csv.reader(io.StringIO(text), delimiter=";")
    header = None
    data_col_idx = None
    time_idx = None
    quality_idx = None
    data_col_name = None

    for row in reader:
        if not row or not row[0]:
            continue
        first = row[0].strip()
        if header is None:
            if "datum" in first.lower():
                header = [cell.strip() for cell in row]
                for idx, name in enumerate(header):
                    lowered = name.lower()
                    if lowered == "tid" or lowered.startswith("tid "):
                        time_idx = idx
                    elif lowered == "kvalitet":
                        quality_idx = idx
                for idx, name in enumerate(header):
                    lowered = name.lower()
                    if not name or "datum" in lowered or lowered.startswith("tid"):
                        continue
                    if (
                        lowered == "kvalitet"
                        or lowered.startswith("tidsutsnitt")
                        or lowered.startswith("mätdjup")
                        or lowered.startswith("representativt")
                        or "latitud" in lowered
                        or "longitud" in lowered
                        or "höjd" in lowered
                    ):
                        continue
                    data_col_idx = idx
                    data_col_name = name
                    break
            continue

        date_value = first
        time_value = None
        datetime_match = DATETIME_RE.match(first)
        if datetime_match:
            date_value = datetime_match.group(1)
            time_value = datetime_match.group(2)
        elif not DATE_RE.match(first):
            continue

        value = row[data_col_idx].strip() if data_col_idx is not None and data_col_idx < len(row) else None
        yield {
            "family_id": family,
            "parameter_key": parameter_key,
            "station_key": station_key,
            "period_key": period_key,
            "date": date_value,
            "time": (
                row[time_idx].strip()
                if time_idx is not None and time_idx < len(row)
                else time_value
            ),
            "value": value,
            "quality": (
                row[quality_idx].strip()
                if quality_idx is not None and quality_idx < len(row)
                else None
            ),
            "value_column": data_col_name,
            "raw_columns": header,
            "raw_row": row,
        }


def _fragment_key(parameter_key: str, station_key: str) -> str:
    return f"p-{parameter_key}-s-{station_key}"


def _write_station_observation_fragment(
    node_id: str,
    family: str,
    parameter_key: str,
    station_key: str,
    detail: dict,
) -> int:
    base_url = FAMILIES[family]["base_url"]
    fetched_at = datetime.now(timezone.utc).isoformat()
    count = 0
    with raw_writer(
        node_id,
        OBSERVATION_EXT,
        mode="wt",
        compression="gzip",
        fragment=_fragment_key(parameter_key, station_key),
    ) as out:
        for period in detail.get("period") or []:
            period_key = period.get("key")
            if not period_key:
                continue
            url = (
                f"{base_url}/version/1.0/parameter/{parameter_key}/station/"
                f"{station_key}/period/{period_key}/data.csv"
            )
            text = _fetch_data_text(url)
            if text is None:
                continue
            for row in _csv_data_rows(text, family, parameter_key, station_key, str(period_key)):
                row["fetched_at"] = fetched_at
                out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                count += 1
    return count


def _write_observations(node_id: str, family: str) -> bool:
    done = set(list_raw_fragments(node_id, OBSERVATION_EXT).keys())
    station_refs = list(_iter_station_refs(family))
    worklist = [
        (parameter_key, station_key)
        for parameter_key, station_key, _station in station_refs
        if _fragment_key(parameter_key, station_key) not in done
    ]
    started = time.monotonic()
    rows_written = 0
    processed = 0

    for parameter_key, station_key in worklist:
        if processed and time.monotonic() - started > OBSERVATION_NODE_BUDGET_S:
            print(
                f"  -> {node_id}: observation leg budget spent after "
                f"{processed:,} station fragment(s), {rows_written:,} row(s); continuing"
            )
            return True
        detail = _station_detail(family, parameter_key, station_key)
        rows_written += _write_station_observation_fragment(
            node_id,
            family,
            parameter_key,
            station_key,
            detail,
        )
        processed += 1

    if not station_refs:
        raise RuntimeError(f"{node_id}: no observation stations discovered")
    committed = set(list_raw_fragments(node_id, OBSERVATION_EXT).keys())
    if not committed and rows_written == 0:
        raise RuntimeError(f"{node_id}: no observation rows fetched")
    return False


def fetch_one(node_id: str) -> bool | None:
    entity_id = _entity_from_node_id(node_id)
    family = _family_from_entity(entity_id)
    if entity_id.endswith("-parameters"):
        save_raw_ndjson(_parameter_rows(family), node_id)
    elif entity_id.endswith("-stations"):
        save_raw_ndjson(_station_rows(family), node_id)
    elif entity_id.endswith("-observations"):
        return _write_observations(node_id, family)
    else:
        raise ValueError(f"Unhandled SMHI entity id: {entity_id}")
    return None


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"smhi-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]


def _maintain_ext(asset_id: str) -> str:
    return OBSERVATION_EXT if asset_id.endswith("-observations") else "ndjson.zst"


def _maintain_max_age_days(asset_id: str) -> int:
    if asset_id.endswith("-observations"):
        return FRESH_OBSERVATION_MAX_AGE_DAYS
    return FRESH_REFERENCE_MAX_AGE_DAYS


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"smhi-{entity_id.lower().replace('_', '-')}",
        description=(
            "SMHI open-data API is continuously updated for observations and "
            "catalog metadata; refresh observations weekly and reference "
            "catalogs monthly (cadence inferred from https://opendata.smhi.se/)."
        ),
        check=lambda aid: raw_asset_exists(
            aid,
            _maintain_ext(aid),
            max_age_days=_maintain_max_age_days(aid),
        ),
    )
    for entity_id in ENTITY_IDS
]
