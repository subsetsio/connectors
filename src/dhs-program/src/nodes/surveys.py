"""DHS survey catalog (single page, perpage=5000)."""
from __future__ import annotations

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

SURVEYS_URL = f"{BASE}/surveys"


def fetch_surveys(node_id: str) -> None:
    records = fetch_all(SURVEYS_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-surveys", fn=fetch_surveys, kind="download"),
]
