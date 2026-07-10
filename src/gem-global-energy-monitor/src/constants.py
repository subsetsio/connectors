"""Dataset-id selections for the gem-global-energy-monitor connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "bioenergy-tracker", "cement-concrete-tracker", "chemicals-inventory",
    "coal-mine-tracker", "coal-plant-tracker", "coal-project-finance-tracker",
    "coal-terminal-tracker", "energy-ownership-tracker", "gas-finance-tracker",
    "gas-pipeline-tracker", "geothermal-tracker",
    "hydropower-tracker",
    "integrated-power-tracker", "iron-ore-mines-tracker", "iron-steel-iron-unit",
    "iron-steel-plant-tracker", "iron-steel-steel-unit",
    "latin-america-energy-tracker", "lng-terminal-tracker",
    "methane-emitters-tracker", "nuclear-power-tracker",
    "oil-gas-extraction-tracker", "oil-gas-plant-tracker", "oil-pipeline-tracker",
    "solar-power-tracker", "wind-power-tracker",
]
