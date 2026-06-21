"""Dataset-id selections for the meta connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "climate-change-opinion-survey",
    "commuting-zones",
    "cross-gender-ties",
    "facebook-business-activity-trends-during-covid19",
    "facebook-business-activity-trends-during-crisis",
    "future-of-business-survey-aggregated-data",
    "international-migration-flows",
    "long-ties-data",
    "movement-distribution",
    "movement-range-maps",
    "relative-wealth-index",
    "social-capital-atlas",
    "social-connectedness-index",
    "social-connections-survey",
    "survey-on-gender-equality-at-home",
    "uk-social-capital-atlas",
]
