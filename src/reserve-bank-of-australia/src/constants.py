"""Dataset-id selections for the reserve-bank-of-australia connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "a1-data", "a2-data", "a3-daily-open-market-operations",
    "a3-es-balances-and-repo-agreements", "a3.1-summary", "a4-data", "a5-data",
    "a6-data-from-1984", "a6-data-prior-to-1984", "b1-data", "b10-data",
    "b11.1-assets", "b11.1-liabilities", "b11.2-exposures-in-aud-terms",
    "b11.2-exposures-in-usd-terms", "b12.1-data", "b12.1.1", "b12.1.1-summary",
    "b12.2-data", "b12.2.1", "b12.2.1-summary", "b13.1-data", "b13.1.1",
    "b13.1.1-summary", "b13.1.2", "b13.1.2-summary", "b13.2-data", "b13.2.1",
    "b13.2.1-summary", "b2-data", "b3-repo-and-securities-lending", "c1-data",
    "c1.1-aggregate", "c1.1-device-not-present", "c1.1-device-present",
    "c1.2-data", "c2-data", "c2.1-aggregate", "c2.1-device-not-present",
    "c2.1-device-present", "c2.2-aggregate", "c2.2-by-card-type", "c3-data",
    "c4-data", "c4.1-data", "c5-data", "c5.1-data", "c6-data", "c6.1-data",
    "c7-data", "c9-data", "d1-data", "d10-data", "d11-data", "d12-data",
    "d13-data", "d14-data", "d14.1-data", "d2-data", "d3-data", "d4-data",
    "d5-data", "e1-data", "e13-data", "e2-data", "f1-data", "f1.1-data",
    "f10-data", "f11.1-data", "f12-data", "f15-data", "f16-data",
    "f17-discount-factors", "f17-forward-rates", "f17-yields", "f2-data",
    "f2.1-data", "f3-data", "f4-data", "f4.1-data", "f5-data", "f6-data",
    "f7-data", "f8-data", "f9-data", "g1-data", "g2-data", "g3-data", "g4-data",
    "h1-data", "h2-data", "h3-data", "h4-data", "h5-data", "i1-data", "i2-data",
    "i3-data", "i4-data", "i5-data", "j1-forecasts",
]
