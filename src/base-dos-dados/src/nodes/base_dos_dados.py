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

Raw format: we **parse the gz CSV to typed parquet at download time** rather than
saving the gz verbatim. The runtime's SqlNodeSpec executor would otherwise read
each raw dep with DuckDB `read_csv_auto` (options the transform SQL cannot
override), and that reader is unreliable on this heterogeneous catalog (238
tables, 238 distinct column lists): on several tables its dialect sniffer
mis-detects quoting around free-text fields with embedded newlines and doubled
quotes (`""`), silently splitting one row across many phantom `columnNNN`
columns; on others its 20 480-row type sniff or 2 MB line cap fails outright.

We parse instead with pandas' C engine, a battle-tested RFC-4180 reader: it
handles embedded newlines, doubled-quote escapes, and ragged rows correctly, and
infers each column's type over the *whole* column (no sample-window flips, and no
bare `TIME` type — which Delta Lake can't store anyway — since unparsed
date/time strings stay strings). The parsed frame is written as parquet, so the
transform reads a correctly-aligned, typed file and each subset stays a thin
`SELECT *` passthrough that still acts as the 0-row correctness gate. We do NOT
skip bad lines: a row pandas cannot tokenize fails the node loudly rather than
publishing silently-misaligned data.
"""

from __future__ import annotations

import os
import tempfile

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

from constants import GCS_OBJECTS

BUCKET_BASE = "https://storage.googleapis.com/basedosdados-public/"


@transient_retry()  # 6 attempts, exp backoff over transient net errors + 429/5xx
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    """Download one table's public one-click csv.gz, parse it with pandas, and
    persist it as typed parquet under the asset id.

    The runtime passes the spec id, which is both the lookup key and the asset
    name. pandas' C engine parses the RFC-4180 CSV (correct column alignment
    through quoted newlines / doubled quotes), and the frame is converted to a
    PyArrow table and saved as `<asset>.parquet` — the format the transform's
    `read_parquet` view reads with no further sniffing.
    """
    import pandas as pd
    import pyarrow as pa

    asset = node_id
    obj = GCS_OBJECTS[node_id]  # KeyError here = a spec/constants drift bug
    content = _download(BUCKET_BASE + obj)

    tmp_csv = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".csv.gz", delete=False) as fh:
            fh.write(content)
            tmp_csv = fh.name

        # low_memory=False so each column's dtype is inferred from the whole
        # column in one pass (mixed-type chunk artifacts otherwise force object).
        df = pd.read_csv(tmp_csv, compression="gzip", engine="c", low_memory=False)
        try:
            table = pa.Table.from_pandas(df, preserve_index=False)
        except (pa.ArrowInvalid, pa.ArrowTypeError):
            # A genuinely mixed-type object column (e.g. ints and strings in one
            # source column) can defeat Arrow's inference — fall back to a
            # faithful all-string parse, which always converts cleanly.
            df = pd.read_csv(
                tmp_csv, compression="gzip", engine="c", dtype=str, low_memory=False
            )
            table = pa.Table.from_pandas(df, preserve_index=False)
        save_raw_parquet(table, asset)
    finally:
        if tmp_csv and os.path.exists(tmp_csv):
            os.unlink(tmp_csv)


DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in GCS_OBJECTS
]

# One published Delta table per table. Schemas are heterogeneous and curated
# upstream, so each transform is a straight typed passthrough; the transform
# still acts as the correctness gate (0 rows / unreadable parquet fails the node).
TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
