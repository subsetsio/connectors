"""Dataset-id selections for the bis connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "WS_CBPOL",
    "WS_CBS_PUB",
    "WS_CBTA",
    "WS_CPMI_CASHLESS",
    "WS_CPMI_CT1",
    "WS_CPMI_CT2",
    "WS_CPMI_DEVICES",
    "WS_CPMI_INSTITUT",
    "WS_CPMI_MACRO",
    "WS_CPMI_PARTICIP",
    "WS_CPMI_SYSTEMS",
    "WS_CPP",
    "WS_CREDIT_GAP",
    "WS_DEBT_SEC2_PUB",
    "WS_DER_OTC_TOV",
    "WS_DPP",
    "WS_DSR",
    "WS_EER",
    "WS_GLI",
    "WS_LBS_D_PUB",
    "WS_LONG_CPI",
    "WS_NA_SEC_DSS",
    "WS_OTC_DERIV2",
    "WS_SPP",
    "WS_TC",
    "WS_XRU",
    "WS_XTD_DERIV",
]
