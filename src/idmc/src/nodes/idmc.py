"""IDMC download specs."""

from subsets_utils import NodeSpec

from nodes.conflicts import fetch_conflicts
from nodes.disaggregations import fetch_disaggregations
from nodes.disasters import fetch_disasters
from nodes.displacements import fetch_displacements
from nodes.idu import fetch_idu
from nodes.public_figure_analyses import fetch_public_figure_analyses


DOWNLOAD_SPECS = [
    NodeSpec(id="idmc-conflicts", fn=fetch_conflicts, kind="download"),
    NodeSpec(id="idmc-disaggregations", fn=fetch_disaggregations, kind="download"),
    NodeSpec(id="idmc-disasters", fn=fetch_disasters, kind="download"),
    NodeSpec(id="idmc-displacements", fn=fetch_displacements, kind="download"),
    NodeSpec(id="idmc-idu", fn=fetch_idu, kind="download"),
    NodeSpec(
        id="idmc-public-figure-analyses",
        fn=fetch_public_figure_analyses,
        kind="download",
    ),
]
