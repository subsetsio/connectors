"""NYC Open Data — Socrata catalog connector.

One download node per rank-accepted dataset (fxf id), fetched in full each run
via the Socrata bulk CSV export (`/api/views/{id}/rows.csv`, a single streamed
request that returns the entire table). The CSV is streamed to a temp file,
normalized through DuckDB (`normalize_names=true` so column names are
Delta-legal; typed sniffing with an `all_varchar=true` fallback so a column
whose type can't be inferred never errors the read), written to a temp parquet,
and streamed into the raw layer — all memory-bounded so large datasets
(311, collisions, inspections) don't OOM the spawn subprocess.

Stateless full re-pull: every run overwrites. The export endpoint exposes no
incremental delta we use; the maintain step gates whether a node runs at all.
Each subset's transform is a thin `SELECT *` passthrough over its raw parquet.
"""

import os
import shutil
import tempfile

import duckdb
import httpx
import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer, transient_retry
from subsets_utils.http_client import get_client
from constants import ENTITY_IDS

_PREFIX = "nyc-open-data-"
_BASE = "https://data.cityofnewyork.us"
_TIMEOUT = httpx.Timeout(connect=15.0, read=600.0, write=120.0, pool=15.0)
_DL_BATCH = 100_000


def _fxf(node_id: str) -> str:
    """Recover the Socrata 4x4 id from the spec id."""
    return node_id[len(_PREFIX):]


@transient_retry()
def _download_csv(url: str, headers: dict, dest_path: str) -> None:
    """Stream the full bulk-CSV export to dest_path. Retried on transient
    network/5xx/429 errors; a retry truncates and restarts the file."""
    client = get_client()
    with open(dest_path, "wb") as fh:
        with client.stream("GET", url, headers=headers, timeout=_TIMEOUT) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                fh.write(chunk)


def _csv_to_parquet(csv_path: str, pq_path: str) -> None:
    """Normalize the CSV to parquet via DuckDB. Try typed sniffing first
    (better column types); on any inference/cast error fall back to
    all_varchar so the read is total."""
    con = duckdb.connect()
    try:
        typed = (
            f"SELECT * FROM read_csv_auto('{csv_path}', "
            f"normalize_names=true, header=true, sample_size=200000)"
        )
        allvarchar = (
            f"SELECT * FROM read_csv_auto('{csv_path}', "
            f"normalize_names=true, header=true, all_varchar=true)"
        )
        copy_opts = "(FORMAT parquet, COMPRESSION zstd)"
        try:
            con.execute(f"COPY ({typed}) TO '{pq_path}' {copy_opts}")
        except duckdb.Error:
            if os.path.exists(pq_path):
                os.remove(pq_path)
            con.execute(f"COPY ({allvarchar}) TO '{pq_path}' {copy_opts}")
    finally:
        con.close()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    fxf = _fxf(node_id)
    url = f"{_BASE}/api/views/{fxf}/rows.csv"
    headers = {}
    token = os.environ.get("SOCRATA_APP_TOKEN")
    if token:
        headers["X-App-Token"] = token

    tmpdir = tempfile.mkdtemp(prefix="nycod-")
    csv_path = os.path.join(tmpdir, "data.csv")
    pq_path = os.path.join(tmpdir, "data.parquet")
    try:
        _download_csv(url, headers, csv_path)
        _csv_to_parquet(csv_path, pq_path)
        os.remove(csv_path)  # free disk before re-streaming the parquet

        pf = pq.ParquetFile(pq_path)
        schema = pf.schema_arrow
        with raw_parquet_writer(asset, schema) as writer:
            wrote_any = False
            for batch in pf.iter_batches(batch_size=_DL_BATCH):
                writer.write_batch(batch)
                wrote_any = True
            if not wrote_any:
                # 0-row dataset: emit an empty table so the schema is recorded
                # (the SQL transform will then fail loudly on the empty publish).
                writer.write_table(schema.empty_table())
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{_PREFIX}{eid.lower().replace('_', '-')}",
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
