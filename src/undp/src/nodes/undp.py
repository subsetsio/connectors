"""UNDP download specs."""
from subsets_utils import NodeSpec

from nodes.composite_indices import fetch_composite_indices
from nodes.indicators import fetch_indicators
from nodes.mpi import fetch_mpi


DOWNLOAD_SPECS = [
    NodeSpec(id="undp-composite-indices", fn=fetch_composite_indices, kind="download"),
    NodeSpec(id="undp-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="undp-mpi", fn=fetch_mpi, kind="download"),
]
