"""EPO country metadata (countries-metadata.json)."""

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_countries(node_id: str) -> None:
    """countries-metadata.json: a flat list of country records."""
    data = fetch_json("countries-metadata.json")
    save_raw_ndjson(data, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="epo-countries", fn=fetch_countries, kind="download"),
]
