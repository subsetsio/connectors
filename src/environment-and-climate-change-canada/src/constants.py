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
