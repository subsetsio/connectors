"""European Central Bank — SDMX 2.1 RESTful web service (ECB Data Portal).

One published Delta table per ECB dataflow (the rank-accepted entity union in
``constants.ENTITY_IDS``). Each dataflow is fetched in full as SDMX-CSV from
``/service/data/{FLOW}`` (key omitted = every series in the flow) and stored as
gzip NDJSON, one record per observation.

Fetch shape: **stateless full re-pull**. The whole flow is re-fetched every
refresh and overwritten; revisions and late corrections are picked up for free.
The response is streamed and parsed line-by-line into NDJSON so memory stays
bounded regardless of flow size (the largest flows — SHS, MMSR, SEC — can be
many millions of observations).

NDJSON (not parquet) is deliberate: each dataflow carries its own DSD dimension
columns (EXR has CURRENCY/EXR_TYPE, YC has FM_MATURITY/DATA_TYPE_FM, ...), so
there is no single stable schema across the 75 assets. NDJSON lets each asset
keep its own columns and lets the transform re-type on read.
"""

import csv
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "european-central-bank"
PREFIX = f"{SLUG}-"
DATA_BASE = "https://data-api.ecb.europa.eu/service/data"


def _flow_from_node_id(node_id: str) -> str:
    """Recover the upstream dataflow id from a download spec id.

    Inverse of ``f"{SLUG}-{eid.lower().replace('_', '-')}"``. ECB flow ids are
    uppercase alphanumeric, so upper-casing (and undoing the '_' -> '-' map)
    round-trips exactly.
    """
    return node_id[len(PREFIX):].replace("-", "_").upper()


@transient_retry()  # 6 attempts, exponential backoff, reraise on exhaustion
def _stream_flow(flow: str, asset: str) -> int:
    """Stream one dataflow's SDMX-CSV into gzip NDJSON. Returns rows written."""
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
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            for row in reader:
                # Map empty SDMX cells to null; keep everything else verbatim.
                rec = {h: (v if v != "" else None) for h, v in zip(header, row)}
                out.write(json.dumps(rec, separators=(",", ":")))
                out.write("\n")
                written += 1
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
