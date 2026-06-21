"""Australian Bureau of Statistics — SDMX Data API connector.

Mechanism: ABS SDMX Data API (https://data.api.abs.gov.au/rest/), no auth.
Each entity is one SDMX *dataflow* (one publishable statistical collection:
CPI, Labour Force, Census tables, ERP, National Accounts, ...). The full flat
table for a dataflow is fetched in a single request:

    GET /data/{dataflowId}/all?format=csv   ->  SDMX-CSV

returning one row per observation: a variable set of dimension columns (which
DIFFER per dataflow, since each has its own DSD) plus the stable
TIME_PERIOD / OBS_VALUE / OBS_STATUS / UNIT_MEASURE columns.

Fetch shape: **stateless full re-pull** (shape 1). A bare dataflow id resolves
to the latest version, and a single CSV request returns the entire dataflow, so
each refresh re-pulls the whole table and overwrites — revisions and late
corrections are picked up for free. The corpus is per-dataflow bulk; no global
archive exists, so one fetch per dataflow is the bulk path.

Memory: flows span ~kB to **multi-GB / tens of millions of rows** (e.g. BA_GCCSA
~1.2GB / 19M rows, BA_SA2 ~2.3GB), so the body must NOT be materialized. The CSV
is parsed straight off the socket and each observation streamed to a gzipped
NDJSON raw asset via a multipart upload, so peak memory is independent of
dataflow size. (An earlier all-in-RAM version OOM-killed the runner on BA_GCCSA.)

Raw format: **NDJSON**. The dimension column set is heterogeneous across the
353 dataflows (every DSD has a different dimension list), so a single shared
parquet schema is impossible — NDJSON stores each dataflow's own columns as
strings without a schema burden, and the per-dataflow transform re-types on read.

Per-dataflow id (NOT a version-pinned key) is used — ABS,CPI,1.0.0 404s once a
flow is superseded; the bare id always resolves to latest.
"""

import csv
import io
import itertools
import json
import logging

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

logger = logging.getLogger(__name__)

SLUG = "australian-bureau-of-statistics"
BASE = "https://data.api.abs.gov.au/rest"

# The entity union — one ABS dataflow id per entry, copied verbatim from
# data/sources/australian-bureau-of-statistics/work/entity_union.json (353 ids).
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# Reverse map: spec id -> original ABS dataflow id. The id derivation
# (lower + '_'->'-') is lossy (one id, BA_SA2_2016-21, already contains a
# hyphen), so the fetch fn cannot reconstruct the dataflow id from the spec id
# by string surgery — it looks it up here instead. Pure derivation, no I/O.
SPEC_ID_TO_ENTITY = {_spec_id(eid): eid for eid in ENTITY_IDS}


class _ChunkStream(io.RawIOBase):
    """Adapt an httpx byte iterator to a readable binary file object so the csv
    module can parse the response incrementally. Bounded memory (one chunk at a
    time) and CSV-correct: the csv reader sees a real stream, so quoted fields
    with embedded commas/newlines are handled — unlike splitting on raw lines."""

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


# Generous read window: the multi-GB flows take minutes to stream end-to-end.
_TIMEOUT = httpx.Timeout(connect=15.0, read=300.0, write=15.0, pool=15.0)


@transient_retry()
def _stream_dataflow(dataflow_id: str, asset: str) -> None:
    """Stream one dataflow's SDMX-CSV and write it as gzipped NDJSON, row by row.

    The body is parsed straight off the socket and each observation is written
    through a streaming multipart upload, so peak memory is independent of the
    dataflow's size (the largest are multi-GB / tens of millions of rows). The
    bare (unversioned) id resolves to the latest version; format=csv is
    mandatory (the default is XML). A permanent 4xx (superseded/withdrawn
    dataflow) is logged and skipped so siblings still run; transient failures
    (429/5xx/timeouts) raise for the retry — each attempt re-streams from
    scratch and overwrites, so a mid-stream failure leaves no partial asset.
    """
    url = f"{BASE}/data/{dataflow_id}/all"
    client = get_client()
    with client.stream("GET", url, params={"format": "csv"}, timeout=_TIMEOUT) as resp:
        code = resp.status_code
        if 400 <= code < 500 and code != 429:
            resp.read()
            logger.warning(
                "ABS dataflow %s permanently unavailable (HTTP %s) at %s; skipping",
                dataflow_id, code, resp.request.url,
            )
            return
        if code != 200:
            resp.read()
            resp.raise_for_status()  # 429 / 5xx -> transient, retried

        # SDMX-CSV: one header row + one row per observation. Columns are the
        # dataflow's dimensions plus the stable TIME_PERIOD/OBS_VALUE/... fields.
        # Keep every value as a string — the per-dataflow transform re-types.
        text = io.TextIOWrapper(
            io.BufferedReader(_ChunkStream(resp.iter_bytes(1 << 16)), buffer_size=1 << 20),
            encoding="utf-8",
            newline="",
        )
        reader = csv.DictReader(text)
        first = next(reader, None)
        if first is None:
            logger.warning("ABS dataflow %s returned an empty CSV; skipping", dataflow_id)
            return

        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            for row in itertools.chain((first,), reader):
                out.write(json.dumps(dict(row), separators=(",", ":")))
                out.write("\n")
                n += 1
        print(f"  -> streamed {asset} ({n:,} rows)")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _stream_dataflow(SPEC_ID_TO_ENTITY[node_id], asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# One published Delta table per dataflow. The transform is SQL-only: it reads
# the dataflow's NDJSON (every column arrives as a string), keeps the full
# dimension set as-is (it differs per dataflow), casts the numeric observation,
# and drops non-numeric / missing observations. `SELECT * REPLACE (...)` keeps
# whatever dimension columns that dataflow has without enumerating them.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
            FROM "{s.id}"
            WHERE OBS_VALUE IS NOT NULL
              AND TRIM(CAST(OBS_VALUE AS VARCHAR)) <> ''
              AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
