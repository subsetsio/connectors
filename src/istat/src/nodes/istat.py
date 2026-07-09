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

LARGE FLOWS -- the endpoint generates the whole response before sending a byte,
and for the biggest dataflows (millions of observations) it gives up and closes
the connection. There is no server-side paging, so the only lever is to shrink
the result set: TIME_PERIOD is the one dimension every flow has, so a flow that
fails whole is re-fetched as a union of time windows, bisected until each window
is small enough to serve (_iter_rows).
"""
import csv
import io
import os
import tempfile
import time

import httpx

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://esploradati.istat.it/SDMXWS/rest"
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"

# Earliest year any Istat historical series carries / latest year its population
# projections reach. The bisection universe, not a claim about any one flow.
_YEAR_MIN = 1861
_YEAR_MAX = 2060

# A flow that needs more windows than this is pathological -- fail loudly rather
# than grind through the rate limiter for hours.
_MAX_REQUESTS_PER_FLOW = 200

# Exceptions that mean "the server could not generate this response" -- i.e. the
# window is too big, so split it. Raised by get() only after its own transient
# retries are exhausted.
_TOO_BIG = (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.WriteTimeout)

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


class _DeadFlow(RuntimeError):
    """The dataflow is listed in the structure registry but no data sits behind
    it (no mapping set, or its DSD references a concept that doesn't resolve).
    Permanent upstream defect -- waive the spec, don't retry it."""


def _fetch_csv(flow_id: str, start: str = "", end: str = "", *, attempts: int = 0) -> str | None:
    """Fetch one dataflow as SDMX-CSV, optionally restricted to a time window.
    Returns None when the window holds no observations. Throttled + retried.

    `attempts` overrides the shared client's transient-retry budget for this call
    (0 = leave it alone). The full-flow probe passes 1: on a too-big flow all its
    retries are doomed and each burns up to the read timeout, so retrying four
    times before falling back to windows costs ~40 wasted minutes.
    """
    params = {"detail": "dataonly", "dimensionAtObservation": "TIME_PERIOD"}
    if start:
        params["startPeriod"] = start
    if end:
        params["endPeriod"] = end

    prior = os.environ.get("HTTP_RETRY_ATTEMPTS")
    if attempts:
        os.environ["HTTP_RETRY_ATTEMPTS"] = str(attempts)
    _throttle()
    try:
        resp = get(
            f"{BASE}/data/IT1,{flow_id},1.0/all/ALL/",
            params=params,
            headers={"Accept": CSV_ACCEPT},
            timeout=(10.0, 600.0),
        )
    finally:
        if attempts:
            if prior is None:
                os.environ.pop("HTTP_RETRY_ATTEMPTS", None)
            else:
                os.environ["HTTP_RETRY_ATTEMPTS"] = prior

    # 404 is overloaded: an empty time window and a dataflow with no data behind
    # it at all come back the same way, distinguished only by the body.
    if resp.status_code == 404:
        body = resp.text[:400]
        if "NoRecordsFound" in body:
            return None
        raise _DeadFlow(f"{flow_id}: {body.strip()}")
    if resp.status_code == 422:
        raise _DeadFlow(f"{flow_id}: {resp.text[:400].strip()}")
    resp.raise_for_status()
    return resp.text


def _iter_rows(flow_id: str):
    """Yield every observation of `flow_id`, splitting into time windows if the
    server can't serve the flow whole."""
    budget = [_MAX_REQUESTS_PER_FLOW]

    def window(start: str, end: str, *, probe: bool = False) -> str | None:
        if budget[0] <= 0:
            raise RuntimeError(f"{flow_id}: exceeded {_MAX_REQUESTS_PER_FLOW} requests")
        budget[0] -= 1
        return _fetch_csv(flow_id, start, end, attempts=1 if probe else 0)

    def split_years(lo: int, hi: int):
        try:
            text = window(str(lo), str(hi))
        except _TOO_BIG:
            if lo < hi:
                mid = (lo + hi) // 2
                yield from split_years(lo, mid)
                yield from split_years(mid + 1, hi)
            else:
                yield from split_months(lo)
            return
        if text is not None:
            yield from _rows(text)

    def split_months(year: int):
        for month in range(1, 13):
            text = window(f"{year}-{month:02d}", f"{year}-{month:02d}")
            if text is not None:
                yield from _rows(text)

    try:
        text = _fetch_csv(flow_id, attempts=1)
    except _TOO_BIG:
        print(f"[istat] {flow_id}: too large to serve whole — splitting by time window")
        yield from split_years(_YEAR_MIN, _YEAR_MAX)
        return
    if text is not None:
        yield from _rows(text)


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
