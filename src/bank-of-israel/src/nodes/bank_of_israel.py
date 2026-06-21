"""Bank of Israel — SDMX statistical database (EDGE / FusionEdgeServer).

One download spec per SDMX dataflow under agency BOI.STATISTICS (the rank-active
entity union). Each dataflow is pulled in full as SDMX-CSV via the bulk
per-dataflow endpoint (empty series key returns every series at once), then
published as one long-format Delta table.

Fetch shape: stateless full re-pull. The whole corpus is a few hundred MB and
re-fetches in minutes, so every run overwrites the full history — late
revisions are picked up for free, no watermark/cursor. The SDMX API does expose
startperiod/endperiod incremental filters, but they are unnecessary for our
whole-corpus snapshot pattern.

Raw is written as Parquet with an all-string schema derived per dataflow from
its CSV header: the 41 dataflows each have their own DSD (11-34 columns,
drifting dimension sets), so the schema is built per asset rather than shared.
Every value is kept as a string and the transform re-types OBS_VALUE downstream.
An explicit declared schema is used (not JSON/CSV auto-inference): the largest
flows (CARDS ~1.8M rows, FTR ~1.4M, PRI ~1.0M) exceed any reader's type-sniffing
sample window, so inference picks the wrong type on a late row — declaring every
column VARCHAR up front sidesteps that entirely. Writes stream in row batches to
keep memory bounded. Columns universal to every flow: SERIES_CODE, FREQ,
TIME_PERIOD, OBS_VALUE.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

_BATCH_ROWS = 50_000

# Entity union — copied verbatim from
# data/sources/bank-of-israel/work/entity_union.json
from constants import ENTITY_IDS

_SLUG = "bank-of-israel"
_DATA_BASE = (
    "https://edge.boi.org.il/FusionEdgeServer/sdmx/v2/"
    "data/dataflow/BOI.STATISTICS"
)
_VERSION = "1.0"  # every BOI.STATISTICS dataflow is version 1.0


def _asset_id(entity_id: str) -> str:
    return f"{_SLUG}-{entity_id.lower().replace('_', '-')}"


def _flow_for_node(node_id: str) -> str:
    """Recover the source dataflow id from the spec/asset id.

    The asset id lower-cases and dash-substitutes the dataflow id, which is not
    reversible on its own, so resolve it by matching against the entity union.
    """
    for eid in ENTITY_IDS:
        if _asset_id(eid) == node_id:
            return eid
    raise KeyError(f"no dataflow maps to node id {node_id!r}")


@transient_retry()
def _fetch_csv(url: str) -> str:
    # (connect, read) — generous read timeout: the bulk dataflows can be
    # hundreds of MB and take a while to stream.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


def _to_batch(rows: list[list[str]], schema: pa.Schema) -> pa.RecordBatch:
    # rows is a list of equal-length string lists; transpose to columns.
    columns = list(zip(*rows)) if rows else [() for _ in schema]
    arrays = [pa.array(list(col), type=pa.string()) for col in columns]
    return pa.RecordBatch.from_arrays(arrays, schema=schema)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = _flow_for_node(node_id)
    url = f"{_DATA_BASE}/{flow}/{_VERSION}?format=csv"

    text = _fetch_csv(url)
    reader = csv.reader(io.StringIO(text))
    header = next(reader, None)
    assert header, f"{asset}: empty CSV (no header) from {url}"
    ncol = len(header)
    schema = pa.schema([(col, pa.string()) for col in header])

    n = 0
    with raw_parquet_writer(asset, schema) as w:
        buf: list[list[str]] = []
        for row in reader:
            # Normalize ragged rows to the header width: SDMX-CSV can omit
            # trailing empty fields. Keep values as raw strings; the transform
            # re-types OBS_VALUE.
            if len(row) < ncol:
                row = row + [""] * (ncol - len(row))
            elif len(row) > ncol:
                row = row[:ncol]
            buf.append(row)
            if len(buf) >= _BATCH_ROWS:
                w.write_batch(_to_batch(buf, schema))
                n += len(buf)
                buf = []
        if buf:
            w.write_batch(_to_batch(buf, schema))
            n += len(buf)

    # A bulk dataflow pull returning no observations means the endpoint or
    # format changed underneath us — fail loudly rather than publish nothing.
    assert n > 0, f"{asset}: 0 data rows from {url}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_asset_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# One published Delta table per dataflow. Uniform thin parse-and-type pass:
# keep all of the dataflow's dimension/attribute columns (as strings),
# cast OBS_VALUE to a number, and drop rows with no usable observation.
# TIME_PERIOD stays a string because frequencies differ across flows
# (daily 2005-09-01, monthly 2005-09, quarterly 2005-Q1, annual 2005).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
            FROM "{s.id}"
            WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
