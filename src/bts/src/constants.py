"""Dataset-id selections for the bts connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "FGJ", "FGK", "FHK", "FIH", "FIL", "FIM", "FJD", "FJE", "FJH", "FKF",
    "FKG", "FKI", "FKJ", "FKK", "FKL", "FKM", "FLF", "FLM", "FMD", "FME",
    "FMF", "FMG", "FMH", "FMI", "FMJ", "FMK", "GDE", "GDF", "GDJ", "GDK",
    "GDL", "GDM", "GED", "GEE", "GEF", "GEH", "GFE", "GFH", "GFI", "GGD",
    "KKI",
]
