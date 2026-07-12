"""Canonical L2BEAT download spec module."""

from subsets_utils import NodeSpec

from nodes.activity import fetch_activity
from nodes.projects import fetch_projects
from nodes.tvs import fetch_tvs

DOWNLOAD_SPECS = [
    NodeSpec(id="l2beat-activity", fn=fetch_activity, kind="download"),
    NodeSpec(id="l2beat-projects", fn=fetch_projects, kind="download"),
    NodeSpec(id="l2beat-tvs", fn=fetch_tvs, kind="download"),
]
