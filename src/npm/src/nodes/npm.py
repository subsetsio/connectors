"""Download specs for the npm Registry connector."""
from subsets_utils import NodeSpec

from nodes.daily_downloads import fetch_daily_downloads
from nodes.package_inventory import fetch_package_inventory
from nodes.package_versions import fetch_package_versions
from nodes.popular_packages import fetch_popular_packages
from nodes.registry_stats import fetch_registry_stats


DOWNLOAD_SPECS = [
    NodeSpec(id="npm-daily-downloads", fn=fetch_daily_downloads, kind="download"),
    NodeSpec(id="npm-package-inventory", fn=fetch_package_inventory, kind="download"),
    NodeSpec(id="npm-package-versions", fn=fetch_package_versions, kind="download"),
    NodeSpec(id="npm-popular-packages", fn=fetch_popular_packages, kind="download"),
    NodeSpec(id="npm-registry-stats", fn=fetch_registry_stats, kind="download"),
]
