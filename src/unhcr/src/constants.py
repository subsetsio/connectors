# The entity union — copied from data/sources/unhcr/work/entity_union.json.
# Each id is also the API path under https://api.unhcr.org/population/v1/.
ENTITY_IDS = [
    "asylum-applications",
    "asylum-decisions",
    "countries",
    "demographics",
    "footnotes",
    "nowcasting",
    "population",
    "regions",
    "solutions",
    "years",
]

# Data endpoints return one row per (year, country-of-origin, country-of-asylum)
# tuple plus statistical-disaggregation measures. Reference endpoints are small
# lookup tables with no year/country grid.
REFERENCE_ENDPOINTS = frozenset({"countries", "footnotes", "regions", "years"})
