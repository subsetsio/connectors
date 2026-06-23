"""Dataset-id selections for the ism connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "bacord",
    "buypol",
    "cusinv",
    "employment",
    "imports",
    "inventories",
    "newexpord",
    "neword",
    "nm-bacord",
    "nm-busact",
    "nm-employment",
    "nm-imports",
    "nm-inventories",
    "nm-invsen",
    "nm-newexpord",
    "nm-neword",
    "nm-pmi",
    "nm-prices",
    "nm-supdel",
    "pmi",
    "prices",
    "production",
    "supdel",
]
