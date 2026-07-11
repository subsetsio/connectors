"""DOWNLOAD_SPECS for the ITU DataHub connector."""

from subsets_utils import NodeSpec

from nodes.categories import fetch_categories
from nodes.countries import fetch_countries
from nodes.datasets import fetch_datasets
from nodes.indicators import fetch_indicators
from nodes.values import fetch_values

DOWNLOAD_SPECS = [
    NodeSpec(id="itu-categories", fn=fetch_categories, kind="download"),
    NodeSpec(id="itu-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="itu-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="itu-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="itu-values", fn=fetch_values, kind="download"),
]
