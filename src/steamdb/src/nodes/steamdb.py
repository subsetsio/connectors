"""SteamDB download specs.

Fetch implementations live in per-entity helper modules; this file is the
single harness-facing owner of DOWNLOAD_SPECS.
"""

from subsets_utils import NodeSpec

from nodes.app_details import fetch_app_details
from nodes.app_reviews import fetch_app_reviews
from nodes.concurrent_players import fetch_concurrent_players
from nodes.most_played import fetch_most_played
from nodes.top_releases import fetch_top_releases


DOWNLOAD_SPECS = [
    NodeSpec(id="steamdb-app-details", fn=fetch_app_details, kind="download"),
    NodeSpec(id="steamdb-app-reviews", fn=fetch_app_reviews, kind="download"),
    NodeSpec(id="steamdb-concurrent-players", fn=fetch_concurrent_players, kind="download"),
    NodeSpec(id="steamdb-most-played", fn=fetch_most_played, kind="download"),
    NodeSpec(id="steamdb-top-releases", fn=fetch_top_releases, kind="download"),
]
