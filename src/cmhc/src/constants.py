"""Dataset-id selections for the cmhc connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "34100096", "34100097", "34100098", "34100099", "34100103",
    "34100108", "34100127", "34100128", "34100129", "34100130",
    "34100132", "34100133", "34100135", "34100136", "34100137",
    "34100138", "34100139", "34100140", "34100141", "34100142",
    "34100143", "34100145", "34100147", "34100148", "34100149",
    "34100150", "34100151", "34100152", "34100153", "34100154",
    "34100155", "34100157", "34100159", "34100161", "34100162",
]
