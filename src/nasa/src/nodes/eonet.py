"""Earth Observatory Natural Event Tracker (EONET).

Events flattened to one row per geometry point. Stateless full re-pull every run.
"""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_json

EONET_EVENTS = "https://eonet.gsfc.nasa.gov/api/v3/events"


def fetch_eonet(node_id: str) -> None:
    asset = node_id
    payload = get_json(EONET_EVENTS, {"status": "all"})
    events = payload.get("events") or []
    rows = []
    for ev in events:
        cats = ev.get("categories") or [{}]
        srcs = ev.get("sources") or [{}]
        cat = cats[0] if cats else {}
        src = srcs[0] if srcs else {}
        for geom in ev.get("geometry") or []:
            coords = geom.get("coordinates")
            lon = lat = None
            if geom.get("type") == "Point" and isinstance(coords, list) and len(coords) >= 2:
                try:
                    lon, lat = float(coords[0]), float(coords[1])
                except (TypeError, ValueError):
                    lon = lat = None
            rows.append({
                "event_id": ev.get("id"),
                "title": ev.get("title"),
                "category_id": cat.get("id"),
                "category_title": cat.get("title"),
                "source_id": src.get("id"),
                "closed": ev.get("closed"),
                "date": geom.get("date"),
                "geom_type": geom.get("type"),
                "longitude": lon,
                "latitude": lat,
                "magnitude_value": geom.get("magnitudeValue"),
                "magnitude_unit": geom.get("magnitudeUnit"),
            })
    if not rows:
        raise AssertionError(f"{asset}: EONET returned no event geometries")
    save_raw_ndjson(rows, asset)


_EONET_SQL = {
    "nasa-events": '''
        SELECT event_id, title, category_id, category_title, source_id,
               TRY_CAST(date AS TIMESTAMP) AS observed_at,
               geom_type, longitude, latitude,
               magnitude_value, magnitude_unit, closed
        FROM "nasa-events"
        WHERE date IS NOT NULL
    ''',
}


DOWNLOAD_SPECS = [
    NodeSpec(id="nasa-events", fn=fetch_eonet, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_EONET_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
