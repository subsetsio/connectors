"""Dataset-id selections for the bank-of-israel connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "ACC", "ATM", "BBS_99", "BFR_99", "BIR", "BIR_MRTG_99", "BKN", "BMB_99",
    "BOP", "BR", "BTS_7", "CAP", "CARDS", "CCIR", "CCP", "CHEQUES", "CONS",
    "DEBT_AGG", "DEM", "DRV", "ECON_IND", "ENR", "EXR", "EXS", "FTR", "INSINV",
    "INSINV2", "LBM", "MAG", "MASAV", "MF", "MNF", "NA", "PRI", "PS",
    "REAL_ES_DF", "REV", "SECDWH", "TLB", "ZAHAV", "ZCM",
]
