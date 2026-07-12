"""Sveriges Riksbank SWEA download specs."""

from subsets_utils import NodeSpec

from nodes.groups import fetch_groups
from nodes.series import fetch_series
from nodes.values import fetch_values

DOWNLOAD_SPECS = [
    NodeSpec(id="sveriges-riksbank-groups", fn=fetch_groups, kind="download"),
    NodeSpec(id="sveriges-riksbank-series", fn=fetch_series, kind="download"),
    NodeSpec(id="sveriges-riksbank-values", fn=fetch_values, kind="download"),
]
