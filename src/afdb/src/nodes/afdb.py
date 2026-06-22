"""AfDB (African Development Bank) connector — Knoema "Africa Information
Highway" platform API (https://dataportal.opendataforafrica.org/api/1.0).

One download node per rank-active Knoema dataset (the entity union); each
publishes one long-format Delta table (date, value, unit, frequency, + one
column per dataset dimension).

Fetch shape: STATELESS FULL RE-PULL. Each dataset is at most a few million
points; we re-fetch the whole dataset every run and overwrite. No watermark —
revisions are picked up for free. The maintain step (authored later) decides
whether a given node runs on a refresh.

Per dataset:
  1. GET /meta/dataset/{id}                 -> dimensions
  2. GET /meta/dataset/{id}/dimension/{d}   -> member keys (hasData only)
  3. detect NATIVE frequency (see below)
  4. POST /data/raw paged on continuationToken at the native frequency
     -> rows, each a time series with a values[] array -> expand to (date,value)

NATIVE FREQUENCY: Knoema resamples on request. Requesting a frequency FINER
than the dataset's native grid FORWARD-FILLS (synthetic duplicate values);
requesting COARSER aggregates. So we must fetch each dataset at its own native
frequency. We detect it by walking A->Q->M->W->D on a small member sample and
taking the finest frequency at which the count of DISTINCT values is still
strictly rising — once it plateaus, the source is being upsampled. (borikzb
plateaus at A; lgevikf at M; gthfmjd at D.)

CLOUDFLARE: the whole site is behind a Cloudflare managed challenge. Plain
httpx/requests/urllib (incl. subsets_utils.get) get HTTP 403 ("Just a
moment..."). Python `cloudscraper` solves the JS challenge and returns 200
JSON — verified. So HTTP here goes through a cloudscraper session rather than
subsets_utils.get; everything else (retry policy, timeouts) follows the house
style. A 403 is treated as transient (stale challenge) and triggers a fresh
solve on retry.
"""

import json
from urllib.parse import quote

import cloudscraper
import pandas as pd
import requests
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer
from constants import ENTITY_IDS

SLUG = "afdb"
BASE = "https://dataportal.opendataforafrica.org/api/1.0"

# Wide time window; the API clips to each series' available periods.
TIME_RANGE = "1900-2027"
# Frequency ladder, coarse -> fine, for native-frequency detection.
FREQ_LADDER = ["A", "Q", "M", "W", "D"]
# Map a Knoema frequency code to a pandas date-range step. Calendar offsets
# (YS/QS/MS) anchor to period starts (which the API's startDate already is);
# W/D use fixed timedeltas so they align to the series start exactly.
PANDAS_FREQ = {"A": "YS", "S": "6MS", "H": "6MS", "Q": "QS", "M": "MS", "W": "7D", "D": "D"}
SAMPLE_MEMBERS = 8       # members per dimension used for frequency detection
MAX_PAGES = 100_000      # safety ceiling -> raise (never silently truncate)

_scraper = None


def _client():
    global _scraper
    if _scraper is None:
        _scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "darwin", "mobile": False}
        )
    return _scraper


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
        return True
    if isinstance(exc, requests.exceptions.HTTPError) and exc.response is not None:
        sc = exc.response.status_code
        # 403 == Cloudflare challenge bounce; retry with a fresh solve.
        return sc in (403, 429) or 500 <= sc < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    wait=wait_exponential(multiplier=2, max=120),
    stop=stop_after_attempt(6),
    reraise=True,
)
def _get(path: str):
    try:
        resp = _client().get(BASE + path, timeout=(10.0, 120.0))
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            global _scraper
            _scraper = None  # force a fresh challenge solve on the next attempt
        raise


@retry(
    retry=retry_if_exception(_is_transient),
    wait=wait_exponential(multiplier=2, max=120),
    stop=stop_after_attempt(6),
    reraise=True,
)
def _post(path: str, payload: dict):
    try:
        resp = _client().post(BASE + path, json=payload, timeout=(10.0, 180.0))
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            global _scraper
            _scraper = None
        raise


def _dimension_members(dataset_id: str, dim_id: str) -> list[dict]:
    data = _get(f"/meta/dataset/{dataset_id}/dimension/{dim_id}")
    items = data.get("items") if isinstance(data, dict) else data
    return [m for m in (items or []) if m.get("hasData")]


def _pivot_request(dataset_id, dims, keys_by_dim, freq):
    stub = [{"DimensionId": dims[0]["id"], "Members": keys_by_dim[dims[0]["id"]]}]
    header = [
        {"DimensionId": d["id"], "Members": keys_by_dim[d["id"]]} for d in dims[1:]
    ]
    header.append({"DimensionId": "Time", "Members": [TIME_RANGE]})
    return {
        "Dataset": dataset_id,
        "Stub": stub,
        "Header": header,
        "Filter": [],
        "Frequencies": [freq],
    }


def _detect_frequency(dataset_id, dims, members_by_dim) -> str:
    """Finest frequency whose distinct-value count is still strictly rising."""
    sample = {
        d["id"]: [m["key"] for m in members_by_dim[d["id"]][:SAMPLE_MEMBERS]]
        for d in dims
    }
    native = FREQ_LADDER[0]
    prev = -1
    for freq in FREQ_LADDER:
        req = _pivot_request(dataset_id, dims, sample, freq)
        rows = _post("/data/raw", req).get("data") or []
        best = 0
        for r in rows:
            vals = [round(v, 8) for v in (r.get("values") or []) if v is not None]
            best = max(best, len(set(vals)))
        if best > prev:
            native, prev = freq, best
        else:
            break  # plateaued -> the source is being upsampled; stop here
    return native


def _iter_rows(dataset_id, dims, keys_by_dim, freq):
    """Yield raw pivot rows, paging on continuationToken.

    The first page is a POST carrying the pivot request; each subsequent page is
    a GET on /data/raw?continuationToken=<token>. (Re-POSTing the pivot body with
    the token added is silently ignored by the API — it just re-serves page 1
    forever, so any dataset exceeding the 1000-series page would loop endlessly.
    The GET-with-token form is the only one the server actually honours; it
    returns a falsy token on the final page so paging terminates.)"""
    req = _pivot_request(dataset_id, dims, keys_by_dim, freq)
    resp = _post("/data/raw", req)
    pages = 0
    while True:
        for row in resp.get("data") or []:
            yield row
        token = resp.get("continuationToken")
        pages += 1
        if not token:
            break
        if pages >= MAX_PAGES:
            raise RuntimeError(f"{dataset_id}: exceeded MAX_PAGES={MAX_PAGES} (source grew?)")
        resp = _get(f"/data/raw?continuationToken={quote(token, safe='')}")


def _expand(row, dims):
    """Expand one time-series row into long-format records (one per period)."""
    base = {}
    for d in dims:
        slug = d["id"].replace("-", "_")
        member = row.get(d["id"]) or {}
        base[slug] = member.get("name")
        base[slug + "_code"] = member.get("id")
    base["unit"] = row.get("unit")
    freq = row.get("frequency") or "A"
    base["frequency"] = freq
    start = (row.get("startDate") or "")[:10]
    values = row.get("values") or []
    if not start or not values:
        return
    dates = pd.date_range(start=start, periods=len(values), freq=PANDAS_FREQ.get(freq, "YS"))
    for dt, v in zip(dates, values):
        if v is None:
            continue
        rec = dict(base)
        rec["date"] = dt.strftime("%Y-%m-%d")
        rec["value"] = v
        yield rec


def fetch_one(node_id: str) -> None:
    asset = node_id                              # the spec id IS the asset name
    dataset_id = node_id[len(SLUG) + 1:]         # strip "afdb-"
    meta = _get(f"/meta/dataset/{dataset_id}")
    dims = meta.get("dimensions") or []
    if not dims:
        raise RuntimeError(f"{dataset_id}: dataset has no dimensions")

    members_by_dim = {d["id"]: _dimension_members(dataset_id, d["id"]) for d in dims}
    keys_by_dim = {dim: [m["key"] for m in mems] for dim, mems in members_by_dim.items()}
    for dim, keys in keys_by_dim.items():
        if not keys:
            raise RuntimeError(f"{dataset_id}: dimension {dim} has no members with data")

    freq = _detect_frequency(dataset_id, dims, members_by_dim)

    nrows = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in _iter_rows(dataset_id, dims, keys_by_dim, freq):
            for rec in _expand(row, dims):
                f.write(json.dumps(rec) + "\n")
                nrows += 1
    if nrows == 0:
        raise RuntimeError(f"{dataset_id}: produced 0 observations at frequency {freq}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(asset: str) -> str:
    # Thin parse-and-type pass: cast date/value, keep unit/frequency/dimension
    # columns as-is, drop the (already rare) null values. One published table
    # per dataset; columns differ across datasets, hence SELECT * EXCLUDE.
    return f'''
        SELECT
            CAST(date AS DATE)    AS date,
            CAST(value AS DOUBLE) AS value,
            * EXCLUDE (date, value)
        FROM "{asset}"
        WHERE value IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_transform_sql(s.id))
    for s in DOWNLOAD_SPECS
]
