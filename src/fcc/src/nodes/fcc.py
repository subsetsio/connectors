"""FCC connector — opendata.fcc.gov (Socrata / Tyler Technologies portal).

Each accepted entity is one Socrata four-by-four dataset, published 1:1 as a
Delta table. We fetch the full table per dataset from the SODA CSV export
(`/resource/<id>.csv?$limit=<all>`), which returns every row in a single
streamed response with stable snake_case (field-name) headers. Raw is streamed
straight to a gzip-compressed CSV so even the multi-million-row datasets
(consumer complaints ~3.5M rows) never materialize in memory.

Strategy: stateless full re-pull (shape 1). The whole accepted corpus is small
enough (~3.7M rows total across 18 datasets) to re-fetch every run; revisions
and late corrections are picked up for free. No watermark/cursor.

Transform is a thin passthrough: `SELECT * FROM "<dep>"` reads the raw CSV back
through DuckDB (read_csv_auto, gzip inferred from the .gz suffix) and publishes
it. Type inference is left to DuckDB so each heterogeneous dataset keeps its own
column list.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

# The 18 rank-accepted Socrata dataset ids (the entity union).
from constants import ENTITY_IDS

BASE = "https://opendata.fcc.gov/resource"
# SODA honours an arbitrarily large $limit on the CSV export and streams the
# whole table in one response; this is comfortably above the largest accepted
# dataset (~3.5M rows).
FULL_LIMIT = 200_000_000
CHUNK = 1 << 20  # 1 MiB stream chunks


def _dataset_id(node_id: str) -> str:
    """Recover the Socrata four-by-four id from the spec id (strip 'fcc-')."""
    return node_id[len("fcc-"):]


@transient_retry()
def _stream_csv_to_raw(asset: str, dataset_id: str) -> None:
    """Stream the full dataset CSV to a gzip-compressed raw asset.

    The whole transfer happens inside the retried fn: a transient drop
    mid-stream re-fetches the entire table (the destination is overwritten),
    so a partial gzip is never left behind for the transform to read.
    """
    url = f"{BASE}/{dataset_id}.csv"
    client = get_client()
    with client.stream(
        "GET", url, params={"$limit": FULL_LIMIT}, timeout=(10.0, 600.0)
    ) as resp:
        resp.raise_for_status()
        with raw_writer(asset, extension="csv.gz", mode="wb",
                        compression="gzip") as out:
            for chunk in resp.iter_bytes(CHUNK):
                out.write(chunk)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _stream_csv_to_raw(asset, _dataset_id(node_id))


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fcc-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
