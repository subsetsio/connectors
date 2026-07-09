"""Australian Bureau of Statistics — SDMX Data API connector.

Mechanism: ABS SDMX Data API (https://data.api.abs.gov.au/rest/), no auth.
Each entity is one SDMX *dataflow* — one publishable statistical collection
(CPI, Labour Force, Census tables, ERP, National Accounts, ...). The full flat
table for a dataflow comes back in a single request:

    GET /data/{dataflowId}/all?format=csv   ->  SDMX-CSV

one row per observation: a variable set of dimension columns (which DIFFER per
dataflow, since each has its own DSD) plus the stable
DATAFLOW / TIME_PERIOD / OBS_VALUE / OBS_STATUS / UNIT_MEASURE columns. The
bare, unversioned id is used deliberately — a version-pinned key (ABS,CPI,1.0.0)
404s once the flow is superseded, while the bare id always resolves to latest.

Fetch shape: **stateless full re-pull**. One request returns the whole dataflow,
and ABS restates history on every release, so a stored watermark would silently
skip revised observations.

Memory: flows span a few kB to **multi-GB** — BA_SA2_2016-21 is a 2.86 GB CSV,
and several Census tables clear 400 MB. The body must never be materialized (an
earlier all-in-RAM version of this connector OOM-killed the runner), so the CSV
is parsed straight off the socket and streamed into a row-group-streamed
parquet file. Peak memory is one record batch, independent of dataflow size.
This is why the fetch reaches for `get_client().stream(...)` rather than
`subsets_utils.get`, which buffers the whole body.

Raw format: **parquet**, with a schema derived per dataflow from its own CSV
header. Every dimension column is pinned to string: ABS codes are
numeric-looking but are not numbers — postal areas ("0800"), SA2 codes
("101031016"), MEASURE ("1") — and type inference would strip leading zeros.
Only OBS_VALUE is numeric.

A permanently-dead dataflow (4xx) fails its own node and no other; the harness
records the per-spec failure, and `waive-spec` is the path for an upstream that
stays dead.
"""

import io

import httpx
import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)

from constants import ENTITY_IDS

SLUG = "australian-bureau-of-statistics"
BASE = "https://data.api.abs.gov.au/rest"

# Generous read window: the multi-GB flows take minutes to stream end-to-end.
_TIMEOUT = httpx.Timeout(connect=15.0, read=300.0, write=15.0, pool=15.0)

# Census 2021/2016 output tables are a fixed vintage — only ever corrected, never
# extended. Re-pulling ~20 GB of frozen tables every refresh is pure waste; a
# yearly refetch still picks up a correction. FORCE_REFRESH=1 bypasses.
_CENSUS_MAX_AGE_DAYS = 365


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# Reverse map: spec id -> original ABS dataflow id. The id derivation
# (lower + '_'->'-') is lossy — one id, BA_SA2_2016-21, already contains a
# hyphen — so the fetch fn cannot reconstruct the dataflow id by string surgery.
# Pure derivation, no I/O.
SPEC_ID_TO_ENTITY = {_spec_id(eid): eid for eid in ENTITY_IDS}


class _ChunkStream(io.RawIOBase):
    """Adapt an httpx byte iterator to a readable binary file object.

    Bounded memory: one chunk at a time. pyarrow's CSV reader parses through
    this incrementally, so quoted fields with embedded commas or newlines are
    handled correctly — unlike splitting the body on raw line boundaries.
    """

    def __init__(self, chunks):
        self._chunks = chunks
        self._buf = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self._buf:
            try:
                self._buf = next(self._chunks)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n], self._buf = self._buf[:n], self._buf[n:]
        return n


def _peek_header(buffered: io.BufferedReader) -> list[str]:
    """Read the CSV header without consuming it.

    The parquet schema has to be declared before the CSV reader is built, and
    the column set is only knowable from the dataflow's own header — each DSD
    has a different dimension list. `peek` leaves the bytes in the buffer, so
    the reader still sees a well-formed CSV starting at the header row.
    """
    chunk = buffered.peek(1 << 20)
    end = chunk.find(b"\n")
    if end == -1:
        raise ValueError(
            f"no header line in the first {len(chunk)} bytes of the SDMX-CSV "
            f"response: {chunk[:200]!r}"
        )
    return chunk[:end].decode("utf-8-sig").rstrip("\r").split(",")


def _schema_for(columns: list[str], obs_value_type: pa.DataType) -> pa.Schema:
    if "OBS_VALUE" not in columns:
        raise ValueError(f"SDMX-CSV header carries no OBS_VALUE column: {columns}")
    return pa.schema(
        [(c, obs_value_type if c == "OBS_VALUE" else pa.string()) for c in columns]
    )


@transient_retry()
def _stream_dataflow(dataflow_id: str, asset: str, obs_value_type: pa.DataType) -> int:
    """Stream one dataflow's SDMX-CSV straight into raw parquet. Returns rows.

    Retried as a unit: `raw_parquet_writer` only commits to the raw manifest on
    a clean exit, so a mid-stream failure leaves an uncommitted object behind
    rather than a truncated asset, and the retry re-streams from scratch.
    """
    url = f"{BASE}/data/{dataflow_id}/all"
    with get_client().stream(
        "GET", url, params={"format": "csv"}, timeout=_TIMEOUT
    ) as resp:
        if resp.status_code != 200:
            resp.read()
            resp.raise_for_status()  # 429/5xx retried; other 4xx fails this node

        buffered = io.BufferedReader(
            _ChunkStream(resp.iter_bytes(1 << 16)), buffer_size=1 << 20
        )
        schema = _schema_for(_peek_header(buffered), obs_value_type)
        convert = pacsv.ConvertOptions(column_types=schema, strings_can_be_null=True)

        rows = 0
        with pacsv.open_csv(buffered, convert_options=convert) as reader:
            with raw_parquet_writer(asset, reader.schema) as writer:
                for batch in reader:
                    writer.write_batch(batch)
                    rows += batch.num_rows
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataflow_id = SPEC_ID_TO_ENTITY[node_id]
    try:
        rows = _stream_dataflow(dataflow_id, asset, pa.float64())
    except pa.ArrowInvalid as exc:
        # SDMX declares OBS_VALUE numeric, and it is on every flow probed. Rather
        # than lose a flow that carries coded observations, keep the raw as
        # string and let the transform stage re-type it.
        print(f"  -> {asset}: OBS_VALUE not numeric ({exc}); refetching as string")
        rows = _stream_dataflow(dataflow_id, asset, pa.string())

    if rows == 0:
        raise RuntimeError(f"{asset}: dataflow {dataflow_id} returned 0 observations")
    print(f"  -> streamed {asset} ({rows:,} rows)")


def _is_census_vintage(entity_id: str) -> bool:
    return entity_id.startswith("C21_") or entity_id.startswith("ABS_C16_")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=_spec_id(eid),
        description=(
            "Census output tables are a fixed vintage per "
            "https://www.abs.gov.au/census — corrected, never extended. "
            "Refetch at most yearly (inferred — ABS publishes no correction "
            "schedule)."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=_CENSUS_MAX_AGE_DAYS),
    )
    for eid in ENTITY_IDS
    if _is_census_vintage(eid)
]
