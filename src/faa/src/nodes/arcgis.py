"""FAA AIS ArcGIS Hub — eight tabular aeronautical FeatureServer datasets.

services6.arcgis.com FeatureServers expose eight tabular aeronautical datasets
(airports, runways, navaids, frequencies, ILS, obstacles, designated points).
Pulled via the ArcGIS REST query API, OBJECTID-ordered offset pagination,
geometry dropped, saved as NDJSON (each layer has its own column set, so no
shared parquet schema).

Whole-corpus snapshot with no incremental filter, so the fetch shape is
stateless full re-pull + overwrite.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import faa_get

_ARCGIS_HOST = "https://services6.arcgis.com/ssFJjBXIUyZDrSYZ/arcgis/rest/services"

# download spec id -> FeatureServer service name (layer 0 on each)
_ARCGIS_SERVICES = {
    "faa-airports": "US_Airport",
    "faa-runways": "Runways",
    "faa-navaid-system": "NAVAIDSystem",
    "faa-navaid-component": "NavaidComponents",
    "faa-digital-obstacle-file": "Digital_Obstacle_File",
    "faa-frequency": "Frequencies",
    "faa-ils-system": "ILSSystemNew",
    "faa-designated-point": "DesignatedPoints",
}

_PAGE = 1000          # <= every layer's maxRecordCount (min observed 1000)
_MAX_PAGES = 100_000  # safety ceiling; raises (never silently truncates)


def _iter_features(service: str):
    """Yield attribute dicts for every feature, OBJECTID-ordered offset paging."""
    base = f"{_ARCGIS_HOST}/{service}/FeatureServer/0/query"
    offset = 0
    pages = 0
    while True:
        pages += 1
        if pages > _MAX_PAGES:
            raise RuntimeError(f"{service}: exceeded {_MAX_PAGES} pages — source grew unexpectedly")
        data = faa_get(
            base,
            params={
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "false",
                "orderByFields": "OBJECTID",
                "resultOffset": str(offset),
                "resultRecordCount": str(_PAGE),
                "f": "json",
            },
        ).json()
        if "error" in data:
            raise RuntimeError(f"{service}: ArcGIS error {data['error']}")
        feats = data.get("features", [])
        for feat in feats:
            yield feat.get("attributes", {})
        if not feats:
            break
        offset += len(feats)
        if not data.get("exceededTransferLimit") and len(feats) < _PAGE:
            break


def fetch_arcgis(node_id: str) -> None:
    asset = node_id
    service = _ARCGIS_SERVICES[node_id]
    save_raw_ndjson(_iter_features(service), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_arcgis, kind="download") for sid in _ARCGIS_SERVICES
]

# ArcGIS layers are already typed via JSON; publish the attribute table as-is.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{sid}-transform",
        deps=[sid],
        sql=f'SELECT * FROM "{sid}"',
    )
    for sid in _ARCGIS_SERVICES
]
