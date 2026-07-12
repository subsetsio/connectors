from subsets_utils import MaintainSpec, NodeSpec, raw_asset_exists

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

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "StatCounter Global Stats is updated monthly, usually near the "
            "start of the month; skip a recent committed parquet asset."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=31),
    )
    for spec in DOWNLOAD_SPECS
]
