"""Dataset-id selections for the oenb connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "100140001", "100140002", "11", "13", "18", "22", "23", "24", "2502",
    "2503", "2504", "3101", "3102", "3103", "3104", "318", "32", "321", "33",
    "34", "35", "41", "6", "74", "75", "8", "901", "902", "904", "905", "97",
]
