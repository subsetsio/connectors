"""CDC (data.cdc.gov) connector — Socrata open-data portal.

Catalog connector: each rank-active entity is one Socrata dataset, identified by
its stable 4x4 id (e.g. "24w5-nppr"). Raw extraction uses the per-dataset bulk
CSV export (`/api/views/{id}/rows.csv?accessType=DOWNLOAD`) — one stable URL per
dataset returning the entire table in one request (chosen mechanism: bulk_csv).

Fetch shape: stateless full re-pull. There is no portal-wide changed-since feed,
so each dataset is re-fetched in full every run and the raw CSV is overwritten.
Datasets are streamed to disk gzip-compressed (CSV exports range from KBs to tens
of MBs) so a large export never has to materialize in memory. Freshness — whether
a given dataset is re-fetched on a run — is the maintain step's job, not ours.

Transform: each subset is a thin pass-through of its dataset's CSV. DuckDB's
`read_csv_auto` (invoked by the runtime over the gzipped raw) infers column names
and types directly from the Socrata export, so the published table mirrors the
source schema 1:1.
"""

from __future__ import annotations


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

# Per-dataset bulk CSV export. The 4x4 id is the only variable; the URL is stable
# and persistent (research: url_stability="persistent").
_EXPORT_URL = "https://data.cdc.gov/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"

# Stream chunk size for the CSV download.
_CHUNK = 1 << 20  # 1 MiB

# The rank-accepted entity union — the 654 Socrata dataset ids to publish.
# Inlined (no module-level I/O); the authoritative source is
# data/sources/cdc/work/entity_union.json.
from constants import ENTITY_IDS


@transient_retry()
def _download_csv_gz(url: str, asset: str) -> None:
    """Stream one dataset's full CSV export to a gzip-compressed raw asset.

    Streaming + gzip keeps memory flat regardless of export size, and writing the
    raw inside the retried fn means a mid-stream transient failure simply re-opens
    the writer (truncating any partial bytes) on the next attempt.
    """
    client = get_client()
    # (connect, read) timeouts — a generous read window for multi-MB exports.
    with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        with raw_writer(asset, "csv.gz", mode="wb", compression="gzip") as out:
            for chunk in resp.iter_bytes(_CHUNK):
                out.write(chunk)


def fetch_one(node_id: str) -> None:
    """Fetch one Socrata dataset's full table. The runtime passes the spec id,
    which is also the raw asset name; the dataset's 4x4 id is the id minus the
    "cdc-" prefix."""
    asset = node_id
    dataset_id = node_id[len("cdc-"):]
    _download_csv_gz(_EXPORT_URL.format(dataset_id=dataset_id), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cdc-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per subset: a thin pass-through of the dataset CSV.
# The runtime registers each dep's gzipped raw as a `read_csv_auto` view, so
# SELECT * publishes the source schema as DuckDB infers it.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
