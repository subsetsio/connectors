"""StatsWales connector — Welsh Government official statistics.

Mechanism: the StatsWales public API (https://api.stats.gov.wales/v1, no auth).
Each published dataset has a stable UUID and is served in full as a single
long-format CSV at GET /v1/{dataset_id}/download/csv. Every CSV shares the
shape: ``Data values, Data description, <one column per dimension>, Notes``.

Strategy: stateless full re-pull. One download node per dataset fetches the
whole CSV and stores it verbatim; one SQL transform per dataset publishes it as
a Delta table. The corpus is ~747 small CSVs with no incremental filter, so a
full refresh each run is cheap and picks up revisions for free.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_file,
    transient_retry,
)

from constants import ENTITY_IDS

API_BASE = "https://api.stats.gov.wales/v1"


def _entity_id(node_id: str) -> str:
    """Recover the dataset UUID from the spec id (strip the connector prefix)."""
    return node_id[len("statswales-"):]


@transient_retry()
def _download_csv(dataset_id: str) -> bytes:
    url = f"{API_BASE}/{dataset_id}/download/csv"
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()  # 5xx/429 retried by decorator; 4xx propagates as a bug/permanent
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


# One Delta table per dataset. The raw CSV is already a clean long-format table
# (DuckDB auto-detects column types); publish it as-is. Each dataset has its own
# dimension columns, so this thin pass-through is the right shape — heavier
# normalization would require per-dataset schema knowledge we don't have here.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
