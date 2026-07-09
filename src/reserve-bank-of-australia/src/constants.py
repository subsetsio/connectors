"""Dataset-id selections for the reserve-bank-of-australia connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    'a1-data', 'a2-data', 'a3-daily-open-market-operations',
    'a3-es-balances-and-repo-agreements', 'a3-long-dated-open-mkt-operations',
    'a3-omo-outright-transaction-detail', 'a3-omo-repo-transaction-details',
    'a3-omo-repo-unwinds', 'a3-short-dated-liquidity-mgmt', 'a3-term-funding-facility',
    'a3-term-funding-facility-unwinds', 'a3-us-dollar-repo-operations', 'a3.1-act',
    'a3.1-ags---bonds', 'a3.1-ags---notes', 'a3.1-nswtc', 'a3.1-nt', 'a3.1-qtc', 'a3.1-safa',
    'a3.1-summary', 'a3.1-tasc', 'a3.1-tcv', 'a3.1-watc', 'a3.2-rba-securities-lending',
    'a3.2-rba-switches', 'a4-data', 'a5-data', 'a6-data-from-1984', 'a6-data-prior-to-1984',
    'a7-data', 'b1-data', 'b10-data', 'b10-series-breaks', 'b11.1-assets', 'b11.1-liabilities',
    'b11.1-series-breaks', 'b11.2-exposures-in-aud-terms', 'b11.2-exposures-in-usd-terms',
    'b11.2-series-breaks', 'b12.1-data', 'b12.1-series-breaks', 'b12.1.1',
    'b12.1.1-series-breaks', 'b12.1.1-summary', 'b12.2-data', 'b12.2-series-breaks', 'b12.2.1',
    'b12.2.1-series-breaks', 'b12.2.1-summary', 'b13.1-data', 'b13.1-series-breaks', 'b13.1.1',
    'b13.1.1-series-breaks', 'b13.1.1-summary', 'b13.1.2', 'b13.1.2-series-breaks',
    'b13.1.2-summary', 'b13.2-data', 'b13.2-series-breaks', 'b13.2.1', 'b13.2.1-series-breaks',
    'b13.2.1-summary', 'b2-data', 'b2-series-breaks', 'b20-data',
    'b3-repo-and-securities-lending', 'c1-data', 'c1-series-breaks', 'c1.1-aggregate',
    'c1.1-device-not-present', 'c1.1-device-present', 'c1.1-series-breaks', 'c1.2-data',
    'c1.2-series-breaks', 'c2-data', 'c2-series-breaks', 'c2.1-aggregate',
    'c2.1-device-not-present', 'c2.1-device-present', 'c2.1-series-breaks', 'c2.2-aggregate',
    'c2.2-by-card-type', 'c2.2-series-breaks', 'c3-data', 'c3-series-breaks', 'c4-data',
    'c4-series-breaks', 'c4.1-data', 'c4.1-series-breaks', 'c5-data', 'c5-series-breaks',
    'c5.1-data', 'c5.1-series-breaks', 'c6-data', 'c6-series-breaks', 'c6.1-data',
    'c6.1-series-breaks', 'c7-data', 'c9-data', 'd1-data', 'd10-data', 'd10-series-breaks',
    'd11-data', 'd12-data', 'd13-data', 'd14-data', 'd14.1-data', 'd2-data',
    'd2-series-breaks', 'd3-data', 'd3-series-breaks', 'd4-data', 'd5-data',
    'd5-series-breaks', 'd9-data', 'e1-data', 'e13-data', 'e2-data', 'e3-2002', 'e3-2006',
    'e3-2010', 'e3-2014', 'e4-2002', 'e4-2006', 'e4-2010', 'e4-2014', 'e5-2002', 'e5-2006',
    'e5-2010', 'e5-2014', 'e6-2002', 'e6-2006', 'e6-2010', 'e6-2014', 'e7-2002', 'e7-2006',
    'e7-2010', 'e7-2014', 'f1-data', 'f1-use-of-expert-judgement', 'f1.1-data', 'f10-data',
    'f11.1-data', 'f12-data', 'f15-data', 'f16-data', 'f17-discount-factors',
    'f17-forward-rates', 'f17-yields', 'f2-data', 'f2.1-data', 'f3-data', 'f4-data',
    'f4-series-breaks', 'f4.1-data', 'f5-data', 'f5-series-breaks', 'f6-data', 'f7-data',
    'f8-data', 'f9-data', 'g1-data', 'g2-data', 'g3-data', 'g4-data', 'h1-data', 'h2-data',
    'h3-data', 'h4-data', 'h5-data', 'i1-data', 'i2-data', 'i3-data', 'i4-data', 'i5-data',
    'j1-forecasts', 'j1-historical---brent-oil-price', 'j1-historical---twi',
    'j1-star-variables',
]
