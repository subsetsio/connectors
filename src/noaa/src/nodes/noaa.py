"""NOAA download specs.

The dataset-specific fetch implementations live in sibling modules to keep the
large source-specific parsing code readable; this module is the harness-facing
download spec manifest.
"""

from subsets_utils import NodeSpec

from nodes.international_best_track_archive_for_climate_stewardship_ibtracs import (
    fetch_ibtracs,
)
from nodes.northeast_snowfall_impact_scale import fetch_nesis
from nodes.nws_public_forecast_zone_codebook import (
    fetch_nws_public_forecast_zone_codebook,
)
from nodes.regional_snowfall_index import fetch_rsi
from nodes.storm_events import fetch_storm_events


DOWNLOAD_SPECS = [
    NodeSpec(
        id="noaa-international-best-track-archive-for-climate-stewardship-ibtracs",
        fn=fetch_ibtracs,
        kind="download",
    ),
    NodeSpec(
        id="noaa-northeast-snowfall-impact-scale",
        fn=fetch_nesis,
        kind="download",
    ),
    NodeSpec(
        id="noaa-nws-public-forecast-zone-codebook",
        fn=fetch_nws_public_forecast_zone_codebook,
        kind="download",
    ),
    NodeSpec(
        id="noaa-regional-snowfall-index",
        fn=fetch_rsi,
        kind="download",
    ),
    NodeSpec(
        id="noaa-storm-events",
        fn=fetch_storm_events,
        kind="download",
    ),
]
