"""Download specs for the active Crossref reference catalogs."""

from __future__ import annotations

from subsets_utils import NodeSpec

from nodes.registries import fetch_registry as _fetch_registry
from nodes.registries import fetch_types as _fetch_types


def fetch_registry(node_id: str) -> None:
    _fetch_registry(node_id)


def fetch_types(node_id: str) -> None:
    _fetch_types(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="crossref-funders", fn=fetch_registry, kind="download"),
    NodeSpec(id="crossref-journals", fn=fetch_registry, kind="download"),
    NodeSpec(id="crossref-members", fn=fetch_registry, kind="download"),
    NodeSpec(id="crossref-types", fn=fetch_types, kind="download"),
]
