"""DHS country reference table."""
from __future__ import annotations

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

COUNTRIES_URL = f"{BASE}/countries"


def fetch_countries(node_id: str) -> None:
    records = fetch_all(COUNTRIES_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-countries", fn=fetch_countries, kind="download"),
]
