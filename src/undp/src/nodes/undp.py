"""UNDP download specs."""
from subsets_utils import NodeSpec

from nodes.composite_indices import fetch_composite_indices
from nodes.mpi import fetch_mpi


DOWNLOAD_SPECS = [
    NodeSpec(id="undp-composite-indices", fn=fetch_composite_indices, kind="download"),
    NodeSpec(id="undp-mpi", fn=fetch_mpi, kind="download"),
]
