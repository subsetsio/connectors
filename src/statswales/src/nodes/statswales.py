"""StatsWales connector — Welsh Government official statistics.

Mechanism: the StatsWales public API (https://api.stats.gov.wales/v1, no auth).
Each published dataset has a stable UUID and is served in full as a single
long-format CSV at GET /v1/{dataset_id}/download/csv. Every CSV shares the
shape: ``Data values, Data description, <one column per dimension>, Notes``.

Strategy: stateless full re-pull. One download node per dataset fetches the
whole CSV and stores it verbatim. The corpus is ~755 small CSVs with no
incremental filter, so a full refresh each run is cheap and picks up revisions
for free.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_file,
)

from constants import ENTITY_IDS

API_BASE = "https://api.stats.gov.wales/v1"


def _entity_id(node_id: str) -> str:
    """Recover the dataset UUID from the spec id (strip the connector prefix)."""
    return node_id[len("statswales-"):]


def _download_csv(dataset_id: str) -> bytes:
    url = f"{API_BASE}/{dataset_id}/download/csv"
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _entity_id(node_id)
    content = _download_csv(dataset_id)
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"statswales-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
