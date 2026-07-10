"""FCC connector: one Socrata CSV download per accepted dataset."""

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get_client, raw_writer

BASE = "https://opendata.fcc.gov/resource"
FULL_LIMIT = 200_000_000
CHUNK_SIZE = 1 << 20


def _dataset_id(node_id: str) -> str:
    return node_id.removeprefix("fcc-")


def fetch_one(node_id: str) -> None:
    dataset_id = _dataset_id(node_id)
    url = f"{BASE}/{dataset_id}.csv"
    client = get_client()
    with client.stream(
        "GET",
        url,
        params={"$limit": FULL_LIMIT},
        timeout=(10.0, 900.0),
    ) as response:
        response.raise_for_status()
        with raw_writer(
            node_id,
            extension="csv.gz",
            mode="wb",
            compression="gzip",
        ) as out:
            for chunk in response.iter_bytes(CHUNK_SIZE):
                out.write(chunk)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fcc-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
