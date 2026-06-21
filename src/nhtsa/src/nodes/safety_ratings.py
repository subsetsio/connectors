"""NHTSA NCAP Safety Ratings subset (api.nhtsa.gov/SafetyRatings).

The NCAP 5-Star ratings API has no bulk endpoint and no delta filter, so it is
a full re-crawl each run: traverse modelyear -> make -> model to collect
VehicleIds, then fetch each VehicleId's rating record. The make-level traversal
and the per-VehicleId detail fetches are parallelised across a small thread pool
(the shared httpx.Client is thread-safe). Bounded corpus (~tens of thousands of
rated variants).
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    is_transient,
    save_raw_ndjson,
)


# --------------------------------------------------------------------------- #
# HTTP retry/transport
# --------------------------------------------------------------------------- #
def _is_transient_or_blocked(exc: BaseException) -> bool:
    """As _is_transient, but also retries 403 — api.nhtsa.gov is Akamai-fronted
    and answers a concurrency/rate burst from datacenter IPs with a fast 403
    rather than a 429. Backing off and retrying recovers from the throttle; a
    genuinely persistent 403 exhausts retries and surfaces loudly (the node
    fails) instead of being silently swallowed into an empty dataset."""
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 403
    return False


class _RateLimiter:
    """Thread-safe min-interval limiter shared across the SafetyRatings pool."""

    def __init__(self, rate_per_sec: float):
        self._interval = 1.0 / rate_per_sec
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            start = max(now, self._next)
            self._next = start + self._interval
            delay = start - now
        if delay > 0:
            time.sleep(delay)


# --------------------------------------------------------------------------- #
# NCAP Safety Ratings (api.nhtsa.gov/SafetyRatings)
# --------------------------------------------------------------------------- #
_SR_BASE = "https://api.nhtsa.gov/SafetyRatings"
# Low concurrency + a shared rate cap: the 8-worker burst in the first run
# tripped Akamai's edge throttle (fast 403s). Keep well under it.
_SR_WORKERS = 3
_SR_RATE = _RateLimiter(rate_per_sec=6.0)

# A realistic browser identity raises Akamai's trust score for the datacenter
# IP; api.nhtsa.gov returns JSON regardless of Accept.
_SR_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


@retry(
    retry=retry_if_exception(_is_transient_or_blocked),
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=3, max=45),
    reraise=True,
)
def _sr_get(url: str):
    _SR_RATE.wait()
    resp = get(url, timeout=(10.0, 90.0))
    resp.raise_for_status()
    return resp.json()


# Permanent client errors that mean "this node is unaddressable / empty" and
# should be skipped, not fail the whole crawl. 400 shows up on model names that
# contain a slash (e.g. "RANGE ROVER LWB PHEV/MHEV") — the encoded %2F is
# rejected by the API and there is no alternate addressing, so we drop those
# few models rather than the entire dataset.
_SR_SKIP_CODES = {400, 404, 410, 422}


def _sr_results(url: str) -> list:
    """GET a SafetyRatings node. A skippable 4xx (bad/missing node) yields []; a
    persistent 403 (Akamai block surviving retries) propagates and fails the
    node loudly rather than silently yielding an empty dataset."""
    try:
        return _sr_get(url).get("Results", []) or []
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in _SR_SKIP_CODES:
            print(f"  safety_ratings: {exc.response.status_code} on {url} - skipping")
            return []
        raise


def _vehicle_ids_for_make(model_year, make: str) -> list:
    base = f"{_SR_BASE}/modelyear/{model_year}/make/{quote(make, safe='')}"
    ids = []
    for md in _sr_results(base):
        model = md.get("Model")
        if not model:
            continue
        variants = _sr_results(f"{base}/model/{quote(model, safe='')}")
        ids.extend(v["VehicleId"] for v in variants if v.get("VehicleId"))
    return ids


def fetch_safety_ratings(node_id: str) -> None:
    # Runs in its own spawn subprocess, so this only re-skins this node's client.
    configure_http(headers=_SR_HEADERS)
    years = [y["ModelYear"] for y in _sr_results(_SR_BASE) if y.get("ModelYear")]
    if not years:
        raise RuntimeError("safety_ratings: no model years returned")

    # (model_year, make) work units — listing makes is cheap and sequential.
    make_tasks = []
    for my in years:
        for mk in _sr_results(f"{_SR_BASE}/modelyear/{my}"):
            if mk.get("Make"):
                make_tasks.append((my, mk["Make"]))

    vehicle_ids = set()
    with ThreadPoolExecutor(max_workers=_SR_WORKERS) as pool:
        futs = [pool.submit(_vehicle_ids_for_make, my, mk) for my, mk in make_tasks]
        for fut in as_completed(futs):
            vehicle_ids.update(fut.result())

    if not vehicle_ids:
        raise RuntimeError("safety_ratings: traversal produced 0 VehicleIds")

    rows = []
    with ThreadPoolExecutor(max_workers=_SR_WORKERS) as pool:
        futs = {
            pool.submit(_sr_results, f"{_SR_BASE}/VehicleId/{vid}"): vid
            for vid in vehicle_ids
        }
        for fut in as_completed(futs):
            res = fut.result()
            if res:
                rows.append(res[0])

    if not rows:
        raise RuntimeError("safety_ratings: fetched 0 rating records")
    print(f"  safety_ratings: {len(vehicle_ids)} VehicleIds -> {len(rows)} records")
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="nhtsa-safety-ratings", fn=fetch_safety_ratings, kind="download"),
]


_SAFETY_RATINGS_SQL = '''
    SELECT
        TRY_CAST(VehicleId AS BIGINT)                  AS vehicle_id,
        TRY_CAST(ModelYear AS INTEGER)                 AS model_year,
        NULLIF(TRIM(Make), '')                         AS make,
        NULLIF(TRIM(Model), '')                        AS model,
        NULLIF(TRIM(VehicleDescription), '')           AS vehicle_description,
        NULLIF(TRIM(OverallRating), '')                AS overall_rating,
        NULLIF(TRIM(OverallFrontCrashRating), '')      AS overall_front_crash_rating,
        NULLIF(TRIM(OverallSideCrashRating), '')       AS overall_side_crash_rating,
        NULLIF(TRIM(RolloverRating), '')               AS rollover_rating,
        TRY_CAST(RolloverPossibility AS DOUBLE)        AS rollover_possibility,
        NULLIF(TRIM(FrontCrashDriversideRating), '')   AS front_crash_driver_rating,
        NULLIF(TRIM(FrontCrashPassengersideRating), '') AS front_crash_passenger_rating,
        NULLIF(TRIM(SideCrashDriversideRating), '')    AS side_crash_driver_rating,
        NULLIF(TRIM(SideCrashPassengersideRating), '') AS side_crash_passenger_rating,
        NULLIF(TRIM(SidePoleCrashRating), '')          AS side_pole_crash_rating,
        NULLIF(TRIM(NHTSAElectronicStabilityControl), '') AS electronic_stability_control,
        NULLIF(TRIM(NHTSAForwardCollisionWarning), '') AS forward_collision_warning,
        NULLIF(TRIM(NHTSALaneDepartureWarning), '')    AS lane_departure_warning,
        TRY_CAST(RecallsCount AS INTEGER)              AS recalls_count,
        TRY_CAST(ComplaintsCount AS INTEGER)           AS complaints_count,
        TRY_CAST(InvestigationCount AS INTEGER)        AS investigations_count
    FROM "nhtsa-safety-ratings"
    WHERE VehicleId IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="nhtsa-safety-ratings-transform", deps=["nhtsa-safety-ratings"], sql=_SAFETY_RATINGS_SQL),
]
