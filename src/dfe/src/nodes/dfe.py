"""DfE — Explore Education Statistics (EES) public data API connector.

Catalog connector: one download spec per EES data set (the rank-active entity
union). Each data set is fetched in full from the bulk CSV endpoint
(GET /data-sets/{dataSetId}/csv) — a stable, deterministic URL returning the
entire table as gzip CSV.

Fetch strategy: stateless full re-pull. The EES API exposes no incremental
filter for bulk extraction, and overwriting the whole table each refresh picks
up DfE's revisions for free, so every run downloads each data set whole.

Raw format & memory: the CSV is streamed (never fully buffered) straight into a
row-group-streamed Parquet file with EVERY column typed as VARCHAR. Two reasons
for all-string Parquet over the obvious alternatives:
  * DfE statistical CSVs carry suppression markers (c, z, x, k, low, ~) inside
    otherwise-numeric columns. The runtime registers raw assets via bare
    read_csv_auto / read_json_auto with no type-override hook, so any numeric
    inference would hard-fail mid-file. String columns sidestep this entirely.
  * Some EES data sets are very wide (200+ columns). read_json_auto collapses
    such wide objects into a single "json" column, so NDJSON is unusable here;
    Parquet handles arbitrary width cleanly.
Streaming + 50k-row Parquet batches keep peak memory flat regardless of data
set size (the largest is ~12.5M rows / ~2GB of CSV), which matters because the
DAG runs many download nodes concurrently. The published table preserves the
source faithfully (counts and markers side by side) for downstream casting.
"""

from __future__ import annotations

import csv

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

API = "https://api.education.gov.uk/statistics/v1"
BATCH_ROWS = 50_000  # rows per Parquet row group; bounds peak memory per node

# The rank-active entity union (EES data set ids). Inlined — module-level I/O
# is not allowed, and these are the authoritative coverage target.
from constants import ENTITY_IDS


@transient_retry()
def _download_to_parquet(asset: str, data_set_id: str) -> None:
    """Stream one data set's CSV into an all-VARCHAR Parquet asset.

    A transient failure restarts the whole download (the Parquet writer
    overwrites from the top), so a partial file is never published — an
    exhausted retry raises and the node (and its transform) is marked failed.
    """
    client = get_client()
    url = f"{API}/data-sets/{data_set_id}/csv"
    with client.stream("GET", url, timeout=httpx.Timeout(300.0, connect=10.0)) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines())  # httpx decodes the gzip stream
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"{asset}: CSV response was empty (no header row)")
        ncol = len(header)
        schema = pa.schema([(name, pa.string()) for name in header])

        total = 0
        with raw_parquet_writer(asset, schema) as writer:
            cols = [[] for _ in range(ncol)]
            batch = 0
            for row in reader:
                if len(row) < ncol:
                    row = row + [None] * (ncol - len(row))
                for i in range(ncol):
                    cols[i].append(row[i])
                batch += 1
                total += 1
                if batch >= BATCH_ROWS:
                    writer.write_table(
                        pa.table({header[i]: cols[i] for i in range(ncol)}, schema=schema)
                    )
                    cols = [[] for _ in range(ncol)]
                    batch = 0
            if batch:
                writer.write_table(
                    pa.table({header[i]: cols[i] for i in range(ncol)}, schema=schema)
                )
        if total == 0:
            raise ValueError(f"{asset}: data set CSV had a header but zero data rows")


def fetch_one(node_id: str) -> None:
    """Download one EES data set. node_id is the spec id; the data set id is the
    suffix after the "dfe-" prefix."""
    _download_to_parquet(node_id, node_id[len("dfe-"):])


DOWNLOAD_SPECS = [
    NodeSpec(id=f"dfe-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per data set. The transform is a thin pass-through:
# the raw Parquet is already the faithful, string-typed table, so SELECT *
# publishes every column.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
