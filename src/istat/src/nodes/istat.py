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
  * but ONLY when we actually abandoned one. A "too big" that Istat RETURNS
    ("Unable to generate SQL") left nothing generating and owes no drain --
    charging it 6 min of sleep, and one of the 6 per-flow wedges, is how a
    splittable flow runs out of budget before it runs out of splits to try
    (_too_big_backoff).
  * the full-flow probe gets a generous read timeout: a wedge costs ~5 min, so
    waiting a few extra seconds to avoid misclassifying a merely-slow flow as a
    monster is always the cheaper trade.

A WEDGE IS INFERRED, NOT OBSERVED -- and the inference is only available once
Istat has served this runner. Istat fronts the endpoint with a filter
(esploradati.istat.it -> 01a-filtro.istat.it) that silently drops packets from
an IP it dislikes; that looks like a connect TIMEOUT, not a refusal, which is
indistinguishable from a wedge if you only look at one request. Run
20260715-084715 blackholed on its first request, called it a wedge, and charged
all 25 specs 60s + 60s + a 360s drain: 3.5h wall clock, 2.5h asleep, zero
recoveries, 888 specs never attempted. So the drain must be earned
(_endpoint_state): before the leg's first response there is nothing we could
have wedged, and a drain that has failed _MAX_DRAINED_CONNECT_FAILURES times
running has disproved itself. Both cases raise _EndpointUnreachable -- external
and source-wide, never a waiver candidate.

WHICH "TOO BIG" IS IT -- the body, not the status. Istat answers "Unable to
generate SQL" under the same HTTP status it uses for a structurally broken
dataflow, so the response body has to be read before the status is trusted
(_classify_csv). Read the other way round, an oversized window is misfiled as a
permanent _DeadFlow: the splitter never sees it, the spec fails hard, and the
error message invites a waiver for a flow that is merely large (164_305).
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
_MAX_SPLIT_CODES = 500
_PREFERRED_SPLIT_DIMS = (
    "FREQ",
    "SEX",
    "PERS_EMPL_SIZE_CLASS",
    "DATA_TYPE",
    "AGE",
    "DESTINATION_WINEGRAPES",
)

# A split dim only shrinks the result if the flow actually spreads data across
# its codes -- and a CODELIST does not say which codes are populated. 183_1163
# advertises 8 FREQ codes but is annual, so the top-ranked split, FREQ=A, asks
# for the whole flow again: the same monster the probe just abandoned, at 150s
# + a 6-min wedge, to learn nothing. It then does it once per wedge until the
# budget is gone, which is why this flow has failed every run so far.
#
# Knowing which codes are populated would need an availableconstraint request
# per flow, and 1096 of those do not fit the 5/min cap. So a flow whose split
# dim has been OBSERVED useless declares it here (verified against the live DSD:
# 183_1163's remaining candidates are PERS_EMPL_SIZE_CLASS/44 then DATA_TYPE/260,
# with REF_AREA/12471 and ECON_ACTIVITY_NACE_2007/2061 over _MAX_SPLIT_CODES).
# Do not add FREQ for 164_305 -- there it is what makes the flow serve (FREQ+SEX).
_SKIP_SPLIT_DIMS = {"183_1163": frozenset({"FREQ"})}

# These municipal population flows are known to time out before the generic
# splitter gets useful signal: the full-flow probe wedges Istat, then the
# required recovery sleep consumes the node timeout. Their published titles
# expose bounded annual periods, so enter at year windows directly.
_ANNUAL_FIRST_RANGES = {
    "164_305": (1991, 2001),  # Estimated resident population - Years 1991-2001
    "164_346": (1952, 1971),  # Estimated resident population - Years 1952-1971
    "164_347": (1972, 1981),  # Estimated resident population - Years 1972-1981
    "165_1245": (2024, 2050),  # Municipal population projections - Years 2024-2050
    "183_1163": (2019, 2022),  # Enterprises by municipality - latest structural years
}

# This flow still makes Istat fail SQL generation for a single unkeyed year.
# Enter through compact dimensions immediately instead of paying one doomed
# unkeyed request, plus a wedge drain, for each annual window.
_DIMENSION_FIRST_ANNUAL_FLOWS = {"164_305", "183_1163"}

# Flows dimensioned by CL_ITTER107 (12,471 municipalities). They are not dead
# and not wedging us -- they are simply enormous, and the damage they do is to
# the specs BEHIND them.
#
# What run 20260715-131758 actually proved (R2 http_requests.csv, not
# inference). Istat was healthy for the first 90s: the 8 known-dead flows
# answered 404/422 in ~1.5s each. Then 164_305 ran, and every dimension it can
# split on except REF_AREA still leaves the full municipal fan-out in the
# request, so its only servable shape is a whole-year query. Istat DID serve
# those -- and got monotonically slower doing it: 481s, then 833s, then 905s,
# then read timeouts, and then it stopped answering this IP at all. The last
# 54 min of that leg were 60s connect timeouts, one pair per spec, and the
# endpoint never came back.
#
# So the "blackhole" the previous sessions read as an external Istat outage is
# self-inflicted: generating ~10 min of result per request is what sheds us.
# (Confirmed from the other side: Istat answers this dev machine in 3.9s.)
# The cost was not the 2h these flows burned, it was the 903 never-run specs
# that died behind them having never issued a single request.
#
# Nothing here fixes 164_305 -- 12,471 REF_AREA x 471 DATA_TYPE x 343 AGE has
# no split that is both small enough for Istat to generate and few enough
# requests to fit the 5/min IP cap (pinning FREQ+SEX+AGE is ~1,029 requests per
# year, ~41h for the flow). This ORDERS them last instead, so a leg banks every
# cheap flow before any monster gets a chance to spoil the endpoint, and their
# failure is contained to themselves.
_HEAVY_FLOWS = frozenset(_ANNUAL_FIRST_RANGES)


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


# ---------------------------------------------------------------------------
# ENDPOINT REACHABILITY -- distinct from THE WEDGE, and the two must not be
# conflated (run 20260715-084715 died of exactly that).
#
# A wedge is inferred, never observed: we abandon a query, the next request
# fails, and we blame the query we walked away from. That inference is only
# available once Istat has actually served this runner. Before the first
# response of a leg there is nothing we could have wedged -- so a connect
# failure there is Istat's filter (esploradati.istat.it -> 01a-filtro.istat.it)
# blackholing this runner, and a drain cannot fix what we did not cause.
#
# The distinction is not academic. 20260715-084715 connect-timed-out on its
# FIRST request and charged every one of 25 specs 60s + 60s + a 360s drain:
# 3.5h of wall clock, 2.5h of it asleep, zero recoveries, leg halted with 888
# specs unrun. A drain that has failed twice running has disproved itself; keep
# probing (the outage is external and may lift) but stop paying for it.
#
# Node specs run as separate subprocesses, so this state lives in a file beside
# the throttle -- same lifetime, one runner, one leg.
_ENDPOINT_PATH = os.path.join(tempfile.gettempdir(), "istat_endpoint_health")

# Consecutive node-level connect failures still worth a drain. Past this the
# drain has demonstrably not helped, so it is pure cost.
_MAX_DRAINED_CONNECT_FAILURES = 2


class _EndpointUnreachable(RuntimeError):
    """Istat is not completing TCP/TLS for this runner at all.

    Source-wide and external: not this flow's defect, so never a waive
    candidate. Fail fast and cheap -- the leg's consecutive-failure halt will
    stop the run in minutes instead of hours, and the next dispatch (from a
    different runner IP) starts clean."""


def _endpoint_state(record: str | None = None) -> tuple[bool, int]:
    """Read, and optionally update, the shared endpoint-health record.

    record=None reads; "served" marks the endpoint as having answered this leg
    and clears the failure streak; "connect_failure" extends the streak.
    Returns (served_this_leg, consecutive_connect_failures).
    """
    import fcntl
    fd = os.open(_ENDPOINT_PATH, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.read(fd, 256).decode("ascii", "ignore").strip()
        try:
            served, streak = raw.split(",", 1)
            state = (served == "1", int(streak))
        except ValueError:
            state = (False, 0)

        if record == "served":
            state = (True, 0)
        elif record == "connect_failure":
            state = (state[0], state[1] + 1)

        if record:
            os.lseek(fd, 0, os.SEEK_SET)
            os.ftruncate(fd, 0)
            os.write(fd, f"{'1' if state[0] else '0'},{state[1]}".encode("ascii"))
        return state
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _get(url: str, **kwargs):
    """get(), plus the reachability bookkeeping every response feeds.

    Any response proves the endpoint is answering -- a 404 for a dead flow says
    as much about the network as a 200 does -- so this records "served" on
    status, not on success.
    """
    resp = get(url, **kwargs)
    _endpoint_state("served")
    return resp


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


# Not every "too big" leaves a wedge behind, and treating them alike is expensive.
# _OversizedQuery is a response Istat RETURNED: it looked at the query, decided it
# could not build the SQL, and answered (~45s for 164_305). Nothing is queued,
# nothing is draining, and the next request may go out as soon as the throttle
# allows. A read/protocol failure is the opposite -- WE walked away from a query
# Istat is still generating, and it refuses this IP until that drains (THE WEDGE).
#
# Conflating them charges every returned "too big" a 6-minute sleep it does not
# owe, and spends one of the 6 per-flow wedges on it. A flow that answers "Unable
# to generate SQL" quickly and needs to try several splits to find one Istat will
# serve would exhaust its wedge budget long before it ran out of splits to try --
# which is exactly the wall 164_305 is up against.
_ABANDONED_MIDFLIGHT = (
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.RemoteProtocolError,
)


def _too_big_backoff(flow_id: str, exc: BaseException, why: str) -> None:
    """Pay the wedge drain only when the failure actually left a query behind."""
    if isinstance(exc, _ABANDONED_MIDFLIGHT):
        _wedge_backoff(flow_id, why)
        return
    # Server-declined (_OversizedQuery / 413): nothing to drain, split on.
    print(f"[istat] {flow_id}: {why} — Istat declined to build it (no query left "
          f"generating, so no drain owed); splitting further")


class _DeadFlow(RuntimeError):
    """The dataflow is listed in the structure registry but no data sits behind
    it (no mapping set, or its DSD references a concept that doesn't resolve).
    Permanent upstream defect -- waive the spec, don't retry it."""


def _classify_csv(resp, flow_id: str) -> str | None:
    """Map one SDMX-CSV response to text / None (empty window) / a typed error.

    The ORDER of these tests is the whole point, and getting it wrong cost run
    20260715-041757 its 164_305 spec. Istat reports "Unable to generate SQL" --
    its way of saying "this result set is too big for me to build" -- under the
    same error status it uses for a structurally broken dataflow. Classify on
    the status first and an oversized window is indistinguishable from a
    permanent defect: it raises _DeadFlow, which is deliberately NOT in _TOO_BIG,
    so the splitter never sees it, never subdivides, and the spec fails hard with
    a message that reads like an upstream defect and invites a bogus waiver.

    So the BODY is the authority on "too big"; the status only classifies what
    the body leaves unexplained. Shared by the unkeyed and keyed fetchers, which
    previously carried two subtly different copies of this ladder.
    """
    body = resp.text[:1000]
    if resp.status_code == 413 or "Unable to generate SQL" in body:
        raise _OversizedQuery(f"{flow_id}: {resp.text[:400].strip()}")
    # 404/422 are overloaded: an empty time window and a dataflow with no data
    # behind it at all come back the same way, distinguished only by the body.
    if resp.status_code in (404, 422):
        if "NoRecordsFound" in body[:400]:
            return None
        raise _DeadFlow(f"{flow_id}: {resp.text[:400].strip()}")
    resp.raise_for_status()
    return resp.text


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
    if tries > 1:
        # The connect retry buys a second chance at a slow TLS handshake. Once a
        # previous spec has failed to connect and NOTHING has been served this
        # leg, that is a blackhole, and the retry only spends another
        # _CONNECT_TIMEOUT re-confirming it. Probe once and let the leg fail out
        # quickly. The first spec keeps its retry: with no streak yet, a slow
        # handshake is still the likelier story.
        served, streak = _endpoint_state()
        if streak and not served:
            tries = 1
    try:
        for attempt_no in range(1, tries + 1):
            _throttle()
            try:
                resp = _get(
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

    return _classify_csv(resp, flow_id)


def _lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


@lru_cache(maxsize=256)
def _flow_structure(flow_id: str) -> tuple[dict, ...]:
    """Return non-time dimensions with their codelist values for one flow."""
    _throttle()
    df_resp = _get(
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
    dsd_resp = _get(
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
    skip = _SKIP_SPLIT_DIMS.get(flow_id, frozenset())
    candidates = [
        d for d in dims
        if d["codes"] and 1 < len(d["codes"]) <= _MAX_SPLIT_CODES
        and d["id"] not in skip
    ]
    rank = {name: i for i, name in enumerate(_PREFERRED_SPLIT_DIMS)}
    candidates.sort(key=lambda d: (rank.get(d["id"], 99), len(d["codes"])))
    return candidates


def _key_for_assignments(dims: list[dict], assignments: dict[str, str]) -> str:
    parts = ["" for _ in dims]
    for i, dim in enumerate(dims):
        parts[i] = assignments.get(dim["id"], "")
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
                resp = _get(
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
    return _classify_csv(resp, flow_id)


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
        except _TOO_BIG as exc:
            _too_big_backoff(flow_id, exc, f"{lo}..{hi} too large to serve")
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

    def split_compact_dims(
        start: str,
        end: str,
        assignments: dict[str, str] | None = None,
    ):
        """Split an otherwise-too-large time window by a compact DSD dimension.

        This is mainly for annual dataflows where TIME_PERIOD cannot be divided
        further. It also avoids the municipal REF_AREA fan-out unless no compact
        dimensions exist.
        """
        assignments = assignments or {}
        try:
            all_dims = list(_flow_structure(flow_id))
            dims = [d for d in _split_dimensions(flow_id) if d["id"] not in assignments]
        except Exception as exc:
            print(f"[istat] {flow_id}: could not inspect DSD for dimension split: {exc}")
            return False

        for dim in dims:
            seen = 0
            prefix = ",".join(f"{k}={v}" for k, v in assignments.items()) or "all"
            print(
                f"[istat] {flow_id}: splitting {start}..{end} {prefix} by "
                f"{dim['id']} ({len(dim['codes'])} codes)"
            )
            for code in dim["codes"]:
                if budget[0] <= 0:
                    raise RuntimeError(f"{flow_id}: exceeded {_MAX_REQUESTS_PER_FLOW} requests")
                budget[0] -= 1
                next_assignments = {**assignments, dim["id"]: code}
                key = _key_for_assignments(all_dims, next_assignments)
                try:
                    text = _fetch_csv_keyed(flow_id, key, start, end)
                except _TOO_BIG as exc:
                    _too_big_backoff(
                        flow_id, exc,
                        f"{dim['id']}={code} over {start}..{end} too large to serve")
                    yielded = yield from split_compact_dims(start, end, next_assignments)
                    if yielded:
                        seen += 1
                        continue
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
            except _TOO_BIG as exc:
                _too_big_backoff(flow_id, exc, f"{start} too large to serve")
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
    except _TOO_BIG as exc:
        # Enter the split ONE LEVEL DOWN, at decades. split_years(_YEAR_MIN,
        # _YEAR_MAX) would re-request the exact monster we just abandoned --
        # that request is guaranteed to fail, and each such failure extends the
        # wedge, which is how one bad flow used to take the whole leg with it.
        print(f"[istat] {flow_id}: too large to serve whole — splitting by decade")
        _too_big_backoff(flow_id, exc, "full-flow probe abandoned")
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
    except (httpx.ConnectTimeout, httpx.ConnectError) as exc:
        # A connect failure is either OUR wedge draining or Istat blackholing
        # this runner, and only the endpoint-health record can tell them apart.
        # Guessing "wedge" and draining is what turned 20260715-084715 into 3.5h
        # of sleep for nothing, so the drain now has to earn its 6 minutes.
        served, streak = _endpoint_state("connect_failure")
        if not served:
            # Istat has not answered this runner once. There is no abandoned
            # query of ours behind this, so there is nothing to drain.
            raise _EndpointUnreachable(
                f"{flow_id}: no TCP/TLS to {BASE} and Istat has not served this "
                f"runner once this leg ({streak} consecutive connect failures) "
                f"— the endpoint is blackholing this IP, not wedged by us. "
                f"Source-wide and external: do NOT waive this flow. Re-dispatch "
                f"later; a fresh runner draws a different egress IP."
            ) from exc
        if streak > _MAX_DRAINED_CONNECT_FAILURES:
            # We were served earlier, so a wedge was plausible -- but a drain
            # that has already failed this many times running has disproved
            # itself. Keep failing fast (and keep probing: the next spec still
            # tries, so a lifting outage is picked up automatically).
            raise _EndpointUnreachable(
                f"{flow_id}: {streak} consecutive specs could not connect to "
                f"{BASE} despite draining — this outlasts any wedge drain "
                f"({_WEDGE_RECOVERY_S:.0f}s). Failing fast instead of sleeping "
                f"the leg away; do NOT waive this flow."
            ) from exc
        # Plausibly our own wedge, and the drain has not been disproved yet.
        # Unbudgeted on purpose: it is for the NEXT spec's benefit, not this
        # flow's, so it must happen even once this flow is over budget.
        _drain_wedge(flow_id, "Istat refused the connection (wedged)")
        raise
    if n[0] == 0:
        raise AssertionError(f"{asset}: dataflow {flow_id} returned 0 observations")


from constants import ENTITY_IDS

ENTITY_BY_NODE = {f"istat-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS}

# Heavy flows last -- see _HEAVY_FLOWS. The orchestrator breaks ties between
# ready specs by declaration index, so this list's order IS the leg's order.
DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"istat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in sorted(ENTITY_IDS, key=lambda e: (e in _HEAVY_FLOWS, e))
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
