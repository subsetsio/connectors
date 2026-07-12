"""Download specs for the GitHub Advisory Database connector."""

from __future__ import annotations

from subsets_utils import NodeSpec

from nodes.advisories import fetch_advisories
from nodes.affected import fetch_affected


DOWNLOAD_SPECS = [
    NodeSpec(id="github-advisories", fn=fetch_advisories, kind="download"),
    NodeSpec(id="github-affected", fn=fetch_affected, kind="download"),
]
