"""Istat (Italian National Institute of Statistics) — SDMX 2.1 REST connector.

Mechanism: per-dataflow SDMX-CSV download from the esploradati.istat.it endpoint
(agency IT1). One DOWNLOAD_SPEC per rank-accepted dataflow; each fetches the full
series in SDMX-CSV (detail=dataonly) and saves it as NDJSON (the dimension
column set differs per dataflow, so a single shared parquet schema is impossible
-- NDJSON carries each flow's own columns).

RATE LIMIT -- the dominant design constraint. Istat enforces ~5 requests/minute
per IP and BLOCKS the IP for 1-2 days when exceeded. Every data fetch counts.
We throttle GLOBALLY across processes with an exclusive file lock held during the
spacing wait (_throttle), so even if DAG_PARALLELISM>1 spawns sibling specs on
the same host/IP, requests are serialized to <=1 per _MIN_INTERVAL seconds
(~4.6/min, under the 5/min cap). Transient 429/5xx are retried with backoff.

Stateless full re-pull: no incremental filter is reliable on this endpoint, so
every refresh re-fetches the full series and overwrites. (Maintain-step freshness
gating is authored separately.)
"""
import csv
import io
import os
import tempfile
import time


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://esploradati.istat.it/SDMXWS/rest"
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"

# Cross-process global rate limiter. 13s spacing => ~4.6 req/min, under the
# hard 5/min IP cap. The lock is held during the sleep so concurrent spawn
# subprocesses (same IP) serialize instead of bursting.
_MIN_INTERVAL = 13.0
_THROTTLE_PATH = os.path.join(tempfile.gettempdir(), "istat_sdmx_throttle.lock")

# Drop SDMX free-text annotation columns (mostly empty, not analytically useful).
_DROP_PREFIX = "NOTE_"


def _throttle() -> None:
    import fcntl  # POSIX (CI is ubuntu, dev is macOS) -- both have fcntl
    fd = os.open(_THROTTLE_PATH, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.read(fd, 64).decode("ascii", "ignore").strip()
        try:
            last = float(raw)
        except ValueError:
            last = 0.0
        wait = _MIN_INTERVAL - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
        os.lseek(fd, 0, os.SEEK_SET)
        os.ftruncate(fd, 0)
        os.write(fd, str(time.time()).encode("ascii"))
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _fetch_csv(flow_id: str) -> str:
    """Fetch one dataflow as SDMX-CSV (full series). Throttled + retried."""
    url = f"{BASE}/data/IT1,{flow_id},1.0/all/ALL/"
    _throttle()
    resp = get(
        url,
        params={"detail": "dataonly", "dimensionAtObservation": "TIME_PERIOD"},
        headers={"Accept": CSV_ACCEPT},
        timeout=(10.0, 600.0),
    )
    resp.raise_for_status()
    return resp.text


def _rows(text):
    """Yield row dicts from SDMX-CSV text, dropping NOTE_* columns and coercing
    empty strings to None. Generator => streamed to the NDJSON writer, so peak
    memory is ~ the response size, not response + materialized list."""
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        return
    keep = [(i, h) for i, h in enumerate(header) if not h.startswith(_DROP_PREFIX)]
    for rec in reader:
        if not rec:
            continue
        row = {}
        for i, h in keep:
            v = rec[i] if i < len(rec) else ""
            row[h] = v if v != "" else None
        yield row


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name the runtime writes
    flow_id = ENTITY_BY_NODE[node_id]
    text = _fetch_csv(flow_id)

    # Detect an empty payload loudly rather than publishing a 0-row table that
    # would fail the downstream transform with a more opaque error.
    n = [0]

    def counting():
        for r in _rows(text):
            n[0] += 1
            yield r

    save_raw_ndjson(counting(), asset)
    if n[0] == 0:
        raise AssertionError(f"{asset}: dataflow {flow_id} returned 0 observations")


from constants import ENTITY_IDS

ENTITY_BY_NODE = {f"istat-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"istat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
