"""India-WRIS catalog constants — data, not logic.

THEMES maps each rank-active observation theme (collect entity id) to the
WRIS dashboard module path it is fetched from and the measuring agency/agencies
to query. The `stations` entity is a reference catalog handled by its own
fetcher and is intentionally absent here.

The module path is the human-readable string after `/Dataset/` (e.g.
`/Dataset/Ground Water Level`). Agencies are the upstream `agencyName` filter
values; an empty string queries the module without an agency filter.
"""

# Earliest date we attempt to pull. WRIS dynamic data generally starts in the
# 1970s-1990s depending on theme; this is a conservative floor. The end of the
# window is "today", discovered at runtime — never a hardcoded end year.
SOURCE_MIN_DATE = "1970-01-01"

THEMES = {
    "rainfall": {
        "module": "RainFall",
        "agencies": ["CWC", "IMD"],
    },
    "ground-water-level": {
        "module": "Ground Water Level",
        "agencies": ["CGWB"],
    },
    "river-water-level": {
        "module": "River Water Level",
        "agencies": ["CWC"],
    },
    "river-water-discharge": {
        "module": "River Water Discharge",
        "agencies": ["CWC"],
    },
    "reservoir": {
        "module": "Reservoir",
        "agencies": ["CWC"],
    },
    "ground-water-quality": {
        "module": "Ground Water Quality",
        "agencies": ["CGWB"],
    },
    "surface-water-quality": {
        "module": "Surface Water Quality",
        "agencies": ["CWC"],
    },
    "evapotranspiration": {
        "module": "Evapotranspiration",
        "agencies": ["NRSC", "IMD", ""],
    },
    "soil-moisture": {
        "module": "Soil Moisture",
        "agencies": ["NRSC", "IMD", ""],
    },
    "well-level-minor-irrigation": {
        "module": "Well Level (Minor Irrigation)",
        "agencies": ["CGWB", ""],
    },
}

# Dataset codes used by the station-master endpoints, paired with the agency
# that operates that network. Used only by the `stations` reference fetcher.
STATION_DATASETS = [
    ("RAINFALL", "IMD"),
    ("GWATERLVL", "CGWB"),
    ("RIVERWLVL", "CWC"),
    ("RIVERDISC", "CWC"),
    ("RESERVOIR", "CWC"),
]

# All collect entity ids (themes + stations) — the authoritative coverage set.
ENTITY_IDS = list(THEMES.keys()) + ["stations"]
