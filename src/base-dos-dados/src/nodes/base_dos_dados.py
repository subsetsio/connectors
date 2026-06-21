"""Base dos Dados connector — public one-click-download GCS path.

Mechanism (from research, id 'gcs_one_click'): the anonymous public bucket
`basedosdados-public` holds one gzipped CSV per curated table under
`one-click-download/<gcp_dataset_id>/<gcp_table_id>/<file>.csv.gz`. Each object
is one full table in a single request — the optimal whole-table snapshot shape.

Shape: stateless full re-pull (decision shape 1). Every table is a single small
csv.gz (<=~27MB compressed); we re-fetch the whole object each run and overwrite.
There is no incremental filter on the GCS path and no per-run budget concern, so
no state/watermark logic. Freshness (whether a node runs at all) is the maintain
step's concern, not ours.

Raw format: we **normalize the gz CSV to parquet at download time** rather than
saving the gz verbatim. The runtime's SqlNodeSpec executor registers each raw
dep as `read_csv_auto([...])` with *default* options (a 20 480-row type sniff,
2 MB max line, strict mode) that the transform SQL cannot override. On this
heterogeneous catalog (238 tables, 238 distinct column lists) those defaults
fail on a minority of tables in three ways:
  - a column whose values flip type past the sniff sample (e.g. a code column
    that is all digits for 66 k rows then hits "J") — fixed by `sample_size=-1`
    (whole-file type inference);
  - quoted free-text fields with embedded newlines that blow past the 2 MB line
    cap — fixed by a 16 MB `max_line_size`;
  - ragged rows with fewer columns than the header — fixed by `null_padding`
    + `strict_mode=false` (pad the short row, don't reject it). `null_padding`
    is incompatible with the *parallel* scanner when a table also has quoted
    newlines (free-text fields spanning lines), so we force `parallel=false`;
    at ≤27 MB/table the single-threaded read is a non-issue;
  - and a column DuckDB sniffs as `TIME`, which Delta Lake cannot store at all
    — fixed by casting every `TIME`/`TIME WITH TIME ZONE` column to VARCHAR.
Doing the parse once here (with robust options) and persisting parquet means the
transform reads a typed file with no re-sniffing, so each subset stays a thin
`SELECT *` passthrough that still acts as the 0-row correctness gate.
"""

from __future__ import annotations

import os
import tempfile

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_file,
    transient_retry,
)

from constants import GCS_OBJECTS

BUCKET_BASE = "https://storage.googleapis.com/basedosdados-public/"

# Robust read_csv_auto options applied to every table. `sample_size=-1` infers
# types from the whole file (no late-row type flips); the 16 MB line cap clears
# the largest observed quoted free-text blob (~3.3 MB); null_padding +
# strict_mode=false keep ragged rows instead of failing the table.
_CSV_READ_OPTS = (
    "sample_size=-1, "
    "max_line_size=16777216, "
    "null_padding=true, "
    "strict_mode=false, "
    "parallel=false, "
    "ignore_errors=false"
)


@transient_retry()  # 6 attempts, exp backoff over transient net errors + 429/5xx
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _is_time_type(duckdb_type: str) -> bool:
    """True for TIME / TIME WITH TIME ZONE (which Delta Lake rejects), but not
    TIMESTAMP / TIMESTAMP WITH TIME ZONE (which Delta stores fine)."""
    t = duckdb_type.upper()
    return t.startswith("TIME") and not t.startswith("TIMESTAMP")


def fetch_one(node_id: str) -> None:
    """Download one table's public one-click csv.gz, parse it with robust
    options, and persist it as typed parquet under the asset id.

    The runtime passes the spec id, which is both the lookup key and the asset
    name. We materialize the CSV into a DuckDB temp table once (full-file type
    inference), cast any Delta-incompatible TIME columns to VARCHAR, then stream
    the result to a parquet file saved as `<asset>.parquet` — the format the
    transform's `read_parquet` view reads with no further sniffing.
    """
    import duckdb

    asset = node_id
    obj = GCS_OBJECTS[node_id]  # KeyError here = a spec/constants drift bug
    content = _download(BUCKET_BASE + obj)

    tmp_csv = tmp_parquet = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".csv.gz", delete=False
        ) as fh:
            fh.write(content)
            tmp_csv = fh.name
        tmp_parquet = tmp_csv + ".parquet"

        con = duckdb.connect()
        try:
            csv_path = tmp_csv.replace("'", "''")
            con.execute(
                f"CREATE TEMP TABLE _t AS "
                f"SELECT * FROM read_csv_auto('{csv_path}', {_CSV_READ_OPTS})"
            )
            cols = con.execute(
                "SELECT column_name, column_type FROM "
                "(DESCRIBE _t)"
            ).fetchall()
            projection = ", ".join(
                f'"{name}"::VARCHAR AS "{name}"' if _is_time_type(ctype) else f'"{name}"'
                for name, ctype in cols
            )
            out_path = tmp_parquet.replace("'", "''")
            con.execute(
                f"COPY (SELECT {projection} FROM _t) "
                f"TO '{out_path}' (FORMAT parquet, COMPRESSION zstd)"
            )
        finally:
            con.close()

        with open(tmp_parquet, "rb") as fh:
            save_raw_file(fh.read(), asset, extension="parquet")
    finally:
        for path in (tmp_csv, tmp_parquet):
            if path and os.path.exists(path):
                os.unlink(path)


DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in GCS_OBJECTS
]

# One published Delta table per table. Schemas are heterogeneous and curated
# upstream, so each transform is a straight typed passthrough; the transform
# still acts as the correctness gate (0 rows / unreadable csv fails the node).
TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
