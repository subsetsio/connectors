"""USA National Phenology Network connector.

The observation service exposes filtered POST endpoints rather than a single
bulk dump. For the four observation products we fetch full snapshots partitioned
by calendar year and write one NDJSON fragment per year. The service labels the
streaming endpoints `.ndjson`, but representative responses are JSON arrays, so
the fetcher normalizes those arrays into one JSON object per line as it streams.

Reference catalogs are small enough to fetch in memory and save as NDJSON.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import xml.etree.ElementTree as ET

import httpx

from subsets_utils import NodeSpec, get, get_client, raw_writer, save_raw_ndjson

SLUG = "usa-npn"
BASE = "https://services.usanpn.org/npn_portal/"
GEOSERVER_WMS = "https://geoserver.usanpn.org/geoserver/wms?request=GetCapabilities"
REQUEST_SOURCE = "subsets.io connector"
START_YEAR = 1955

OBSERVATION_ENDPOINTS = {
    "status-intensity-observations": "observations/getObservations.json",
    "individual-phenometrics": "observations/getSummarizedData.json",
    "site-phenometrics": "observations/getSiteLevelData.json",
    "magnitude-phenometrics": "observations/getMagnitudeData.json",
}

REFERENCE_ENDPOINTS = {
    "species": "species/getSpecies.json",
    "phenophases": "phenophases/getPhenophases.json",
    "partner-groups": "networks/getPartnerNetworks.json",
}

ENTITY_IDS = [
    "geospatial-layers",
    "individual-phenometrics",
    "magnitude-phenometrics",
    "partner-groups",
    "phenophases",
    "site-phenometrics",
    "species",
    "status-intensity-observations",
]


def _entity_id_from_node(node_id: str) -> str:
    return node_id[len(SLUG) + 1 :]


def _json_rows(path: str) -> list[dict]:
    resp = get(BASE + path, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise RuntimeError(f"{path} returned {type(data).__name__}, expected list")
    return data


def _write_json_array_as_ndjson(response: httpx.Response, out) -> int:
    decoder = json.JSONDecoder()
    buffer = ""
    started = False
    rows = 0

    for chunk in response.iter_text():
        buffer += chunk
        while True:
            buffer = buffer.lstrip()
            if not started:
                if not buffer:
                    break
                if buffer[0] != "[":
                    raise RuntimeError(f"expected JSON array, saw {buffer[:40]!r}")
                buffer = buffer[1:]
                started = True
                continue

            buffer = buffer.lstrip()
            if buffer.startswith(","):
                buffer = buffer[1:]
                continue
            if buffer.startswith("]"):
                return rows
            if not buffer:
                break

            try:
                obj, idx = decoder.raw_decode(buffer)
            except ValueError:
                break
            out.write(json.dumps(obj, separators=(",", ":")) + "\n")
            rows += 1
            buffer = buffer[idx:]

    if not started:
        raise RuntimeError("response ended before JSON array started")
    if buffer.strip() not in {"", "]"}:
        raise RuntimeError(f"trailing unparsed JSON after stream end: {buffer[:80]!r}")
    return rows


def _stream_observation_year(asset_id: str, endpoint: str, year: int) -> int:
    data = {
        "request_src": REQUEST_SOURCE,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
    }
    if endpoint.endswith("getSiteLevelData.json"):
        data["num_days_quality_filter"] = "30"
    if endpoint.endswith("getMagnitudeData.json"):
        data["frequency"] = "30"

    timeout = httpx.Timeout(1800.0, connect=30.0, read=1800.0, write=30.0)
    with get_client().stream("POST", BASE + endpoint, data=data, timeout=timeout) as resp:
        resp.raise_for_status()
        with raw_writer(asset_id, "ndjson.gz", mode="wt", compression="gzip", fragment=str(year)) as out:
            return _write_json_array_as_ndjson(resp, out)


def _fetch_observation_product(node_id: str, entity_id: str) -> None:
    endpoint = OBSERVATION_ENDPOINTS[entity_id]
    current_year = dt.date.today().year
    total_rows = 0
    for year in range(START_YEAR, current_year + 1):
        total_rows += _stream_observation_year(node_id, endpoint, year)
    if total_rows == 0:
        raise RuntimeError(f"{entity_id} returned zero rows across {START_YEAR}-{current_year}")


def _fetch_reference(node_id: str, entity_id: str) -> None:
    rows = _json_rows(REFERENCE_ENDPOINTS[entity_id])
    if not rows:
        raise RuntimeError(f"{entity_id} reference endpoint returned no rows")
    save_raw_ndjson(rows, node_id)


def _fetch_geospatial_layers(node_id: str) -> None:
    resp = get(GEOSERVER_WMS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"wms": "http://www.opengis.net/wms"}
    rows = []
    for layer in root.findall(".//wms:Layer/wms:Layer", ns):
        name = layer.findtext("wms:Name", default="", namespaces=ns)
        if not name:
            continue
        dimension = layer.find("wms:Dimension", ns)
        rows.append(
            {
                "name": name,
                "title": layer.findtext("wms:Title", default="", namespaces=ns),
                "abstract": layer.findtext("wms:Abstract", default="", namespaces=ns),
                "dimension_name": dimension.get("name") if dimension is not None else None,
                "dimension_values": (dimension.text or "").strip() if dimension is not None else None,
            }
        )
    if len(rows) < 10:
        raise RuntimeError(f"GeoServer capabilities returned only {len(rows)} layers")
    save_raw_ndjson(rows, node_id)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    if entity_id in OBSERVATION_ENDPOINTS:
        _fetch_observation_product(node_id, entity_id)
    elif entity_id in REFERENCE_ENDPOINTS:
        _fetch_reference(node_id, entity_id)
    elif entity_id == "geospatial-layers":
        _fetch_geospatial_layers(node_id)
    else:
        raise KeyError(entity_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
