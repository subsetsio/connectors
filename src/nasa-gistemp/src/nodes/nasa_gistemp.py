"""Download specs for NASA GISTEMP v4."""

from subsets_utils import NodeSpec

from nodes.annual import fetch_annual
from nodes.monthly import fetch_monthly
from nodes.zonal_annual import fetch_zonal_annual


DOWNLOAD_SPECS = [
    NodeSpec(id="nasa-gistemp-annual", fn=fetch_annual, kind="download"),
    NodeSpec(id="nasa-gistemp-monthly", fn=fetch_monthly, kind="download"),
    NodeSpec(id="nasa-gistemp-zonal-annual", fn=fetch_zonal_annual, kind="download"),
]
