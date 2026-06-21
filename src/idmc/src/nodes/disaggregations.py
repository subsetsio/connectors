"""IDMC disaggregations — full disaggregated, geo-located figures (~48.7k features).

The GeoJSON endpoint 302s to a short-lived pre-signed S3 URL serving a gzip
GeoJSON FeatureCollection (httpx follows the redirect and decompresses
transparently).
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import BASE, CLIENT_ID, get_json, join_field

_DISAGG_RENAME = {
    "ID": "id", "ISO3": "iso3", "Country": "country",
    "Geographical region": "geographical_region", "Figure cause": "figure_cause",
    "Year": "year", "Figure category": "figure_category", "Figure unit": "figure_unit",
    "Reported figures": "reported_figures", "Total figures": "total_figures",
    "Violence type": "violence_type", "Start date": "start_date",
    "Start date accuracy": "start_date_accuracy", "End date": "end_date",
    "End date accuracy": "end_date_accuracy", "Publishers": "publishers",
    "Sources": "sources", "Sources type": "sources_type", "Event ID": "event_id",
    "Event name": "event_name", "Event cause": "event_cause",
    "Event main trigger": "event_main_trigger", "Event start date": "event_start_date",
    "Event end date": "event_end_date", "Is housing destruction": "is_housing_destruction",
    "Event codes (Code:Type)": "event_codes", "Locations name": "locations_name",
    "Locations accuracy": "locations_accuracy", "Locations type": "locations_type",
    "Displacement occurred": "displacement_occurred",
}
# Array-valued properties that must be collapsed to scalar strings.
_DISAGG_ARRAY_FIELDS = {
    "publishers", "sources", "sources_type", "event_codes",
    "locations_name", "locations_accuracy", "locations_type",
}


def _first_coord(geometry: dict | None):
    """Return (longitude, latitude) of the first point of a (Multi)Point, or (None, None)."""
    if not geometry:
        return None, None
    coords = geometry.get("coordinates")
    while isinstance(coords, list) and coords and isinstance(coords[0], list):
        coords = coords[0]
    if isinstance(coords, list) and len(coords) >= 2:
        return coords[0], coords[1]
    return None, None


def fetch_disaggregations(node_id: str) -> None:
    gj = get_json(f"{BASE}/gidd/disaggregations/disaggregation-geojson/", {"client_id": CLIENT_ID})
    features = gj.get("features", []) if isinstance(gj, dict) else []
    if not features:
        raise AssertionError("disaggregation-geojson: no features in FeatureCollection")
    rows = []
    for feat in features:
        props = feat.get("properties", {}) or {}
        row = {}
        for src, dst in _DISAGG_RENAME.items():
            val = props.get(src)
            row[dst] = join_field(val) if dst in _DISAGG_ARRAY_FIELDS else val
        geom = feat.get("geometry") or {}
        lon, lat = _first_coord(geom)
        row["longitude"] = lon
        row["latitude"] = lat
        row["geometry_type"] = geom.get("type")
        rows.append(row)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="idmc-disaggregations", fn=fetch_disaggregations, kind="download"),
]

_SQL_DISAGG = """
SELECT
    CAST(id AS BIGINT) AS id,
    iso3,
    country,
    geographical_region,
    figure_cause,
    CAST(year AS INTEGER) AS year,
    figure_category,
    figure_unit,
    CAST(reported_figures AS BIGINT) AS reported_figures,
    CAST(total_figures AS BIGINT) AS total_figures,
    violence_type,
    TRY_CAST(start_date AS DATE) AS start_date,
    start_date_accuracy,
    TRY_CAST(end_date AS DATE) AS end_date,
    end_date_accuracy,
    publishers,
    sources,
    sources_type,
    CAST(event_id AS BIGINT) AS event_id,
    event_name,
    event_cause,
    event_main_trigger,
    TRY_CAST(event_start_date AS DATE) AS event_start_date,
    TRY_CAST(event_end_date AS DATE) AS event_end_date,
    is_housing_destruction,
    event_codes,
    locations_name,
    locations_accuracy,
    locations_type,
    displacement_occurred,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(latitude AS DOUBLE) AS latitude,
    geometry_type
FROM "idmc-disaggregations"
WHERE id IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(id="idmc-disaggregations-transform", deps=["idmc-disaggregations"], sql=_SQL_DISAGG),
]
