"""Canonical INEGI download node module."""

from subsets_utils import NodeSpec

from nodes.catalog import fetch_catalog as _fetch_catalog
from nodes.values import fetch_values as _fetch_values


def fetch_catalog(node_id: str) -> None:
    _fetch_catalog(node_id)


def fetch_values(node_id: str) -> None:
    _fetch_values(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="inegi-indicators", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-topics", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-units", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-frequencies", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-sources", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-geo-areas", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-values", fn=fetch_values, kind="download"),
]
