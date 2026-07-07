"""Download specs for the UNESCO Institute for Statistics connector."""
from subsets_utils import NodeSpec

from nodes.geounits import fetch_geounits
from nodes.indicators import fetch_indicators
from nodes.values import fetch_values
from utils import SLUG


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-geounits", fn=fetch_geounits, kind="download"),
    NodeSpec(id=f"{SLUG}-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id=f"{SLUG}-values", fn=fetch_values, kind="download"),
]
