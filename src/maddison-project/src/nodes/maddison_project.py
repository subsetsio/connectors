"""Download specs for the Maddison Project connector."""

from subsets_utils import NodeSpec

from nodes.country_panel import fetch_country_panel
from nodes.regional_aggregates import fetch_regional_aggregates
from nodes.source_references import fetch_original_sources, fetch_sources

DOWNLOAD_SPECS = [
    NodeSpec(id="maddison-project-country-panel", fn=fetch_country_panel, kind="download"),
    NodeSpec(id="maddison-project-original-sources", fn=fetch_original_sources, kind="download"),
    NodeSpec(id="maddison-project-regional-aggregates", fn=fetch_regional_aggregates, kind="download"),
    NodeSpec(id="maddison-project-sources", fn=fetch_sources, kind="download"),
]
