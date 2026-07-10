"""Static catalog data for the Global Volcanism Program connector.

ENTITY_IDS are the rank-accepted GeoServer feature-layer names (the local part
of each WFS typeName, under the GVP-VOTW workspace). The node module turns each
into one download spec and one published Delta table.
"""

WORKSPACE = "GVP-VOTW"

ENTITY_IDS = [
    "Smithsonian_VOTW_Holocene_Volcanoes",
    "Smithsonian_VOTW_Holocene_Eruptions",
    "Smithsonian_VOTW_Pleistocene_Volcanoes",
    "E3WebApp_HoloceneVolcanoes",
    "E3WebApp_Eruptions1960",
    "E3WebApp_Emissions",
]
