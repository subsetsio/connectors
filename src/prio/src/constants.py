"""Dataset-id selections for the prio connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "1", "3", "4", "5", "6", "7", "8", "10", "11", "14",
    "16", "18", "20", "23", "26", "28", "29", "30", "31", "32",
    "34", "35", "36", "37", "38", "39", "40",
]
