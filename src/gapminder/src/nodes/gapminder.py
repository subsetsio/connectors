"""Download specs for the Gapminder connector."""

from subsets_utils import NodeSpec

from nodes.concepts import fetch_concepts
from nodes.values import fetch_values


DOWNLOAD_SPECS = [
    NodeSpec(id="gapminder-concepts", fn=fetch_concepts, kind="download"),
    NodeSpec(id="gapminder-values", fn=fetch_values, kind="download"),
]
