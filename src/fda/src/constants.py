"""Dataset-id selections for the fda connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "animalandveterinary-event",
    "cosmetic-event",
    "device-510k",
    "device-classification",
    "device-enforcement",
    "device-pma",
    "device-recall",
    "device-registrationlisting",
    "device-udi",
    "drug-drugsfda",
    "drug-enforcement",
    "drug-label",
    "drug-ndc",
    "drug-shortages",
    "food-enforcement",
    "food-event",
    "other-nsde",
    "other-substance",
    "tobacco-problem",
]
