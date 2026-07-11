"""IDMC public figure analyses - methodology and caveats per country-year-cause."""

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_gidd


def fetch_public_figure_analyses(node_id: str) -> None:
    save_raw_ndjson(fetch_gidd("public-figure-analyses"), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="idmc-public-figure-analyses",
        fn=fetch_public_figure_analyses,
        kind="download",
    ),
]
