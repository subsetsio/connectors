"""National Interagency Fire Center (NIFC) connector — downloads.

NIFC publishes its authoritative interagency wildland-fire data through ArcGIS
feature services hosted in its ArcGIS Online org (org id T4QMspbfLg3qTGWY;
MODIS/VIIRS hotspots live in separate Esri Living-Atlas orgs). Each accepted
subset is one ArcGIS FeatureServer/Table *layer* with its own column schema.

Mechanism (from research): `arcgis_rest`. The accepted entity union is the set
of specific `<itemid>-<layer>` layers; `src/constants.py` maps each to its live
FeatureServer URL + sublayer index (resolved at build time from the ArcGIS
sharing content API). Each layer is queried at `<url>/<layer>/query` with
`where=1=1, outFields=*, returnGeometry=false, f=json`, paginated by
`resultOffset` in steps of `resultRecordCount` until the server stops setting
`exceededTransferLimit`. No auth, no documented rate limit.

Fetch shape: stateless full re-pull. Every refresh re-pulls each layer in full
and overwrites downstream — layers are at most ~1.2M rows and re-pulling is
cheap relative to maintaining a watermark, and it picks up upstream revisions
for free. Raw is streamed to gzip-compressed NDJSON: the attribute records are
wide (13-150+ fields) and heterogeneous across the 94 layers, so NDJSON beats a
fixed parquet schema and keeps memory flat on the large layers. ArcGIS date
fields arrive as epoch-millisecond integers and are converted downstream in the
transform SQL.
"""
import json
from functools import lru_cache

from subsets_utils import NodeSpec, get, raw_writer, transient_retry

from constants import LAYERS

SLUG = "nifc"
PREFIX = f"{SLUG}-"

# Default page size. The core NIFC org caps maxRecordCount at 2000; the
# Living-Atlas hotspot orgs (services9.arcgis.com) allow far larger pages, so
# the ~1.2M-row VIIRS layer pages in bigger chunks.
_DEFAULT_PAGE = 2000
_BIG_PAGE = 16000

# Safety ceiling: the largest layer (VIIRS, ~1.2M rows) is ~76 pages at
# 16000/page. This cap only fires if a source grows far beyond expectation; it
# raises (never silently truncates) so unexpected growth is surfaced.
MAX_PAGES = 20000


def _page_size(url: str) -> int:
    return _BIG_PAGE if "services9.arcgis.com" in url else _DEFAULT_PAGE


@transient_retry()
def _layer_info(layer_url: str, layer: int) -> dict:
    resp = get(
        f"{layer_url}/{layer}",
        params={"f": "json"},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"{layer_url}/{layer}: ArcGIS layer metadata error {data['error']}")
    return data


@lru_cache(maxsize=None)
def _object_id_field(layer_url: str, layer: int) -> str:
    info = _layer_info(layer_url, layer)
    field = info.get("objectIdField") or (info.get("uniqueIdField") or {}).get("name")
    if not field:
        raise RuntimeError(f"{layer_url}/{layer}: ArcGIS layer metadata lacks object id field")
    return field


@transient_retry()
def _query(layer_url: str, layer: int, page: int, offset: int, order_field: str) -> dict:
    resp = get(
        f"{layer_url}/{layer}/query",
        params={
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "orderByFields": order_field,
            "resultRecordCount": page,
            "resultOffset": offset,
            "f": "json",
        },
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Re-pull one ArcGIS layer in full and stream its attributes to NDJSON."""
    eid = node_id[len(PREFIX):]
    spec = LAYERS[eid]
    url, layer = spec["url"], spec["layer"]
    page = _page_size(url)
    order_field = _object_id_field(url, layer)

    offset = 0
    pages = 0
    total = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        while True:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{node_id}: hit MAX_PAGES={MAX_PAGES} at offset {offset} — "
                    "source larger than expected; raise the cap intentionally"
                )
            data = _query(url, layer, page, offset, order_field)
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(f"{node_id}: ArcGIS query error {data['error']}")
            feats = data.get("features", [])
            if not feats:
                break
            for f in feats:
                attrs = f.get("attributes")
                if attrs:
                    out.write(json.dumps(attrs, separators=(",", ":")) + "\n")
                    total += 1
            pages += 1
            offset += len(feats)
            # exceededTransferLimit drops once the final page is served.
            if not data.get("exceededTransferLimit"):
                break
    print(f"  {node_id}: wrote {total:,} records over {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in LAYERS
]
