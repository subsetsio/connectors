"""FAA AIS ArcGIS Hub core tabular aeronautical FeatureServer datasets.

services6.arcgis.com FeatureServers expose the core tabular aeronautical
datasets (airports, runways, navaids, frequencies, ILS, obstacles, designated
points). Pull via the ArcGIS REST query API, OBJECTID-ordered offset
pagination, geometry dropped, saved as NDJSON.

Whole-corpus snapshot with no incremental filter, so the fetch shape is
stateless full re-pull + overwrite.
"""

import time

from subsets_utils import save_raw_ndjson
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

_PAGE = 1000
_MAX_PAGES = 100_000
_MAX_QUERY_ATTEMPTS = 6
_RATE_LIMIT_SLEEP_S = 65


def _query_page(service: str, base: str, offset: int) -> dict:
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "orderByFields": "OBJECTID",
        "resultOffset": str(offset),
        "resultRecordCount": str(_PAGE),
        "f": "json",
    }
    for attempt in range(1, _MAX_QUERY_ATTEMPTS + 1):
        data = faa_get(base, params=params).json()
        error = data.get("error")
        if not error:
            return data
        if error.get("code") != 429 or attempt == _MAX_QUERY_ATTEMPTS:
            raise RuntimeError(f"{service}: ArcGIS error {error}")
        time.sleep(_RATE_LIMIT_SLEEP_S)
    raise AssertionError("unreachable")


def _iter_features(service: str):
    """Yield attribute dicts for every feature, OBJECTID-ordered offset paging."""
    base = f"{_ARCGIS_HOST}/{service}/FeatureServer/0/query"
    offset = 0
    pages = 0
    while True:
        pages += 1
        if pages > _MAX_PAGES:
            raise RuntimeError(f"{service}: exceeded {_MAX_PAGES} pages - source grew unexpectedly")
        data = _query_page(service, base, offset)
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
