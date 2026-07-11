"""Dataset-id selections for the rbnz connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "B1", "B10", "B13", "B2", "B20", "B21", "B25", "B26", "B27", "B3", "B30", "B4", "B6", "B7",
    "C12", "C13", "C21", "C22", "C30", "C31", "C32", "C33", "C35", "C40", "C41",
    "C5", "C50", "C51", "C52", "C55", "C60", "C65", "C66", "C70", "C71",
    "D10", "D12", "D3", "D30", "D31", "D35", "D9",
    "E1", "E2", "F3", "F4", "F5", "H1", "H2", "H3", "J10", "J20",
    "L1", "L2", "L3",
    "M1", "M10", "M12", "M14", "M15", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",
    "R1", "R2", "R3",
    "S10", "S20", "S21", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37",
    "S40", "S41", "S42", "S45", "S46", "S50", "S51",
    "T1", "T11", "T21", "T31", "T4", "T40", "T41", "T42", "T43", "T44", "T45",
    "T46", "T47", "T48",
]
