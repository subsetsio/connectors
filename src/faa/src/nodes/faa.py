from subsets_utils import NodeSpec

from nodes.arcgis import _ARCGIS_SERVICES
from nodes.arcgis import TRANSFORM_SPECS as ARCGIS_TRANSFORM_SPECS
from nodes.arcgis import fetch_arcgis as _fetch_arcgis
from nodes.registry import _REGISTRY_MEMBERS
from nodes.registry import TRANSFORM_SPECS as REGISTRY_TRANSFORM_SPECS
from nodes.registry import fetch_registry as _fetch_registry


def fetch_registry(node_id: str) -> None:
    _fetch_registry(node_id)


def fetch_arcgis(node_id: str) -> None:
    _fetch_arcgis(node_id)

DOWNLOAD_SPECS = [
    *[NodeSpec(id=sid, fn=fetch_registry, kind="download") for sid in _REGISTRY_MEMBERS],
    *[NodeSpec(id=sid, fn=fetch_arcgis, kind="download") for sid in _ARCGIS_SERVICES],
]

TRANSFORM_SPECS = [
    *REGISTRY_TRANSFORM_SPECS,
    *ARCGIS_TRANSFORM_SPECS,
]
