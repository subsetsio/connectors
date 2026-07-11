"""NHTSA download nodes — the raw fetches for all six accepted subsets.

Three families of source, one fetch fn each family:

* ODI flat files (recalls / complaints / investigations) — tab-delimited text,
  NO header row, columns positional per the published field dictionaries. Full
  corpus republished daily; each fetch is a stateless full re-pull streamed to
  all-string parquet (the SQL/model stage does the typing). Recalls is split
  into two era zips (PRE_2010 + POST_2010) concatenated into one raw asset.
* NCAP 5-Star Safety Ratings (api.nhtsa.gov/SafetyRatings) — no bulk endpoint
  and no delta filter, so a full re-crawl each run: traverse
  modelyear -> make -> model to collect VehicleIds, then fetch each rating
  record. Written as NDJSON (heterogeneous record).
* vPIC reference tables (vpic.nhtsa.dot.gov) — GetAllMakes returns the whole
  makes table in one request (flat -> parquet); GetAllManufacturers is paged
  100/page with a nested VehicleTypes list per row (-> NDJSON), iterated until
  an empty page.

No incremental filter exists on any mechanism, so every node is a full
snapshot overwrite.
"""

import io
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    get,
    configure_http,
    is_transient,
    transient_retry,
    raw_parquet_writer,
    save_raw_parquet,
    save_raw_ndjson,
)


# --------------------------------------------------------------------------- #
# HTTP retry/transport
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry(min_wait=2, max_wait=60)
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 90.0))
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------------- #
# ODI flat files (recalls / complaints / investigations)
# --------------------------------------------------------------------------- #
RECALLS_COLS = [
    "RECORD_ID", "CAMPNO", "MAKETXT", "MODELTXT", "YEARTXT", "MFGCAMPNO",
    "COMPNAME", "MFGNAME", "BGMAN", "ENDMAN", "RCLTYPECD", "POTAFF", "ODATE",
    "INFLUENCED_BY", "MFGTXT", "RCDATE", "DATEA", "RPNO", "FMVSS",
    "DESC_DEFECT", "CONEQUENCE_DEFECT", "CORRECTIVE_ACTION", "NOTES",
    "RCL_CMPT_ID", "MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO",
    "DO_NOT_DRIVE", "PARK_OUTSIDE",
]

COMPLAINTS_COLS = [
    "CMPLID", "ODINO", "MFR_NAME", "MAKETXT", "MODELTXT", "YEARTXT", "CRASH",
    "FAILDATE", "FIRE", "INJURED", "DEATHS", "COMPDESC", "CITY", "STATE",
    "VIN", "DATEA", "LDATE", "MILES", "OCCURENCES", "CDESCR", "CMPL_TYPE",
    "POLICE_RPT_YN", "PURCH_DT", "ORIG_OWNER_YN", "ANTI_BRAKES_YN",
    "CRUISE_CONT_YN", "NUM_CYLS", "DRIVE_TRAIN", "FUEL_SYS", "FUEL_TYPE",
    "TRANS_TYPE", "VEH_SPEED", "DOT", "TIRE_SIZE", "LOC_OF_TIRE",
    "TIRE_FAIL_TYPE", "ORIG_EQUIP_YN", "MANUF_DT", "SEAT_TYPE",
    "RESTRAINT_TYPE", "DEALER_NAME", "DEALER_TEL", "DEALER_CITY",
    "DEALER_STATE", "DEALER_ZIP", "PROD_TYPE", "REPAIRED_YN", "MEDICAL_ATTN",
    "VEHICLES_TOWED_YN", "STATE_OF_INCIDENT", "VEHICLE_OPERATOR",
]

INVESTIGATIONS_COLS = [
    "NHTSA_ACTION_NUMBER", "MAKE", "MODEL", "YEAR", "COMPNAME", "MFR_NAME",
    "ODATE", "CDATE", "CAMPNO", "SUBJECT", "SUMMARY",
]

_FFDD = "https://static.nhtsa.gov/odi/ffdd"
FLAT_SOURCES = {
    "nhtsa-recalls": (
        RECALLS_COLS,
        [f"{_FFDD}/rcl/FLAT_RCL_PRE_2010.zip", f"{_FFDD}/rcl/FLAT_RCL_POST_2010.zip"],
    ),
    "nhtsa-complaints": (
        COMPLAINTS_COLS,
        [f"{_FFDD}/cmpl/FLAT_CMPL.zip"],
    ),
    "nhtsa-investigations": (
        INVESTIGATIONS_COLS,
        [f"{_FFDD}/inv/FLAT_INV.zip"],
    ),
}

_BATCH_ROWS = 25_000


def _iter_lines(zip_bytes: bytes):
    """Yield each record as raw bytes (split strictly on b'\\n').

    The ODI flat files use one physical line per record with no embedded
    newlines (verified by probing: every line splits to the exact field
    count), so splitting only on \\n is correct and keeps memory bounded by
    streaming the single zip member rather than materialising the (up to
    ~1.5GB) decompressed text.
    """
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    name = zf.namelist()[0]
    with zf.open(name) as fh:
        buf = b""
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            buf += chunk
            parts = buf.split(b"\n")
            buf = parts.pop()
            for p in parts:
                yield p
        if buf:
            yield buf


def fetch_flat_file(node_id: str) -> None:
    cols, urls = FLAT_SOURCES[node_id]
    n = len(cols)
    schema = pa.schema([(c, pa.string()) for c in cols])

    columns = {c: [] for c in cols}
    size = total = bad = 0

    with raw_parquet_writer(node_id, schema) as writer:
        for url in urls:
            zip_bytes = _get_bytes(url)
            for line in _iter_lines(zip_bytes):
                if line.endswith(b"\r"):
                    line = line[:-1]
                if not line:
                    continue
                cells = line.decode("latin-1").split("\t")
                total += 1
                if len(cells) != n:
                    bad += 1
                for i, c in enumerate(cols):
                    columns[c].append(cells[i] if i < len(cells) else None)
                size += 1
                if size >= _BATCH_ROWS:
                    writer.write_table(pa.table(columns, schema=schema))
                    columns = {c: [] for c in cols}
                    size = 0
        if size:
            writer.write_table(pa.table(columns, schema=schema))

    if total == 0:
        raise RuntimeError(f"{node_id}: parsed 0 records from {urls}")
    if bad / total > 0.05:
        raise RuntimeError(
            f"{node_id}: {bad}/{total} lines had != {n} fields "
            f"(flat-file layout may have changed)"
        )
    print(f"  {node_id}: parsed {total} records ({bad} field-count anomalies)")


# --------------------------------------------------------------------------- #
# NCAP Safety Ratings (api.nhtsa.gov/SafetyRatings)
# --------------------------------------------------------------------------- #
def _is_transient_or_blocked(exc: BaseException) -> bool:
    """As is_transient, but also retries 403 — api.nhtsa.gov is Akamai-fronted
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


_SR_BASE = "https://api.nhtsa.gov/SafetyRatings"
# Low concurrency + a shared rate cap: an 8-worker burst in an early run tripped
# Akamai's edge throttle (fast 403s). Keep well under it.
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
# vPIC reference tables (vpic.nhtsa.dot.gov)
# --------------------------------------------------------------------------- #
_VPIC = "https://vpic.nhtsa.dot.gov/api/vehicles"

_MAKES_SCHEMA = pa.schema([
    ("Make_ID", pa.int64()),
    ("Make_Name", pa.string()),
])


def fetch_vpic_makes(node_id: str) -> None:
    """GetAllMakes returns every make (~12k) in one JSON response — flat rows of
    Make_ID + Make_Name. Full snapshot -> parquet."""
    data = _get_json(f"{_VPIC}/getallmakes?format=json")
    rows = data.get("Results") or []
    if not rows:
        raise RuntimeError("vpic_makes: GetAllMakes returned 0 rows")
    table = pa.Table.from_pylist(
        [{"Make_ID": r.get("Make_ID"), "Make_Name": r.get("Make_Name")} for r in rows],
        schema=_MAKES_SCHEMA,
    )
    print(f"  vpic_makes: {table.num_rows} makes")
    save_raw_parquet(table, node_id)


# Safety ceiling: GetAllManufacturers pages ~100/row; the live universe is a few
# hundred pages. A cap far above that catches runaway pagination (a server that
# never returns an empty page) and RAISES rather than looping forever.
_MFR_MAX_PAGES = 2000


def fetch_vpic_manufacturers(node_id: str) -> None:
    """GetAllManufacturers is paged 100/page and carries a nested VehicleTypes
    list per row, so it's written as NDJSON. Iterate until a page returns no
    results (verified terminus: pages past the universe return an empty
    Results array)."""
    rows = []
    page = 1
    while True:
        data = _get_json(f"{_VPIC}/getallmanufacturers?format=json&page={page}")
        page_rows = data.get("Results") or []
        if not page_rows:
            break
        rows.extend(page_rows)
        page += 1
        if page > _MFR_MAX_PAGES:
            raise RuntimeError(
                f"vpic_manufacturers: exceeded {_MFR_MAX_PAGES} pages without an "
                f"empty page — pagination may be broken or the universe grew hugely"
            )
    if not rows:
        raise RuntimeError("vpic_manufacturers: GetAllManufacturers returned 0 rows")
    print(f"  vpic_manufacturers: {len(rows)} manufacturers over {page - 1} pages")
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# Specs — one per accepted collect entity (the entity union)
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="nhtsa-recalls", fn=fetch_flat_file, kind="download"),
    NodeSpec(id="nhtsa-complaints", fn=fetch_flat_file, kind="download"),
    NodeSpec(id="nhtsa-investigations", fn=fetch_flat_file, kind="download"),
    NodeSpec(id="nhtsa-safety-ratings", fn=fetch_safety_ratings, kind="download"),
    NodeSpec(id="nhtsa-vpic-makes", fn=fetch_vpic_makes, kind="download"),
    NodeSpec(id="nhtsa-vpic-manufacturers", fn=fetch_vpic_manufacturers, kind="download"),
]
