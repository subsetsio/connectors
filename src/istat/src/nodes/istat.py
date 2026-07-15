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
and for the biggest dataflows it never finishes at all (111_263: 0 bytes after
400s). There is no server-side paging, so the only lever is to shrink the result
set: TIME_PERIOD is the one dimension every flow has, so a flow that fails whole
is re-fetched as a union of time windows, subdivided until each window is small
enough to serve (_iter_rows).

THE WEDGE -- the second design constraint, and the one that killed run
20260714-180631 (three legs, each: 15 flows fetched fine at ~1.7 req/min, then
EVERY request failed for the rest of the leg). Abandoning an oversized query
does not stop Istat generating it: the endpoint keeps the work queued and stops
serving this IP until it drains. Measured directly -- a request that returned
2.4MB in 14s returned 0 bytes in 90s immediately after we walked away from a
monster, and recovered ~5 min later. So:

  * every request issued while wedged fails AND deepens the wedge, which is why
    the old top-down bisection was fatal: split_years(1861, 2060) re-requested
    the SAME monster it had just abandoned, then bisected into more monsters,
    stacking stuck jobs until the leg died. We now split DOWN from decades and
    never re-request the full range (_iter_rows).
  * after abandoning an oversized query we sleep _WEDGE_RECOVERY_S before
    touching the endpoint again (_wedge_backoff), instead of burning the next
    N specs into a wall and tripping the DAG's consecutive-failure halt.
  * the full-flow probe gets a generous read timeout: a wedge costs ~5 min, so
    waiting a few extra seconds to avoid misclassifying a merely-slow flow as a
    monster is always the cheaper trade.
"""
import csv
from functools import lru_cache
import io
import os
import tempfile
import time
import xml.etree.ElementTree as ET

import httpx

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_ndjson,
)

BASE = "https://esploradati.istat.it/SDMXWS/rest"
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"

# Earliest year any Istat historical series carries / latest year its population
# projections reach. The bisection universe, not a claim about any one flow.
_YEAR_MIN = 1861
_YEAR_MAX = 2060
# Decade grid the too-big split enters on, aligned below _YEAR_MIN. An empty
# decade costs one cheap 404 (NoRecordsFound), so scanning the dead 19th-century
# ones is far cheaper than one more monster-sized request.
_DECADE_FLOOR = 1860

# A flow that needs more windows than this is pathological -- fail loudly rather
# than grind through the rate limiter for hours.
_MAX_REQUESTS_PER_FLOW = 200

# Full-flow probes exist only to learn whether a dataflow can be served in one
# response. Read timeouts here are the time Istat spends GENERATING before the
# first byte (once bytes flow the clock resets), and giving up early is not free
# -- an abandoned query wedges the endpoint for this IP (see THE WEDGE above).
# So the probe waits well past the slowest flow we have observed serving whole
# (101_1015: 775,727 records, first byte well inside a minute) rather than
# risk paying ~5 min of wedge to save ~1 min of probe.
# GitHub-hosted runners intermittently spend >30s establishing TLS to Istat's
# SDMX endpoint; keep read caps bounded but give connection setup more room.
_CONNECT_TIMEOUT = 60.0
_FULL_PROBE_TIMEOUT = (_CONNECT_TIMEOUT, 150.0)
_WINDOW_TIMEOUT = (_CONNECT_TIMEOUT, 150.0)
_STRUCTURE_TIMEOUT = (_CONNECT_TIMEOUT, 180.0)
_CONNECT_ATTEMPTS_WHEN_RETRIES_DISABLED = 2

# How long Istat needs to drain an abandoned oversized query before it serves
# this IP again. Measured at ~5 min (wedged at +3.5 min, recovered by +5.5 min);
# padded, because under-waiting costs another full wedge rather than a retry.
_WEDGE_RECOVERY_S = float(os.environ.get("ISTAT_WEDGE_RECOVERY_S", "360"))

# Exceptions that mean "the server could not generate this response" -- i.e. the
# window is too big, so split it. Raised by get() only after its own transient
# retries are exhausted.
class _OversizedQuery(RuntimeError):
    """Istat understood the request but could not generate the result."""


_TOO_BIG = (
    _OversizedQuery,
    httpx.RemoteProtocolError,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
)

# Cross-process global rate limiter. 13s spacing => ~4.6 req/min, under the
# hard 5/min IP cap. src/main.py also forces DAG_PARALLELISM=1 because queued
# sibling specs can hit the runtime watchdog while waiting behind this lock.
_MIN_INTERVAL = 13.0
_THROTTLE_PATH = os.path.join(tempfile.gettempdir(), "istat_sdmx_throttle.lock")

# Drop SDMX free-text annotation columns (mostly empty, not analytically useful).
_DROP_PREFIX = "NOTE_"
_STR_NS = "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"

# Avoid splitting on geographic codelists unless there is no other choice: some
# Istat territory lists have >10k codes and would take days under the rate cap.
_MAX_SPLIT_CODES = 300
_PREFERRED_SPLIT_DIMS = ("FREQ", "DATA_TYPE", "DESTINATION_WINEGRAPES")

# These municipal population flows are known to time out before the generic
# splitter gets useful signal: the full-flow probe wedges Istat, then the
# required recovery sleep consumes the node timeout. Their published titles
# expose bounded annual periods, so enter at year windows directly.
_ANNUAL_FIRST_RANGES = {
    "164_305": (1991, 2001),  # Estimated resident population - Years 1991-2001
    "164_346": (1952, 1971),  # Estimated resident population - Years 1952-1971
    "164_347": (1972, 1981),  # Estimated resident population - Years 1972-1981
    "165_1245": (2024, 2050),  # Municipal population projections - Years 2024-2050
}

# This flow still makes Istat fail SQL generation for a single unkeyed year.
# Enter through compact dimensions immediately instead of paying one doomed
# unkeyed request, plus a wedge drain, for each annual window.
_DIMENSION_FIRST_ANNUAL_FLOWS = {"164_305"}


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


class _WedgeBudgetExhausted(RuntimeError):
    """This flow abandoned so many oversized queries that it is spending the
    leg asleep. Bail out and let the leg spend its budget on flows that work --
    the continuation retries this one, and a flow that keeps landing here is a
    waive-spec candidate, not something to grind on."""


# Each wedge costs _WEDGE_RECOVERY_S of doing nothing, so an unbounded number of
# them on one pathological flow would burn a whole leg (200 requests x 6 min =
# 20h) while every other flow waits. Bound the blast radius per flow instead.
_MAX_WEDGES_PER_FLOW = 6
_wedges = [0]


def _drain_wedge(flow_id: str, why: str) -> None:
    """Wait out the wedge left by an oversized query we walked away from.

    Istat keeps generating an abandoned query and refuses to serve this IP until
    it drains, so the next request is not merely likely to fail -- it extends the
    outage. Sleeping here is what keeps a single monster flow from taking the
    rest of the leg down with it.
    """
    print(f"[istat] {flow_id}: {why} — pausing {_WEDGE_RECOVERY_S:.0f}s for Istat "
          f"to drain the abandoned query before the next request")
    time.sleep(_WEDGE_RECOVERY_S)


def _wedge_backoff(flow_id: str, why: str) -> None:
    """Drain the wedge, but only while this flow still has budget for it."""
    _wedges[0] += 1
    if _wedges[0] > _MAX_WEDGES_PER_FLOW:
        raise _WedgeBudgetExhausted(
            f"{flow_id}: abandoned {_wedges[0]} oversized queries "
            f"(limit {_MAX_WEDGES_PER_FLOW}) — giving the leg back to flows that "
            f"can actually be served"
        )
    _drain_wedge(flow_id, f"{why} (wedge {_wedges[0]}/{_MAX_WEDGES_PER_FLOW})")


class _DeadFlow(RuntimeError):
    """The dataflow is listed in the structure registry but no data sits behind
    it (no mapping set, or its DSD references a concept that doesn't resolve).
    Permanent upstream defect -- waive the spec, don't retry it."""


def _fetch_csv(
    flow_id: str,
    start: str = "",
    end: str = "",
    *,
    attempts: int = 0,
    timeout: tuple[float, float] = _WINDOW_TIMEOUT,
) -> str | None:
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
    url = f"{BASE}/data/IT1,{flow_id},1.0/all/ALL/"
    tries = _CONNECT_ATTEMPTS_WHEN_RETRIES_DISABLED if attempts == 1 else 1
    try:
        for attempt_no in range(1, tries + 1):
            _throttle()
            try:
                resp = get(
                    url,
                    params=params,
                    headers={"Accept": CSV_ACCEPT},
                    timeout=timeout,
                )
                break
            except httpx.ConnectTimeout:
                if attempt_no >= tries:
                    raise
                print(f"[istat] {flow_id}: connect timed out — retrying once")
        else:
            raise RuntimeError(f"{flow_id}: request loop ended without response")
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
    if resp.status_code == 413 or "Unable to generate SQL" in resp.text[:1000]:
        raise _OversizedQuery(f"{flow_id}: {resp.text[:400].strip()}")
    resp.raise_for_status()
    return resp.text


def _lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


@lru_cache(maxsize=256)
def _flow_structure(flow_id: str) -> tuple[dict, ...]:
    """Return non-time dimensions with their codelist values for one flow."""
    _throttle()
    df_resp = get(
        f"{BASE}/dataflow/IT1/{flow_id}/1.0",
        headers={"Accept": "application/xml"},
        timeout=_STRUCTURE_TIMEOUT,
    )
    df_resp.raise_for_status()
    root = ET.fromstring(df_resp.text)
    dsd = None
    for el in root.iter():
        if _lname(el.tag) == "Ref" and el.get("class") == "DataStructure":
            dsd = el.attrib
            break
    if not dsd or not dsd.get("id"):
        raise RuntimeError(f"{flow_id}: dataflow did not expose a DSD reference")

    _throttle()
    dsd_resp = get(
        f"{BASE}/datastructure/IT1/{dsd['id']}/{dsd.get('version') or '1.0'}",
        params={"references": "all"},
        headers={"Accept": "application/xml"},
        timeout=_STRUCTURE_TIMEOUT,
    )
    dsd_resp.raise_for_status()
    root = ET.fromstring(dsd_resp.text)

    codelists = {}
    for cl in root.findall(f".//{{{_STR_NS}}}Codelist"):
        cid = cl.get("id")
        if not cid:
            continue
        codelists[cid] = [c.get("id") for c in cl.findall(f"{{{_STR_NS}}}Code") if c.get("id")]

    dims = []
    for dim in root.findall(
        f".//{{{_STR_NS}}}DataStructure/{{{_STR_NS}}}DataStructureComponents/"
        f"{{{_STR_NS}}}DimensionList/{{{_STR_NS}}}Dimension"
    ):
        did = dim.get("id")
        if not did:
            continue
        clid = None
        for el in dim.iter():
            if _lname(el.tag) == "Ref" and el.get("class") == "Codelist":
                clid = el.get("id")
                break
        dims.append({"id": did, "codes": tuple(codelists.get(clid, ()))})
    return tuple(dims)


def _split_dimensions(flow_id: str) -> list[dict]:
    dims = list(_flow_structure(flow_id))
    candidates = [
        d for d in dims
        if d["codes"] and 1 < len(d["codes"]) <= _MAX_SPLIT_CODES
    ]
    rank = {name: i for i, name in enumerate(_PREFERRED_SPLIT_DIMS)}
    candidates.sort(key=lambda d: (rank.get(d["id"], 99), len(d["codes"])))
    return candidates


def _key_for_dim(dims: list[dict], dim_id: str, code: str) -> str:
    parts = ["" for _ in dims]
    for i, dim in enumerate(dims):
        if dim["id"] == dim_id:
            parts[i] = code
            break
    return ".".join(parts)


def _fetch_csv_keyed(
    flow_id: str,
    key: str,
    start: str,
    end: str,
    *,
    attempts: int = 1,
) -> str | None:
    params = {"detail": "dataonly", "dimensionAtObservation": "TIME_PERIOD"}
    if start:
        params["startPeriod"] = start
    if end:
        params["endPeriod"] = end
    prior = os.environ.get("HTTP_RETRY_ATTEMPTS")
    if attempts:
        os.environ["HTTP_RETRY_ATTEMPTS"] = str(attempts)
    url = f"{BASE}/data/IT1,{flow_id},1.0/{key}/ALL/"
    tries = _CONNECT_ATTEMPTS_WHEN_RETRIES_DISABLED if attempts == 1 else 1
    try:
        for attempt_no in range(1, tries + 1):
            _throttle()
            try:
                resp = get(
                    url,
                    params=params,
                    headers={"Accept": CSV_ACCEPT},
                    timeout=_WINDOW_TIMEOUT,
                )
                break
            except httpx.ConnectTimeout:
                if attempt_no >= tries:
                    raise
                print(f"[istat] {flow_id}: connect timed out for keyed split — retrying once")
        else:
            raise RuntimeError(f"{flow_id}: keyed request loop ended without response")
    finally:
        if attempts:
            if prior is None:
                os.environ.pop("HTTP_RETRY_ATTEMPTS", None)
            else:
                os.environ["HTTP_RETRY_ATTEMPTS"] = prior
    if resp.status_code == 404 and "NoRecordsFound" in resp.text[:400]:
        return None
    if resp.status_code == 422:
        body = resp.text[:400]
        if "NoRecordsFound" in body:
            return None
        raise _DeadFlow(f"{flow_id}: {body.strip()}")
    if resp.status_code == 413 or "Unable to generate SQL" in resp.text[:1000]:
        raise _OversizedQuery(f"{flow_id}: {resp.text[:400].strip()}")
    resp.raise_for_status()
    return resp.text


def _iter_rows(flow_id: str):
    """Yield every observation of `flow_id`, splitting into time windows if the
    server can't serve the flow whole."""
    budget = [_MAX_REQUESTS_PER_FLOW]

    def window(start: str, end: str) -> str | None:
        if budget[0] <= 0:
            raise RuntimeError(f"{flow_id}: exceeded {_MAX_REQUESTS_PER_FLOW} requests")
        budget[0] -= 1
        return _fetch_csv(flow_id, start, end, attempts=1)

    def split_years(lo: int, hi: int):
        try:
            text = window(str(lo), str(hi))
        except _TOO_BIG:
            _wedge_backoff(flow_id, f"{lo}..{hi} too large to serve")
            if lo < hi:
                mid = (lo + hi) // 2
                yield from split_years(lo, mid)
                yield from split_years(mid + 1, hi)
            else:
                yielded = yield from split_compact_dims(str(lo), str(hi))
                if not yielded:
                    yield from split_months(lo)
            return
        if text is not None:
            yield from _rows(text, start=str(lo), end=str(hi))

    def split_compact_dims(start: str, end: str):
        """Split an otherwise-too-large time window by a compact DSD dimension.

        This is mainly for annual dataflows where TIME_PERIOD cannot be divided
        further. It also avoids the municipal REF_AREA fan-out unless no compact
        dimensions exist.
        """
        try:
            dims = _split_dimensions(flow_id)
        except Exception as exc:
            print(f"[istat] {flow_id}: could not inspect DSD for dimension split: {exc}")
            return False

        for dim in dims:
            seen = 0
            print(
                f"[istat] {flow_id}: splitting {start}..{end} by {dim['id']} "
                f"({len(dim['codes'])} codes)"
            )
            for code in dim["codes"]:
                if budget[0] <= 0:
                    raise RuntimeError(f"{flow_id}: exceeded {_MAX_REQUESTS_PER_FLOW} requests")
                budget[0] -= 1
                key = _key_for_dim(list(_flow_structure(flow_id)), dim["id"], code)
                try:
                    text = _fetch_csv_keyed(flow_id, key, start, end)
                except _TOO_BIG:
                    _wedge_backoff(
                        flow_id, f"{dim['id']}={code} over {start}..{end} too large to serve")
                    seen = 0
                    break
                if text is None:
                    continue
                for row in _rows(text, start=start, end=end):
                    seen += 1
                    yield row
            if seen:
                return True
        return False

    def split_months(year: int):
        # Only reached when a single YEAR was too big to serve, so the year holds
        # plenty of observations. If monthly windows find none, the flow's
        # TIME_PERIOD isn't month-addressable and we'd be silently dropping the
        # year -- say so instead.
        seen = 0
        for month in range(1, 13):
            start = f"{year}-{month:02d}"
            try:
                text = window(start, start)
            except _TOO_BIG:
                _wedge_backoff(flow_id, f"{start} too large to serve")
                yielded = yield from split_compact_dims(start, start)
                if yielded:
                    seen += 1
                    continue
                raise RuntimeError(
                    f"{flow_id}: {start} is too large to serve whole and no "
                    f"compact dimension split returned rows"
                )
            if text is not None:
                for row in _rows(text, start=start, end=start):
                    seen += 1
                    yield row
        if seen == 0:
            raise RuntimeError(
                f"{flow_id}: {year} is too large to serve whole but no monthly "
                f"window returned rows — cannot subdivide further"
            )

    if flow_id in _ANNUAL_FIRST_RANGES:
        lo, hi = _ANNUAL_FIRST_RANGES[flow_id]
        print(f"[istat] {flow_id}: known large annual flow — fetching {lo}..{hi} by year")
        for year in range(lo, hi + 1):
            if flow_id in _DIMENSION_FIRST_ANNUAL_FLOWS:
                yielded = yield from split_compact_dims(str(year), str(year))
                if yielded:
                    continue
            yield from split_years(year, year)
        return

    try:
        text = _fetch_csv(flow_id, attempts=1, timeout=_FULL_PROBE_TIMEOUT)
    except _TOO_BIG:
        # Enter the split ONE LEVEL DOWN, at decades. split_years(_YEAR_MIN,
        # _YEAR_MAX) would re-request the exact monster we just abandoned --
        # that request is guaranteed to fail, and each such failure extends the
        # wedge, which is how one bad flow used to take the whole leg with it.
        print(f"[istat] {flow_id}: too large to serve whole — splitting by decade")
        _wedge_backoff(flow_id, "full-flow probe abandoned")
        for lo in range(_DECADE_FLOOR, _YEAR_MAX + 1, 10):
            yield from split_years(lo, min(lo + 9, _YEAR_MAX))
        return
    if text is not None:
        yield from _rows(text)


def _period_in_window(period: str | None, start: str | None, end: str | None) -> bool:
    if not period or (not start and not end):
        return True
    if start and len(start) == 4:
        try:
            year = int(period[:4])
        except ValueError:
            return True
        return int(start) <= year <= int(end or start)
    value = period[:7]
    return (not start or value >= start) and (not end or value <= end)


def _rows(text, *, start: str | None = None, end: str | None = None):
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
        if not _period_in_window(row.get("TIME_PERIOD"), start, end):
            continue
        yield row


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name the runtime writes
    flow_id = ENTITY_BY_NODE[node_id]
    _wedges[0] = 0  # per-flow budget (specs run serially — DAG_PARALLELISM=1)

    # Detect an empty payload loudly rather than publishing a 0-row table that
    # would fail the downstream transform with a more opaque error.
    n = [0]

    def counting():
        for r in _iter_rows(flow_id):
            n[0] += 1
            yield r

    # save_raw_ndjson buffers the whole flow and only writes once the generator
    # drains, so a raised fetch leaves NO raw object behind -- which is what lets
    # the maintain gate below treat "raw present" as "flow complete".
    try:
        save_raw_ndjson(counting(), asset)
    except (httpx.ConnectTimeout, httpx.ConnectError):
        # Not this flow's fault: we are behind someone else's abandoned monster
        # (or our own, from an earlier spec) and Istat is refusing this IP. Left
        # alone the DAG would march the next specs into the same wall at ~2 min
        # each and halt the leg on 10 consecutive failures. Pay the drain once
        # so the next spec starts clean; this spec is still recorded failed and
        # the continuation retries it.
        # Unbudgeted on purpose: this drain is for the NEXT spec's benefit, not
        # this flow's, so it must happen even once this flow is over budget.
        _drain_wedge(flow_id, "Istat refused the connection (wedged)")
        raise
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

# Freshness gate -- the other half of what killed run 20260714-180631. A plain
# download node re-runs on every leg (only a MaintainSpec yields skipped_fresh),
# so all three legs re-fetched the same first 15 flows, grew no raw, and the
# chain guard correctly stopped a chain that could never advance. 1096 flows at
# ~36s each cannot fit one leg's budget, so the chain MUST resume where it left
# off, not restart.
#
# The check is deliberately local: raw_asset_exists reads the raw manifest (and
# falls back to this run's raw dir, which continuation legs share via run_id) --
# no HTTP, because maintain checks run once per asset in the parent process and
# 1096 HEADs would themselves blow the 5 req/min budget before a single flow was
# fetched. That rules out the usual source_unchanged/ETag wiring here.
#
# _FRESH_DAYS sits just under maintenance.json's cadence_days=7 so a weekly
# production run still re-pulls every flow, while the legs of one backfill
# (~11-24h end to end) skip what their predecessors already landed.
# FORCE_REFRESH=1 bypasses this entirely.
_FRESH_DAYS = 6

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"istat-{eid.lower().replace('_', '-')}",
        description=(
            f"Dataflow {eid} re-pulled in full at most every {_FRESH_DAYS}d "
            f"(maintenance.json cadence 7d); raw already landed => skip. Istat "
            f"offers no per-flow validator worth a request under the 5/min cap."
        ),
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=_FRESH_DAYS),
    )
    for eid in ENTITY_IDS
]
