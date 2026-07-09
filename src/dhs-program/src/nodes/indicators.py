"""DHS indicator catalog (single page, perpage=5000)."""
from __future__ import annotations

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

INDICATORS_URL = f"{BASE}/indicators"


def fetch_indicators(node_id: str) -> None:
    records = fetch_all(INDICATORS_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-indicators", fn=fetch_indicators, kind="download"),
]
