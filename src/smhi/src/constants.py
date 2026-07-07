ENTITY_IDS = [
    "hydroobs-observations",
    "hydroobs-parameters",
    "hydroobs-stations",
    "metobs-observations",
    "metobs-parameters",
    "metobs-stations",
    "ocobs-observations",
    "ocobs-parameters",
    "ocobs-stations",
]

FAMILIES = {
    "metobs": {
        "label": "meteorological",
        "base_url": "https://opendata-download-metobs.smhi.se/api",
    },
    "hydroobs": {
        "label": "hydrological",
        "base_url": "https://opendata-download-hydroobs.smhi.se/api",
    },
    "ocobs": {
        "label": "oceanographic",
        "base_url": "https://opendata-download-ocobs.smhi.se/api",
    },
}
