"""Download specs for Statistics Portugal (INE) indicator tables.

Mechanism: the public INE JSON indicator endpoint
`/ine/json_indicador/pindica.jsp?op=2&varcd={varcd}&Dim1=T&lang=EN`.
Each accepted INE indicator is its own cross-tabulated dataset, so the connector
emits one download node per accepted indicator. The shared fetch function writes
one long NDJSON raw asset per indicator: one row per (indicator, period,
geography, extra-dimension tuple).
"""
from __future__ import annotations

from constants import ENTITY_IDS, SLUG
from nodes.statistics_portugal_fetch import fetch_indicator
from subsets_utils import NodeSpec


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id.lower().replace('_', '-')}", fn=fetch_indicator, kind="download")
    for entity_id in ENTITY_IDS
]
