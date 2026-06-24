"""European Central Bank — SDMX 2.1 RESTful web service (ECB Data Portal).

One published Delta table per ECB dataflow (the rank-accepted entity union in
``constants.ENTITY_IDS``). Each dataflow is fetched in full as SDMX-CSV from
``/service/data/{FLOW}`` (key omitted = every series in the flow) and stored as
gzip NDJSON, one record per observation.

Fetch shape: **stateless full re-pull**. The whole flow is re-fetched every
refresh and overwritten; revisions and late corrections are picked up for free.
The response is streamed and parsed line-by-line into batched Parquet so memory
stays bounded regardless of flow size (the largest flows — SHS, MMSR, SEC — can
be many millions of observations).

Each dataflow carries its own DSD dimension columns (EXR has CURRENCY/EXR_TYPE,
YC has FM_MATURITY/DATA_TYPE_FM, ...), so there is no single schema across the
75 assets — each asset gets a per-flow schema derived from its CSV header. Every
column is written as a string: SDMX-CSV values are text, and an all-VARCHAR raw
keeps the transform's re-typing explicit (`TRY_CAST` in SQL) and immune to the
JSON type-inference pitfalls a `read_json_auto` view hits when a column is empty
across the inference sample window and populated only later in the file.
"""

import csv

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "european-central-bank"
PREFIX = f"{SLUG}-"
DATA_BASE = "https://data-api.ecb.europa.eu/service/data"
BATCH_ROWS = 50_000  # rows per parquet row-group flush


def _flow_from_node_id(node_id: str) -> str:
    """Recover the upstream dataflow id from a download spec id.

    Inverse of ``f"{SLUG}-{eid.lower().replace('_', '-')}"``. ECB flow ids are
    uppercase alphanumeric, so upper-casing (and undoing the '_' -> '-' map)
    round-trips exactly.
    """
    return node_id[len(PREFIX):].replace("-", "_").upper()


def _flush(writer, schema, batch):
    cols = [
        pa.array([row[i] for row in batch], type=pa.string())
        for i in range(len(schema))
    ]
    writer.write_table(pa.Table.from_arrays(cols, schema=schema))


@transient_retry()  # 6 attempts, exponential backoff, reraise on exhaustion
def _stream_flow(flow: str, asset: str) -> int:
    """Stream one dataflow's SDMX-CSV into batched all-string Parquet.

    Returns the number of observation rows written.
    """
    url = f"{DATA_BASE}/{flow}"
    client = get_client()
    written = 0
    with client.stream(
        "GET",
        url,
        params={"format": "csvdata"},
        timeout=(10.0, 300.0),  # (connect, read)
    ) as resp:
        resp.raise_for_status()  # inside the retry: 429/5xx -> retried
        # csv.reader over the streamed line iterator correctly reconstructs any
        # quoted field that spans physical lines (it pulls more lines while a
        # quote is open).
        reader = csv.reader(resp.iter_lines())
        try:
            header = next(reader)
        except StopIteration:
            raise RuntimeError(f"{flow}: empty CSV response (no header)")
        ncol = len(header)
        schema = pa.schema([(h, pa.string()) for h in header])
        with raw_parquet_writer(asset, schema) as writer:
            batch = []
            for row in reader:
                # Normalize every row to exactly the header width; map empty
                # SDMX cells to null, keep everything else verbatim as text.
                rec = [None] * ncol
                for i, v in enumerate(row[:ncol]):
                    rec[i] = v if v != "" else None
                batch.append(rec)
                if len(batch) >= BATCH_ROWS:
                    _flush(writer, schema, batch)
                    written += len(batch)
                    batch = []
            if batch:
                _flush(writer, schema, batch)
                written += len(batch)
    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = _flow_from_node_id(node_id)
    written = _stream_flow(flow, asset)
    if written == 0:
        # A live ECB dataflow always returns observations; zero means the flow
        # was discontinued/emptied or the endpoint changed shape. Fail loudly.
        raise RuntimeError(f"{flow}: 0 observations returned")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One Delta table per dataflow. The SQL is generic across flows: it keeps every
# column the flow carries (DSD dimensions + metadata + KEY/TIME_PERIOD) and only
# re-types OBS_VALUE to a real number, dropping observations with no numeric
# value. TIME_PERIOD stays text because period granularity varies across flows
# (annual "2019", monthly "2019-06", quarterly "2019-Q1", daily "2026-06-23").
def _transform_sql(dep_id: str) -> str:
    return f'''
        SELECT
            * EXCLUDE (OBS_VALUE),
            TRY_CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE
        FROM "{dep_id}"
        WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
