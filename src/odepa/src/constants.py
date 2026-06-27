"""Entity union for the ODEPA connector (copied from the rank-accepted set).

ENTITY_IDS is the authoritative coverage target. ENTITY_SPECS maps each entity to
the CKAN package it lives in plus an optional trade-flow filter — `comercio-exterior`
is split into two subsets (exports / imports) because their column lists differ.
"""

ENTITY_IDS = [
    "catastro-fruticola",
    "comercio-exterior-exportaciones",
    "comercio-exterior-importaciones",
    "precios-consumidor",
    "precios-mayoristas-de-flores-y-follajes",
    "precios-mayoristas-de-frutas-y-hortalizas",
    "precios-uva-vinificacion",
]

# entity_id -> {"package": <ckan package slug>, "flow": <substring filter or None>}
ENTITY_SPECS = {
    "catastro-fruticola": {"package": "catastro-fruticola", "flow": None},
    "comercio-exterior-exportaciones": {"package": "comercio-exterior", "flow": "exporta"},
    "comercio-exterior-importaciones": {"package": "comercio-exterior", "flow": "importa"},
    "precios-consumidor": {"package": "precios-consumidor", "flow": None},
    "precios-mayoristas-de-flores-y-follajes": {"package": "precios-mayoristas-de-flores-y-follajes", "flow": None},
    "precios-mayoristas-de-frutas-y-hortalizas": {"package": "precios-mayoristas-de-frutas-y-hortalizas", "flow": None},
    "precios-uva-vinificacion": {"package": "precios-uva-vinificacion", "flow": None},
}
