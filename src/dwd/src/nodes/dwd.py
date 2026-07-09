"""DWD download specs for the currently accepted CDC entities."""

from subsets_utils import NodeSpec

from nodes.regional import fetch_regional
from nodes.stations import fetch_stations


DOWNLOAD_SPECS = [
    NodeSpec(id="dwd-regional-annual", fn=fetch_regional, kind="download"),
    NodeSpec(id="dwd-regional-monthly", fn=fetch_regional, kind="download"),
    NodeSpec(id="dwd-regional-seasonal", fn=fetch_regional, kind="download"),
    NodeSpec(id="dwd-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = []
