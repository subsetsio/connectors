"""Download specs for the US Drought Monitor connector."""

from subsets_utils import NodeSpec

from nodes.drought_severity import fetch_drought_severity
from nodes.dsci import fetch_dsci


DOWNLOAD_SPECS = [
    NodeSpec(
        id="us-drought-monitor-drought-severity",
        fn=fetch_drought_severity,
        kind="download",
    ),
    NodeSpec(
        id="us-drought-monitor-dsci",
        fn=fetch_dsci,
        kind="download",
    ),
]
