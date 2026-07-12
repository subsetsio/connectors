"""Download specs for Transparency International CPI tables."""

from subsets_utils import NodeSpec

from nodes.cpi_latest_detail import fetch_latest_detail
from nodes.cpi_regional_averages import fetch_regional
from nodes.cpi_timeseries import fetch_timeseries


DOWNLOAD_SPECS = [
    NodeSpec(
        id="transparency-international-cpi-latest-detail",
        fn=fetch_latest_detail,
        kind="download",
    ),
    NodeSpec(
        id="transparency-international-cpi-regional-averages",
        fn=fetch_regional,
        kind="download",
    ),
    NodeSpec(
        id="transparency-international-cpi-timeseries",
        fn=fetch_timeseries,
        kind="download",
    ),
]
