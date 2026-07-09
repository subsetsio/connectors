"""Connecticut Department of Labor (Office of Research) connector.

Source: the statewide Socrata open-data portal data.ct.gov. Each CTDOL dataset
is reachable at https://data.ct.gov/resource/<4x4-id>.json. No auth required.

Shape: stateless full re-pull (shape 1). Every dataset is small (a few hundred
to ~52k rows), so each refresh re-fetches the whole table and overwrites. No
incremental watermark — Socrata revises rows in place and the full pull is cheap.

Raw is saved as NDJSON: the SODA JSON API returns every value as a string
(numbers carry thousands-separators and percent signs in some tables, and the
LAUS table's columns are period-named and drift release-to-release), so typing
is deferred to the transform SQL where it can clean and cast loudly.
"""
from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import ENTITY_IDS

SLUG = "connecticut-department-of-labor"
BASE = "https://data.ct.gov/resource"
PAGE = 50000          # Socrata's max page size
MAX_PAGES = 100       # safety ceiling: ~5M rows; trips if a dataset grows wildly


@transient_retry()
def _fetch_page(url: str, offset: int) -> list:
    resp = get(
        url,
        params={"$limit": PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Fetch one CTDOL dataset in full and save it as NDJSON.

    The runtime passes the spec id; the Socrata dataset id is the id with the
    connector slug prefix stripped. Pagination via SoQL $offset, ordered by the
    system :id for stable paging, until a short page signals the end.
    """
    asset = node_id
    dataset_id = node_id[len(SLUG) + 1:]
    url = f"{BASE}/{dataset_id}.json"

    rows: list = []
    offset = 0
    pages = 0
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} at offset {offset}; "
                "the dataset grew far past expectations -- investigate before raising the cap"
            )
        batch = _fetch_page(url, offset)
        if not batch:
            break
        rows.extend(batch)
        pages += 1
        if len(batch) < PAGE:
            break
        offset += PAGE

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
