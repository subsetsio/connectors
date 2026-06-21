"""Dataset-id selections for the fcc connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "2ra3-4jd4", "3b3k-34jp", "3xyp-aqkj", "6nz8-czf5", "9wyt-yvgw",
    "a6ec-cry4", "acbv-jbb4", "bzun-59r8", "dpq5-ta9j", "emke-zy79",
    "euz5-46g2", "ijjn-36q8", "m7z2-kzex", "qqhe-xtyw", "s8yu-gdgv",
    "sh3h-3cea", "xqgr-24et", "yd9y-6jqe",
]
