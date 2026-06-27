"""New York State Department of Labor — data.ny.gov Socrata connector.

Catalog connector: each entity is a Socrata 4x4 dataset on data.ny.gov,
fetched in full from its per-dataset SODA endpoint
(https://data.ny.gov/resource/{id}.json) and published 1:1 as a Delta table.

Fetch shape: stateless full re-pull. Each dataset is re-fetched in its
entirety every run and overwritten — Socrata serves the whole table behind one
stable id, the largest in scope (QCEW annual, ~1.2M rows) pages through in ~24
requests, so there is no need for watermarks or incremental queries.

Raw format: NDJSON, streamed page-by-page. Socrata `.json` returns every
scalar as a string and exposes a few columns as nested JSON objects (Socrata
location/point/url types). NDJSON tolerates that heterogeneity; nested
dict/list values are serialized to JSON strings so every column is a flat
scalar and the thin `SELECT *` transform publishes cleanly across all 23
schemas.
"""

import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS

SLUG = "new-york-state-department-of-labor"
BASE = "https://data.ny.gov/resource/{ds}.json"
PAGE_SIZE = 50000          # Socrata SODA hard max per request
MAX_PAGES = 2000           # safety ceiling (~100M rows); raises if exceeded


def _dataset_id(node_id: str) -> str:
    """Recover the Socrata 4x4 id from the spec id."""
    return node_id[len(SLUG) + 1:]


@transient_retry()
def _fetch_page(ds: str, offset: int) -> list:
    resp = get(
        BASE.format(ds=ds),
        params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _flatten(row: dict) -> dict:
    """Coerce nested Socrata objects (point/location/url) to JSON strings so the
    NDJSON row is entirely flat scalars."""
    out = {}
    for k, v in row.items():
        out[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id                     # the spec id IS the asset name
    ds = _dataset_id(node_id)

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        offset = 0
        for page in range(MAX_PAGES):
            rows = _fetch_page(ds, offset)
            if not rows:
                break
            for row in rows:
                f.write(json.dumps(_flatten(row), ensure_ascii=False) + "\n")
            if len(rows) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
        else:
            raise RuntimeError(
                f"{asset}: hit MAX_PAGES={MAX_PAGES} for dataset {ds} without "
                "draining — source grew past expectations, investigate."
            )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per subset. Each Socrata dataset has its own
# heterogeneous schema, so the transform is a thin pass that republishes the
# full (flat, all-string) raw table verbatim.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
