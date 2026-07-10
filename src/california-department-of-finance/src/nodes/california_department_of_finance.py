"""California Department of Finance — Demographic Research Unit (DRU) data portal.

Mechanism: arcgis_rest. The DRU portal is an ArcGIS Online org (id
d9Au2j3KckAl7VOw, orgKey "cacensus"). Each rank-active entity is one hosted
ArcGIS Feature Service / Table holding a tabular demographic dataset (population
& housing estimates, PL94 census tabulations, wildfire housing-unit loss, ADU
changes). Per entity we:

  1. resolve the ArcGIS item id -> its FeatureServer service url (item.url),
  2. pick its single data layer/table (id 0 for every DRU item observed),
  3. page the layer's attributes as JSON (returnGeometry=false drops the
     point/polygon geometry, keeping only the statistical columns),
  4. save the rows as NDJSON — the 18 layers have heterogeneous schemas, so a
     per-entity explicit parquet schema buys nothing; NDJSON re-types on read.

Fetch shape: stateless full re-pull (shape 1). Each layer is small (tens to
~9k rows) and exposes no reliable last-modified field, so we re-fetch the whole
layer every run and overwrite. No watermark, no cursor.

Pagination: ArcGIS caps each response at the layer's maxRecordCount (1000 or
2000 here). We page with resultOffset and stop when the server clears
exceededTransferLimit (the canonical "no more records" signal), which is robust
to the per-layer cap. orderByFields pins the object-id field so offset paging is
stable across requests.
"""

from subsets_utils import NodeSpec, get, save_raw_ndjson
from constants import ENTITY_IDS

SLUG = "california-department-of-finance"
ITEM_URL = "https://www.arcgis.com/sharing/rest/content/items/{item_id}"
PAGE_SIZE = 1000          # <= every observed layer maxRecordCount
MAX_RECORDS = 2_000_000   # safety ceiling; raises rather than looping forever


def _get_json(url, params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    # ArcGIS returns HTTP 200 with an inline {"error": {...}} envelope.
    if isinstance(data, dict) and "error" in data and "features" not in data:
        raise RuntimeError(f"ArcGIS error for {url}: {data['error']}")
    return data


def _resolve_layer(item_id):
    """Return (service_url, layer_id, oid_field) for an ArcGIS item."""
    item = _get_json(ITEM_URL.format(item_id=item_id), {"f": "json"})
    service_url = item.get("url")
    if not service_url:
        raise RuntimeError(f"item {item_id} has no service url")
    root = _get_json(service_url, {"f": "json"})
    layers = root.get("layers") or []
    tables = root.get("tables") or []
    candidates = layers or tables
    if not candidates:
        raise RuntimeError(f"service {service_url} exposes no layers or tables")
    layer_id = candidates[0]["id"]
    meta = _get_json(f"{service_url}/{layer_id}", {"f": "json"})
    oid_field = meta.get("objectIdField") or "OBJECTID"
    return service_url, layer_id, oid_field


def _fetch_layer(service_url, layer_id, oid_field):
    """Page all attribute rows (no geometry) for one layer."""
    rows = []
    offset = 0
    while True:
        data = _get_json(
            f"{service_url}/{layer_id}/query",
            {
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "false",
                "orderByFields": oid_field,
                "resultOffset": offset,
                "resultRecordCount": PAGE_SIZE,
                "f": "json",
            },
        )
        feats = data.get("features") or []
        rows.extend(f.get("attributes", {}) for f in feats)
        if len(rows) > MAX_RECORDS:
            raise RuntimeError(
                f"{service_url}/{layer_id}: exceeded {MAX_RECORDS} rows — "
                "source grew unexpectedly or pagination is looping"
            )
        if not feats or not data.get("exceededTransferLimit"):
            break
        offset += len(feats)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    item_id = node_id[len(SLUG) + 1:]  # strip "california-department-of-finance-"
    service_url, layer_id, oid_field = _resolve_layer(item_id)
    rows = _fetch_layer(service_url, layer_id, oid_field)
    if not rows:
        raise RuntimeError(f"{asset}: layer returned 0 rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
