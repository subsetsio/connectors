# Entity union — the rank-active collect entities (subsets to publish).
# Copied from data/sources/environment-and-climate-change-canada/work/entity_union.json.
# Each id is an MSC GeoMet OGC API Features collection id.
#
# Five firehose-scale collections (climate-daily 63M, climate-hourly 299M,
# hydrometric-daily-mean 69M, hydrometric-realtime 19M, swob-realtime 14M) were
# deferred at rank below the publish threshold: they require a station x year
# partitioned firehose that will not reliably complete in a single CI run via
# the JSON API. The 19 below all paginate to completion in minutes.
ENTITY_IDS = [
    "ahccd-annual",
    "ahccd-monthly",
    "ahccd-seasonal",
    "ahccd-stations",
    "ahccd-trends",
    "aqhi-observations-realtime",
    "aqhi-stations",
    "climate-monthly",
    "climate-normals",
    "climate-stations",
    "hydrometric-annual-peaks",
    "hydrometric-annual-statistics",
    "hydrometric-monthly-mean",
    "hydrometric-stations",
    "ltce-precipitation",
    "ltce-snowfall",
    "ltce-stations",
    "ltce-temperature",
    "swob-stations",
]

# Observation collections are fetched PER STATION, not by walking the whole
# collection with offset pagination. The GeoMet backend's offset pagination is
# O(offset): a deep page on a multi-million-row collection takes minutes
# (climate-monthly offset=1.9M measured at 161s), so a full crawl is unusable.
# Filtering to one station returns a small indexed result in ~0.1s, so we
# enumerate the stations from the companion station collection and pull each
# station's slice. Maps obs collection -> (filter_field, stations_collection,
# station_id_field). Every field verified live against /queryables + a filtered
# /items call. Collections NOT listed here (the *-stations reference tables) are
# small and fetched with plain shallow pagination.
STATION_PARTITIONS = {
    "climate-monthly":               ("CLIMATE_IDENTIFIER",  "climate-stations",     "CLIMATE_IDENTIFIER"),
    "climate-normals":               ("CLIMATE_IDENTIFIER",  "climate-stations",     "CLIMATE_IDENTIFIER"),
    "ahccd-annual":                  ("station_id__id_station", "ahccd-stations",    "station_id__id_station"),
    "ahccd-monthly":                 ("station_id__id_station", "ahccd-stations",    "station_id__id_station"),
    "ahccd-seasonal":                ("station_id__id_station", "ahccd-stations",    "station_id__id_station"),
    "ahccd-trends":                  ("station_id__id_station", "ahccd-stations",    "station_id__id_station"),
    "hydrometric-annual-peaks":      ("STATION_NUMBER",      "hydrometric-stations", "STATION_NUMBER"),
    "hydrometric-annual-statistics": ("STATION_NUMBER",      "hydrometric-stations", "STATION_NUMBER"),
    "hydrometric-monthly-mean":      ("STATION_NUMBER",      "hydrometric-stations", "STATION_NUMBER"),
    "ltce-precipitation":            ("VIRTUAL_CLIMATE_ID",  "ltce-stations",        "VIRTUAL_CLIMATE_ID"),
    "ltce-snowfall":                 ("VIRTUAL_CLIMATE_ID",  "ltce-stations",        "VIRTUAL_CLIMATE_ID"),
    "ltce-temperature":              ("VIRTUAL_CLIMATE_ID",  "ltce-stations",        "VIRTUAL_CLIMATE_ID"),
    "aqhi-observations-realtime":    ("location_id",         "aqhi-stations",        "location_id"),
}
