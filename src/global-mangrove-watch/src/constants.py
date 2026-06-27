SLUG = "global-mangrove-watch"

# Widget entity ids — these are the collect entity ids AND the API route names
# (/api/v2/widgets/<id>?location_id=<numeric id>). The `locations` reference
# catalog is handled by its own fetch fn, so it is NOT in this list.
WIDGET_IDS = [
    "aboveground_biomass",
    "biodiversity",
    "blue-carbon-investment",
    "blue_carbon",
    "degradation-and-loss",
    "drivers_of_change",
    "ecoregions",
    "ecosystem_services",
    "fisheries",
    "fishery_mitigation_potentials",
    "habitat_extent",
    "international_status",
    "mitigation_potentials",
    "net_change",
    "protected-areas",
    "restoration-potential",
    "tree_height",
]
