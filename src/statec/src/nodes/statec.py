"""STATEC LUSTAT SDMX downloads.

Each accepted collect entity is one SDMX dataflow. Schemas vary by dataflow,
so the download stage preserves the source SDMX-CSV response as raw CSV and
the transform stage profiles each table from observed raw.
"""

from urllib.parse import quote

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_file

BASE_URL = "https://lustat.statec.lu/rest"
SLUG = "statec"

CSV_HEADERS = {
    "Accept": "application/vnd.sdmx.data+csv;urn=true;file=true;labels=both",
    "Accept-Language": "en",
}

_SPEC_SUFFIX_TO_ENTITY_ID = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}


def _entity_id_from_spec(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected STATEC node id: {node_id}")
    suffix = node_id.removeprefix(prefix)
    return _SPEC_SUFFIX_TO_ENTITY_ID[suffix]


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_spec(node_id)
    dataflow = quote(entity_id, safe="")
    url = f"{BASE_URL}/data/LU1,{dataflow}/all"
    response = get(
        url,
        headers=CSV_HEADERS,
        params={"dimensionAtObservation": "AllDimensions"},
        timeout=300.0,
    )
    response.raise_for_status()

    content = response.content
    head = content[:2048].decode("utf-8-sig", "replace")
    if "OBS_VALUE" not in head or "\n" not in head:
        raise ValueError(f"{entity_id}: response does not look like SDMX-CSV")

    save_raw_file(content, node_id, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
