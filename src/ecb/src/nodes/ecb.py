"""ECB Data Portal connector — SDMX 2.1 RESTful web service.

Access mechanism (from research): `sdmx_21`. The ECB Data Portal exposes ~150
dataflows (EXR exchange rates, YC yield curves, BSI/MIR banking, HICP/ICP
prices, BOP balance of payments, ...). Each dataflow is pulled in full as
SDMX-CSV with one request:

    https://data-api.ecb.europa.eu/service/data/{FLOW}?format=csvdata

An empty series key returns every series in the flow (the bulk path — there is
no all-flows archive). NOTE: the URL must NOT have a trailing slash after the
flow id (`/service/data/YC/` 404s; `/service/data/YC` returns the full flow).

Fetch shape: **stateless full re-pull** (shape 1). The whole corpus is re-pulled
each run and overwritten — revisions and late corrections are picked up for free.
The flows are large (several exceed 200MB of uncompressed CSV / hundreds of
thousands of rows), so each flow is **streamed** and written to parquet in bounded
row-group batches via `raw_parquet_writer` — never materialised whole in memory.
zstd compresses the heavily-repeated dimension strings to a fraction of the CSV
size. The source documents the `updatedAfter=` incremental filter, but full
re-pull is correct here and keeps the connector trivially idempotent.

Each SDMX-CSV flow has a stable-within-flow but cross-flow-varying column set:
always `KEY`, the flow's dimension columns, `TIME_PERIOD`, `OBS_VALUE`, plus
SDMX attributes (`FREQ`, `OBS_STATUS`, `TITLE`/`TITLE_COMPL`, `UNIT`, ...). We
normalise every flow down to a fixed curated column set keyed by header name, so
a single explicit parquet schema is the contract for every flow (absent columns
become null). The full dimension breakdown is preserved inside the dot-separated
`series_key`.
"""
import csv
import io
import time

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    load_state,
    save_state,
    raw_parquet_writer,
    transient_retry,
)

STATE_VERSION = 1

BASE = "https://data-api.ecb.europa.eu/service/data"

# Dataflow ids — the entity union (every collect entity ranked at/above the
# publish threshold). Copied from data/sources/ecb/work/entity_union.json.
from constants import ENTITY_IDS

# Curated, fixed raw schema — every flow normalises into this. Stored as strings
# (faithful to the CSV); the transform casts. Absent columns => null.
RAW_SCHEMA = pa.schema([
    ("series_key", pa.string()),
    ("freq", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.string()),
    ("obs_status", pa.string()),
    ("title", pa.string()),
    ("unit", pa.string()),
    ("unit_mult", pa.string()),
    ("decimals", pa.string()),
])

BATCH_ROWS = 100_000  # rows per parquet row group flushed during streaming


def _flow_id(node_id: str) -> str:
    """Recover the SDMX dataflow id from the spec id (`ecb-yc` -> `YC`)."""
    return node_id[len("ecb-"):].replace("-", "_").upper()


def _normalise_row(idx: dict, row: list) -> dict:
    """Pull the curated columns out of one CSV row by header position."""
    def col(name):
        i = idx.get(name)
        if i is None or i >= len(row):
            return None
        v = row[i]
        return v if v != "" else None

    title = col("TITLE_COMPL") or col("TITLE")
    return {
        "series_key": col("KEY"),
        "freq": col("FREQ"),
        "time_period": col("TIME_PERIOD"),
        "obs_value": col("OBS_VALUE"),
        "obs_status": col("OBS_STATUS"),
        "title": title,
        "unit": col("UNIT"),
        "unit_mult": col("UNIT_MULT"),
        "decimals": col("DECIMALS"),
    }


def _flush(writer, buf):
    table = pa.Table.from_pylist(buf, schema=RAW_SCHEMA)
    writer.write_table(table)


@transient_retry()
def _stream_flow_to_parquet(asset: str, flow: str) -> int:
    """Stream one full dataflow CSV and write it to parquet in batches.

    Re-runs from scratch on a transient mid-stream failure (the parquet writer
    re-opens and overwrites the asset), so the whole call is idempotent.
    """
    url = f"{BASE}/{flow}"
    client = get_client()
    written = 0
    with client.stream(
        "GET", url, params={"format": "csvdata"}, timeout=httpx.Timeout(10.0, read=300.0)
    ) as resp:
        resp.raise_for_status()
        # Decode the byte stream to text lines for csv.reader. csv.reader pulls
        # further lines itself to span quoted fields, so multi-line descriptive
        # attributes parse correctly.
        text = io.TextIOWrapper(_ByteStream(resp.iter_bytes()), encoding="utf-8", newline="")
        reader = csv.reader(text)
        header = next(reader, None)
        if header is None:
            raise AssertionError(f"{flow}: empty CSV response (no header)")
        idx = {name: i for i, name in enumerate(header)}
        if "KEY" not in idx or "OBS_VALUE" not in idx:
            raise AssertionError(f"{flow}: unexpected header {header[:6]}")

        with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
            buf = []
            for row in reader:
                if not row:
                    continue
                buf.append(_normalise_row(idx, row))
                if len(buf) >= BATCH_ROWS:
                    _flush(writer, buf)
                    written += len(buf)
                    buf = []
            if buf:
                _flush(writer, buf)
                written += len(buf)
    return written


class _ByteStream(io.RawIOBase):
    """Adapt an httpx byte-chunk iterator into a readable binary stream."""

    def __init__(self, chunks):
        self._chunks = iter(chunks)
        self._rest = b""

    def readable(self):
        return True

    def readinto(self, b):
        if not self._rest:
            try:
                self._rest = next(self._chunks)
            except StopIteration:
                return 0
        n = min(len(b), len(self._rest))
        b[:n] = self._rest[:n]
        self._rest = self._rest[n:]
        return n


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = _flow_id(node_id)
    state = load_state(asset)

    try:
        n = _stream_flow_to_parquet(asset, flow)
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        # Permanent (4xx except 429): mark skipped with a TTL and return cleanly
        # so one withdrawn flow doesn't fail the run. Transient codes are already
        # retried above; reaching here means the code is genuinely permanent.
        if 400 <= code < 500 and code != 429:
            skipped = state.get("skipped", {})
            skipped[flow] = {
                "reason": f"HTTP {code} on {BASE}/{flow}",
                "expires_at": int(time.time()) + 14 * 86400,
            }
            print(f"  ! {flow}: permanent HTTP {code}; wrote skipped marker")
            save_state(asset, {"schema_version": STATE_VERSION, "skipped": skipped})
            return
        raise

    save_state(asset, {
        "schema_version": STATE_VERSION,
        "rows": n,
        "last_success_at": int(time.time()),
    })


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ecb-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per flow: a thin parse-and-type pass over the raw
# CSV columns. TIME_PERIOD is kept as text because frequencies are mixed within
# a flow (daily / monthly / quarterly / annual), so a single DATE cast is unsafe.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                series_key,
                freq,
                time_period,
                CAST(obs_value AS DOUBLE)  AS value,
                obs_status,
                title,
                unit
            FROM "{s.id}"
            WHERE obs_value IS NOT NULL
              AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
        ''',
        key=("series_key", "time_period"),
        temporal="time_period",
    )
    for s in DOWNLOAD_SPECS
]
