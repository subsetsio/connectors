"""Met Office historic station download specs."""

from subsets_utils import NodeSpec

from nodes.observations import fetch_observations
from nodes.stations import fetch_stations


DOWNLOAD_SPECS = [
    NodeSpec(id="met-office-observations", fn=fetch_observations, kind="download"),
    NodeSpec(id="met-office-stations", fn=fetch_stations, kind="download"),
]
