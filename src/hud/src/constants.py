"""Dataset-id selections for the hud connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "aaf",
    "cdbg-income-limits",
    "chas",
    "fmr",
    "fmr-50th-percentile",
    "home-income-limits",
    "home-rent-limits",
    "htf-income-limits",
    "htf-rent-limits",
    "income-limits",
    "mtsp-income-limits",
    "muaf",
    "picture-of-subsidized-households",
    "qct-dda",
    "safmr",
]
