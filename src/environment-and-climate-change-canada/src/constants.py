"""Data, not logic: the accepted collect entities for this connector.

Each id is an OGC API Features collection on https://api.weather.gc.ca, except
`climate-daily`, which is fetched from the MSC Datamart bulk CSV mirror.
Copied from data/sources/environment-and-climate-change-canada/work/entity_union.json.
"""

ENTITY_IDS = [
    "ahccd-annual",
    "ahccd-monthly",
    "ahccd-seasonal",
    "ahccd-stations",
    "ahccd-trends",
    "aqhi-stations",
    "climate-daily",
    "climate-monthly",
    "climate-normals",
    "climate-stations",
    "datasets-footprints",
    "hydrometric-annual-peaks",
    "hydrometric-annual-statistics",
    "hydrometric-monthly-mean",
    "hydrometric-stations",
    "ltce-precipitation",
    "ltce-snowfall",
    "ltce-stations",
    "ltce-temperature",
    "marine-standard-forecast-zones",
    "public-standard-forecast-zones",
    "swob-marine-stations",
    "swob-partner-stations",
    "swob-stations",
]
