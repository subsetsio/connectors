"""CFTC Commitments of Traders download nodes."""
from subsets_utils import NodeSpec

from utils import fetch_family


FAMILY_RESOURCES = {
    "cftc-disaggregated": ("72hh-3qpy", "kh3c-gbw2"),
    "cftc-legacy": ("6dca-aqww", "jun7-fc8e"),
    "cftc-supplemental-cit": ("4zgm-a668",),
    "cftc-tff": ("gpe5-46if", "yw9f-hn96"),
}


def fetch(node_id: str) -> None:
    fetch_family(node_id, list(FAMILY_RESOURCES[node_id]))


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch, kind="download")
    for spec_id in FAMILY_RESOURCES
]
