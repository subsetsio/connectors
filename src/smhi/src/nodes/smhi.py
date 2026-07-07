import csv
import io
import json
import re
from datetime import datetime, timezone

from constants import ENTITY_IDS, FAMILIES
from subsets_utils import NodeSpec, get, raw_writer, save_raw_ndjson, transient_retry


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@transient_retry()
def _fetch_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text.lstrip("\ufeff")


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
            if first.startswith("Datum"):
                header = [cell.strip() for cell in row]
                for idx, name in enumerate(header):
                    lowered = name.lower()
                    if lowered.startswith("tid"):
                        time_idx = idx
                    elif lowered == "kvalitet":
                        quality_idx = idx
                for idx, name in enumerate(header):
                    lowered = name.lower()
                    if not name or lowered.startswith("datum") or lowered.startswith("tid"):
                        continue
                    if lowered == "kvalitet" or lowered.startswith("tidsutsnitt"):
                        continue
                    data_col_idx = idx
                    data_col_name = name
                    break
            continue

        if not DATE_RE.match(first):
            continue

        value = row[data_col_idx].strip() if data_col_idx is not None and data_col_idx < len(row) else None
        yield {
            "family_id": family,
            "parameter_key": parameter_key,
            "station_key": station_key,
            "period_key": period_key,
            "date": first,
            "time": row[time_idx].strip() if time_idx is not None and time_idx < len(row) else None,
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


def _write_observations(node_id: str, family: str) -> None:
    base_url = FAMILIES[family]["base_url"]
    fetched_at = datetime.now(timezone.utc).isoformat()
    count = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for parameter_key, station_key, _station in _iter_station_refs(family):
            detail = _station_detail(family, parameter_key, station_key)
            for period in detail.get("period") or []:
                period_key = period.get("key")
                if not period_key:
                    continue
                url = (
                    f"{base_url}/version/1.0/parameter/{parameter_key}/station/"
                    f"{station_key}/period/{period_key}/data.csv"
                )
                text = _fetch_text(url)
                for row in _csv_data_rows(text, family, parameter_key, station_key, str(period_key)):
                    row["fetched_at"] = fetched_at
                    out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                    count += 1
    if count == 0:
        raise RuntimeError(f"{node_id}: no observation rows fetched")


def fetch_one(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    family = _family_from_entity(entity_id)
    if entity_id.endswith("-parameters"):
        save_raw_ndjson(_parameter_rows(family), node_id)
    elif entity_id.endswith("-stations"):
        save_raw_ndjson(_station_rows(family), node_id)
    elif entity_id.endswith("-observations"):
        _write_observations(node_id, family)
    else:
        raise ValueError(f"Unhandled SMHI entity id: {entity_id}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"smhi-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
