"""EPA Envirofacts connector.

Fetches the full contents of EPA Envirofacts relational tables/views via the
Envirofacts Data Service API V1 (https://data.epa.gov/dmapservice/). Each
accepted collect entity is one `[program].[table]` target pulled in full.

Access shape: stateless full re-pull (download prompt shape 1). Envirofacts
exposes NO incremental query surface (no since/modifiedAfter/cursor parameter
on the dmapservice tables), so every refresh re-pulls each table in full and
overwrites. Several tables are large (icis.icis_dmr_value, icis.icis_npdes_-
violation, rcra.rcr_em_waste_line and others exceed 10M rows), so each table is
paginated by the [first]:[last] row-window segment and streamed batch-by-batch
into a single gzip-compressed NDJSON raw asset — memory stays bounded to one
page regardless of table size. NDJSON (not parquet) because the 202 tables span
13 program systems with wildly different, drifty schemas; a per-table parquet
schema contract would be brittle. The transform re-types on read.

Pagination: the API row-window is 1-indexed and inclusive — `t/1:100000` returns
rows 1..100000. A page shorter than the requested size (or empty) marks the end
of the table.
"""

from __future__ import annotations

import json


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

BASE = "https://data.epa.gov/dmapservice/"

# Rows per API request. 100k rows of a wide table is ~55MB JSON and returns in
# ~20s, comfortably inside the 15-minute per-request completion window while
# keeping the request count (and per-page memory) reasonable.
PAGE_SIZE = 100_000

# Safety ceiling: detect a table that paginates far past any plausible EPA
# table size (would be >2 billion rows at PAGE_SIZE) and RAISE rather than loop
# forever. Real tables top out in the tens of millions.
MAX_PAGES = 20_000


@transient_retry()
def _fetch_page(table: str, first: int, last: int) -> list[dict]:
    """Fetch one inclusive row-window [first:last] of an Envirofacts table as
    a list of records. Raises on transient errors (retried) and 4xx (bug/perm).
    """
    url = f"{BASE}{table}/{first}:{last}/JSON"
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.json()


def _table_for(node_id: str) -> str:
    """Recover the Envirofacts `program.table` path from a spec/asset id.

    The id is `epa-{entity.lower().replace('_', '-')}`; the program separator is
    a dot (preserved) and underscores became dashes. EPA table names contain no
    real dashes, so dash->underscore round-trips exactly.
    """
    return node_id[len("epa-"):].replace("-", "_")


def fetch_one(node_id: str) -> None:
    """Pull one Envirofacts table in full, streaming pages into a single
    gzip-NDJSON raw asset. The runtime passes the spec id, which is also the
    asset name. Freshness gating is the maintain step's job — if invoked, fetch.
    """
    asset = node_id
    table = _table_for(node_id)
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for page in range(MAX_PAGES):
            first = page * PAGE_SIZE + 1
            last = (page + 1) * PAGE_SIZE
            rows = _fetch_page(table, first, last)
            for row in rows:
                fh.write(json.dumps(row, separators=(",", ":")))
                fh.write("\n")
            total += len(rows)
            if len(rows) < PAGE_SIZE:
                break
        else:
            raise RuntimeError(
                f"{table}: hit MAX_PAGES={MAX_PAGES} ({total:,} rows) without "
                "draining the table — investigate before raising the cap"
            )
    print(f"  -> {table}: {total:,} rows")


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"epa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per accepted subset. The raw NDJSON is already a
# clean per-table dump, so the transform is a thin straight-through projection;
# DuckDB's read_json_auto re-types each table's columns on read. The 0-row
# guard in the runtime makes this the correctness gate on each raw pull.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
