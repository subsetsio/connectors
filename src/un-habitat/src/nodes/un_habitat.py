from __future__ import annotations

import io
import math
import tempfile
import zipfile
from datetime import date, datetime
from pathlib import Path

import pyogrio

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson

SLUG = "un-habitat"
PREFIX = f"{SLUG}-"
ARCGIS_ITEM = "https://www.arcgis.com/sharing/rest/content/items/{item_id}"
USER_AGENT = "subsets.io un-habitat connector"


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}; expected prefix {PREFIX!r}")
    return node_id[len(PREFIX):]


def _json_get(url: str, **params) -> dict:
    resp = get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=120.0)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"ArcGIS request failed for {url}: {data['error']!r}")
    return data


def _item(item_id: str) -> dict:
    return _json_get(ARCGIS_ITEM.format(item_id=item_id), f="json")


def _item_data(item_id: str) -> bytes:
    resp = get(
        f"{ARCGIS_ITEM.format(item_id=item_id)}/data",
        headers={"User-Agent": USER_AGENT},
        timeout=300.0,
    )
    resp.raise_for_status()
    return resp.content


def _clean_value(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _with_provenance(item: dict, source_kind: str, source_name: str, row_number: int, attrs: dict) -> dict:
    out = {
        "source_item_id": item["id"],
        "source_title": item.get("title") or item["id"],
        "source_type": item.get("type"),
        "source_kind": source_kind,
        "source_name": source_name,
        "source_row_number": row_number,
    }
    for key, value in attrs.items():
        out[str(key)] = _clean_value(value)
    return out


def _rows_from_arrow(item: dict, source_kind: str, source_name: str, meta: dict, table) -> list[dict]:
    geometry_name = meta.get("geometry_name")
    rows = []
    for row_number, row in enumerate(table.to_pylist(), start=1):
        attrs = {k: v for k, v in row.items() if k != geometry_name}
        rows.append(_with_provenance(item, source_kind, source_name, row_number, attrs))
    return rows


def _read_vector_path(path: Path, item: dict, source_kind: str, source_name: str | None = None) -> list[dict]:
    rows = []
    layers = pyogrio.list_layers(path)
    for layer_name, _geometry_type in layers:
        meta, table = pyogrio.read_arrow(path, layer=layer_name)
        rows.extend(_rows_from_arrow(item, source_kind, str(layer_name), meta, table))
    if not rows:
        raise RuntimeError(f"{item['id']}: no rows read from {source_name or path.name}")
    return rows


def _read_archive(item: dict, content: bytes) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            zf.extractall(root)

        rows = []
        gdbs = list(root.rglob("*.gdb"))
        if gdbs:
            for gdb in gdbs:
                rows.extend(_read_vector_path(gdb, item, "file_geodatabase", gdb.name))
            return rows

        shapefiles = list(root.rglob("*.shp"))
        if shapefiles:
            for shp in shapefiles:
                rows.extend(_read_vector_path(shp, item, "shapefile", shp.name))
            return rows

    raise RuntimeError(f"{item['id']}: archive did not contain a readable File Geodatabase or Shapefile")


def _rectangularize_rows(rows: list[dict]) -> list[dict]:
    keys = list(dict.fromkeys(key for row in rows for key in row))
    return [{key: row.get(key) for key in keys} for row in rows]


def _service_layers(service_url: str) -> list[dict]:
    service = _json_get(service_url, f="json")
    return list(service.get("layers") or []) + list(service.get("tables") or [])


def _query_service_layer(item: dict, service_url: str, layer: dict) -> list[dict]:
    layer_id = layer["id"]
    layer_name = layer.get("name") or str(layer_id)
    layer_url = f"{service_url.rstrip('/')}/{layer_id}/query"
    rows = []
    offset = 0
    page_size = 2000

    while True:
        data = _json_get(
            layer_url,
            f="json",
            where="1=1",
            outFields="*",
            returnGeometry="false",
            resultOffset=offset,
            resultRecordCount=page_size,
        )
        features = data.get("features") or []
        for feature in features:
            rows.append(
                _with_provenance(
                    item,
                    "feature_service",
                    layer_name,
                    len(rows) + 1,
                    feature.get("attributes") or {},
                )
            )
        if not data.get("exceededTransferLimit") and len(features) < page_size:
            break
        if not features:
            break
        offset += len(features)

    return rows


def _read_feature_service(item: dict) -> list[dict]:
    service_url = item.get("url")
    if not service_url:
        raise RuntimeError(f"{item['id']}: Feature Service item has no service URL")
    rows = []
    for layer in _service_layers(service_url):
        rows.extend(_query_service_layer(item, service_url, layer))
    if not rows:
        raise RuntimeError(f"{item['id']}: no rows returned from Feature Service")
    return rows


def fetch_one(node_id: str) -> None:
    item_id = _entity_id(node_id)
    item = _item(item_id)
    item_type = item.get("type")

    if item_type == "Feature Service":
        rows = _read_feature_service(item)
    elif item_type in {"File Geodatabase", "Shapefile"}:
        rows = _read_archive(item, _item_data(item_id))
    else:
        raise RuntimeError(f"{item_id}: unsupported ArcGIS item type {item_type!r}")

    rows = _rectangularize_rows(rows)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
