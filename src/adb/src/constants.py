"""Dataset-id selections for the adb connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "EGELC_EG", "EGELC_ELC", "ENV_CC", "ENV_FW", "ENV_LD", "ENV_PN",
    "EO_NA_CONST_GDP_EXP", "EO_NA_CONST_GOD", "EO_NA_CONST_GOO",
    "EO_NA_CONST_GVA", "EO_NA_CURR_GDP_EXP", "EO_NA_CURR_GDP_SOD",
    "EO_NA_CURR_GDP_SOO", "EO_NA_CURR_GVA", "EO_NA_INV_FIN", "EO_PRIX",
    "GG_GF", "GG_GV", "GLB_BP", "GLB_CF", "GLB_EI", "GLB_ET", "GLB_IR",
    "GLB_TM", "MFP_MF", "MFP_PR", "MFP_XR", "PPL_LE", "PPL_POP", "PPL_POV",
    "PPL_SI", "SDG_01", "SDG_02", "SDG_03", "SDG_04", "SDG_05", "SDG_06",
    "SDG_07", "SDG_08", "SDG_09", "SDG_10", "SDG_11", "SDG_12", "SDG_13",
    "SDG_14", "SDG_15", "SDG_16", "SDG_17", "TC_COM", "TC_TR",
]
