"""Dataset-id selections for the bls connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "ap", "bd", "ca", "ce", "ci", "cm", "cu", "cw", "cx", "ei",
    "ep", "fa", "fm", "ip", "is", "jt", "kv", "la", "le", "ln",
    "lu", "mp", "nb", "nd", "oe", "or", "pc", "pr", "sm", "su",
    "tu", "wm", "wp", "ws",
]
