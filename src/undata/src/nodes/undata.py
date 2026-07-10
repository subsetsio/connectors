"""UNdata connector — SDMX 2.1 REST (https://data.un.org/ws/rest).

UNdata redistributes a small, curated set of SDMX dataflows (15 as of 2026-06)
from UNSD, Eurostat, World Bank, UNESCO-UIS and the IAEG SDG/MDG programmes.
Each dataflow has its own data structure (distinct dimension list), so each is
published as one long-format Delta table — DATAFLOW + dimension columns +
TIME_PERIOD + obs_value.

Fetch shape: **stateless full re-pull**. The whole corpus (tens of MB to a few
hundred MB per flow; the SDG harmonized flow is the large one) is cheap to
re-fetch every run, so there is no watermark/cursor/state — re-fetching the full
flow each refresh picks up revisions and late corrections for free. SDMX exposes
startPeriod/endPeriod time filters but no since/modifiedAfter change feed, so an
incremental delta is not available anyway.

Each flow is fetched as flat SDMX-CSV (`Accept: application/vnd.sdmx.data+csv`)
in a single unpaginated request and streamed straight to gzipped NDJSON so peak
memory stays bounded regardless of flow size. All cell values are stored as
strings (or null for blanks); the transform casts OBS_VALUE to DOUBLE.
"""

from __future__ import annotations

import csv
import json

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, get_client, raw_writer

BASE = "https://data.un.org/ws/rest"
ACCEPT_CSV = "application/vnd.sdmx.data+csv"

# The rank-accepted entity union — the real (case-sensitive) SDMX dataflow ids.
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return f"undata-{entity_id.lower().replace('_', '-')}"


def _dataflow_for(node_id: str) -> str:
    """Recover the case-sensitive SDMX dataflow id from a download spec id."""
    for eid in ENTITY_IDS:
        if _spec_id(eid) == node_id:
            return eid
    raise KeyError(f"no dataflow maps to node id {node_id!r}")


def _is_transient(exc: BaseException) -> bool:
    # data.un.org's SDMX-RI server is intermittently flaky on large /data
    # queries — it drops connections ("Server disconnected without sending a
    # response", a RemoteProtocolError) and stalls under load (read/connect
    # timeouts). All of these subclass httpx.TransportError, so retry the lot;
    # outages can last minutes, hence the long backoff / high attempt count.
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=5, max=300),
    reraise=True,
)
def _download_dataflow(dataflow_id: str, asset: str) -> int:
    """Stream one dataflow's SDMX-CSV to gzipped NDJSON. Returns row count.

    Streaming (httpx stream -> csv.reader -> raw_writer) keeps peak memory at a
    single row regardless of flow size. csv.reader consumes the line iterator,
    so quoted fields containing commas or embedded newlines are parsed
    correctly. All HTTP goes through the subsets_utils client.
    """
    client = get_client()
    url = f"{BASE}/data/{dataflow_id}/all"
    timeout = httpx.Timeout(60.0, read=900.0, write=60.0, pool=60.0)
    with client.stream("GET", url, headers={"Accept": ACCEPT_CSV}, timeout=timeout) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines())
        header = next(reader, None)
        if not header:
            raise ValueError(f"{dataflow_id}: empty SDMX-CSV response (no header)")
        ncols = len(header)
        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
            for row in reader:
                rec = {}
                for i in range(ncols):
                    val = row[i] if i < len(row) else None
                    rec[header[i]] = val if val not in (None, "") else None
                f.write(json.dumps(rec, separators=(",", ":")))
                f.write("\n")
                n += 1
    return n


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataflow_id = _dataflow_for(node_id)
    n = _download_dataflow(dataflow_id, asset)
    if n == 0:
        # All 15 flows return data; an empty body means the endpoint changed.
        raise ValueError(f"{dataflow_id}: SDMX-CSV returned 0 data rows")
    print(f"  {dataflow_id}: {n:,} observations -> {asset}")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download") for eid in ENTITY_IDS
]
