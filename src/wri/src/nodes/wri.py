"""Download specs for WRI Climate Watch datasets."""

from subsets_utils import NodeSpec

from nodes.content import fetch_content
from nodes.emissions import fetch_emissions
from nodes.sdg import fetch_sdg


DOWNLOAD_SPECS = [
    NodeSpec(id="wri-historical-emissions", fn=fetch_emissions, kind="download"),
    NodeSpec(id="wri-ndc-content", fn=fetch_content, kind="download"),
    NodeSpec(id="wri-ndc-sdg", fn=fetch_sdg, kind="download"),
    NodeSpec(id="wri-net-zero-content", fn=fetch_content, kind="download"),
]
