from subsets_utils import NodeSpec

from nodes.screen_resolution import fetch_resolution as _fetch_resolution
from nodes.timeseries import STATS, fetch_statistic as _fetch_statistic


def fetch_statistic(node_id: str) -> None:
    _fetch_statistic(node_id)


def fetch_resolution(node_id: str) -> None:
    _fetch_resolution(node_id)


DOWNLOAD_SPECS = [
    *(NodeSpec(id=f"statcounter-{entity_id}", fn=fetch_statistic, kind="download") for entity_id in STATS),
    NodeSpec(id="statcounter-screen-resolution", fn=fetch_resolution, kind="download"),
]
