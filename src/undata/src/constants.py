"""Dataset-id selections for the undata connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "DF_SDG_GLH",
    "DF_SEEA_AEA",
    "DF_SEEA_ENERGY",
    "DF_UNDATA_COUNTRYDATA",
    "DF_UNDATA_ENERGY",
    "DF_UNDATA_MDG",
    "DF_UNDATA_WDI",
    "DF_UNData_EnergyBalance",
    "DF_UNData_UIS",
    "DF_UNData_UNFCC",
    "NASEC_IDCFINA_A",
    "NASEC_IDCFINA_Q",
    "NASEC_IDCNFSA_A",
    "NASEC_IDCNFSA_Q",
    "NA_MAIN",
]
