"""Dataset-id selections for the central-bank-of-sri-lanka connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "kei-table-1", "kei-table-2", "kei-table-3", "kei-table-4", "kei-table-5",
    "kei-table-6", "kei-table-7", "kei-table-8", "kei-table-9", "table-1.1",
    "table-1.2", "table-1.3", "table-1.4", "table-1.5", "table-1.6",
    "table-1.7", "table-1.8", "table-1.9", "table-1.10", "table-1.11",
    "table-1.12", "table-1.13", "table-1.14", "table-1.15", "table-1.16",
    "table-1.17", "table-1.18", "table-1.19", "table-1.20", "table-1.21",
    "table-1.22", "table-1.23", "table-1.24", "table-1.27", "table-1.29",
    "table-1.30", "table-1.33", "table-1.34", "table-1.35", "table-1.36",
    "table-1.37", "table-1.38", "table-1.39", "table-1.40", "table-1.41",
    "table-1.42", "table-1.43", "table-2.1", "table-2.2", "table-2.3",
    "table-2.4", "table-2.5", "table-2.6", "table-2.7", "table-2.8",
    "table-2.9", "table-2.10", "table-2.11", "table-2.12", "table-2.13",
    "table-2.18", "table-2.19", "table-2.20", "table-2.23", "table-2.24",
    "table-2.25", "table-2.26", "table-2.27", "table-2.28", "table-2.29",
    "table-2.30", "table-2.37", "table-2.38", "table-2.41", "table-2.42",
    "table-2.44", "table-3.1", "table-3.2", "table-3.3", "table-3.4",
    "table-3.5", "table-3.6", "table-3.7", "table-3.8", "table-3.9",
    "table-3.10", "table-3.11", "table-3.12", "table-3.13", "table-3.14",
    "table-3.16", "table-3.17", "table-3.18", "table-3.20", "table-3.21",
    "table-3.22", "table-3.23", "table-3.24", "table-3.25", "table-3.26",
    "table-3.27", "table-3.28", "table-3.29", "table-3.30", "table-3.31",
    "table-3.32", "table-4.1", "table-4.2", "table-4.3", "table-4.4",
    "table-4.5", "table-4.6", "table-4.7", "table-4.8", "table-4.9",
    "table-4.10", "table-4.11", "table-4.12", "table-4.13", "table-4.14",
    "table-5.1", "table-5.2", "table-5.3", "table-5.5", "table-5.6",
    "table-5.7", "table-5.8", "table-6.1", "table-6.2", "table-6.3",
    "table-6.4", "table-6.5", "table-6.6", "table-6.7", "table-6.8",
    "table-6.9", "table-7.1", "table-7.2", "table-7.3", "table-7.4",
    "table-7.5", "table-7.6", "table-7.7", "table-7.8", "table-7.9",
    "table-7.10", "table-7.11", "table-7.12", "table-8.1", "table-8.2",
    "table-8.3", "table-8.4", "table-8.5", "table-8.6", "table-8.7",
    "table-8.9", "table-8.10",
]
