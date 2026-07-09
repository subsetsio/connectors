"""U.S. Department of Transportation — data.transportation.gov (Socrata).

Catalog connector: one generic fetch per rank-accepted dataset. Each dataset is
pulled in full every run (stateless full re-pull) via the SODA JSON API, paged
at the 50000-row hard cap and streamed to a gzip ndjson raw asset so the very
large tables (some > 1M rows) never have to fit in memory at once. data.gov
ids that belong to BTS 302-redirect to data.bts.gov; subsets_utils.get follows
redirects. No app token is required for anonymous access.

Each subset's transform is a thin SELECT * pass — every dataset has its own
heterogeneous schema, so the connector publishes the source columns as-is
(DuckDB infers types from the ndjson on read).
"""

import json

from subsets_utils import NodeSpec, get, raw_writer
from constants import ENTITY_IDS

PREFIX = "u-s-department-of-transportation-"
BASE = "https://data.transportation.gov/resource"
PAGE = 50000  # SODA per-request hard cap


def _fetch_page(ds_id: str, offset: int) -> list:
    # $order=:id pins a stable sort so offset paging never skips/dups rows.
    resp = get(
        f"{BASE}/{ds_id}.json",
        params={"$limit": PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id
    ds_id = node_id[len(PREFIX):]
    offset = 0
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            rows = _fetch_page(ds_id, offset)
            if not rows:
                break
            for row in rows:
                fh.write(json.dumps(row) + "\n")
            total += len(rows)
            if len(rows) < PAGE:
                break
            offset += PAGE
    print(f"  {asset}: wrote {total} rows from dataset {ds_id}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
