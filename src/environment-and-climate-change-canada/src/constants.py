# Entity union — the rank-active collect entities (subsets to publish).
# Copied from data/sources/environment-and-climate-change-canada/work/entity_union.json.
# Each id is an MSC GeoMet OGC API Features collection id.
#
# Deferred at rank below the publish threshold (not built here):
#   - Five firehose-scale collections (climate-daily 63M, climate-hourly 299M,
#     hydrometric-daily-mean 69M, hydrometric-realtime 19M, swob-realtime 14M).
#   - Three >1M-row monthly collections (ahccd-monthly 1.37M, climate-monthly
#     1.9M, hydrometric-monthly-mean 2.26M): the GeoMet backend's offset
#     pagination is O(offset) — a deep page on a >1M-row collection takes
#     1-3 minutes (climate-monthly offset=1.9M measured at 161s), so a full
#     crawl is impractical, and per-station filtering triggers slow server-side
#     full scans on these collections. They need a province/year-partitioned or
#     bulk-datamart path a curator can add later.
#
# The 16 below all paginate to completion in well under ten minutes each via
# plain offset pagination (max offset ~593k for climate-normals).
ENTITY_IDS = [
    "ahccd-annual",
    "ahccd-seasonal",
    "ahccd-stations",
    "ahccd-trends",
    "aqhi-observations-realtime",
    "aqhi-stations",
    "climate-normals",
    "climate-stations",
    "hydrometric-annual-peaks",
    "hydrometric-annual-statistics",
    "hydrometric-stations",
    "ltce-precipitation",
    "ltce-snowfall",
    "ltce-stations",
    "ltce-temperature",
    "swob-stations",
]
