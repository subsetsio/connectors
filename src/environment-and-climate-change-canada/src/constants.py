"""Data, not logic: the accepted collect entities for this connector.

Each id is an OGC API Features collection on https://api.weather.gc.ca.
Copied from data/sources/environment-and-climate-change-canada/work/entity_union.json.
"""

ENTITY_IDS = [
    "ahccd-annual",
    "ahccd-monthly",
    "ahccd-seasonal",
    "ahccd-stations",
    "ahccd-trends",
    "aqhi-forecasts-realtime",
    "aqhi-observations-realtime",
    "aqhi-stations",
    "citypageweather-realtime",
    "climate-daily",
    "climate-monthly",
    "climate-normals",
    "climate-stations",
    "datasets-footprints",
    "hurricanes-cyclone-realtime",
    "hurricanes-error_cone-realtime",
    "hurricanes-track-realtime",
    "hurricanes-wind_radii-realtime",
    "hydrometric-annual-peaks",
    "hydrometric-annual-statistics",
    "hydrometric-monthly-mean",
    "hydrometric-stations",
    "ltce-precipitation",
    "ltce-snowfall",
    "ltce-stations",
    "ltce-temperature",
    "marine-standard-forecast-zones",
    "marineweather-realtime",
    "metnotes",
    "public-standard-forecast-zones",
    "swob-marine-stations",
    "swob-partner-stations",
    "swob-stations",
    "thunderstorm_outlook",
    "weather-alerts",
]
