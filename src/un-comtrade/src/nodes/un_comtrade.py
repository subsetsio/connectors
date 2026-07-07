"""UN Comtrade bilateral merchandise-trade flows (annual, HS, TOTAL commodity).

One published subset: `un-comtrade-values` — long-format annual bilateral trade
between every reporting economy and all of its partners (imports and exports),
at the TOTAL commodity aggregation, HS classification. Reporter and partner are
column values, not separate datasets, so this is a single ~3M-row table.

Access: the authenticated final-data endpoint
https://comtradeapi.un.org/data/v1/get/C/A/HS. The keyless preview endpoint was
the original research choice, but live runs hit a 403 quota after only a small
slice of the corpus. The final-data endpoint requires COMTRADE_API_KEY and
allows up to 250k records per response, so we can fetch one full all-reporter
TOTAL-commodity year per call.

## Fetch shape — stateless full re-pull, one raw FRAGMENT per year

There is NO incremental cursor on this API (getDA carries no since/modifiedAfter
filter — verified), so per the download rubric this is a **stateless full
re-pull**: every fresh run re-crawls all reporters and all their years. We do
NOT keep a persistent per-reporter "already fetched" signature — that pattern is
a trap here, because raw is written into a *run-scoped* prefix
(`runs/<run_id>/raw/`) while such state would persist across runs, so a re-run
would skip "done" reporters and leave the new run's raw holed (the transform
then materializes on a fraction of the matrix). Correctness first: each run's
raw is complete and self-contained.

The full crawl is ~35 calls (one per annual period) with a key. To survive a
supervisor interrupt we write one raw fragment per year (`fragment=<refYear>` of
the single `un-comtrade-values` asset) and RESUME WITHIN THE RUN from the raw
manifest: a year already committed under the current RUN_ID is skipped. This is
run-scoped resume, not cross-run state — a brand-new run_id starts a clean full
crawl. The transform's dep view glob-unions every `un-comtrade-values-*`
fragment automatically.

Net weight is omitted — it is 0/missing for the TOTAL aggregation.
"""
import os

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    save_raw_parquet,
)

REPORTERS_URL = "https://comtradeapi.un.org/files/v1/app/reference/Reporters.json"
DA_URL = "https://comtradeapi.un.org/public/v1/getDA/C/A/HS"
DATA_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"

# Safety floor: the reference file lists ~219 active reporters. A far smaller
# count means the reference fetch was truncated/changed — fail loudly rather
# than crawl a degraded subset.
MIN_REPORTERS = 150

SCHEMA = pa.schema([
    ("refYear", pa.int32()),
    ("reporterCode", pa.int32()),
    ("reporterISO", pa.string()),
    ("reporterDesc", pa.string()),
    ("partnerCode", pa.int32()),
    ("partnerISO", pa.string()),
    ("partnerDesc", pa.string()),
    ("flowCode", pa.string()),
    ("flowDesc", pa.string()),
    ("cmdCode", pa.string()),
    ("primaryValue", pa.float64()),
    ("isReported", pa.bool_()),
])


# Base pacing so `get`'s built-in 429 backoff rarely has to fire. The final-data
# endpoint returns much larger pages than preview, so this is intentionally
# conservative. `subsets_utils.get` already retries transient errors + 429/5xx
# with exponential backoff and honors Retry-After.
@sleep_and_retry
@limits(calls=20, period=60)
def _throttled_get(url: str, params: dict | None) -> httpx.Response:
    return get(url, params=params, timeout=(10.0, 120.0))


def _api_get(url: str, params: dict | None = None):
    resp = _throttled_get(url, params)
    resp.raise_for_status()
    return resp.json()


def _subscription_key() -> str:
    key = os.environ.get("COMTRADE_API_KEY")
    if not key:
        raise RuntimeError(
            "UN Comtrade final-data extraction requires COMTRADE_API_KEY. "
            "The keyless preview API is quota-capped before the full corpus can "
            "be fetched."
        )
    return key


def _active_reporters() -> list[dict]:
    """Active, non-group reporting economies from the keyless reference file."""
    payload = _api_get(REPORTERS_URL)
    out = []
    for r in payload.get("results", []):
        if r.get("entryExpiredDate"):
            continue
        if r.get("isGroup"):
            continue
        code = r.get("reporterCode")
        if code is None:
            continue
        out.append({"code": int(code), "name": r.get("reporterDesc")})
    if len(out) < MIN_REPORTERS:
        raise AssertionError(
            f"only {len(out)} active reporters from {REPORTERS_URL}; "
            f"expected >= {MIN_REPORTERS} — reference fetch likely degraded"
        )
    return out


def _available_years() -> list[int]:
    """Annual HS periods from keyless getDA."""
    payload = _api_get(DA_URL)
    return sorted({
        int(row["period"])
        for row in (payload.get("data") or [])
        if row.get("period") is not None
    })


def _fetch_year(year: int) -> list[dict]:
    """All-reporter/all-partner imports+exports for one year."""
    params = {
        "period": str(year),
        "flowCode": "M,X",
        "cmdCode": "TOTAL",
        "includeDesc": "true",
        "breakdownMode": "classic",
        "maxRecords": "250000",
        "subscription-key": _subscription_key(),
    }
    try:
        payload = _api_get(DATA_URL, params)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return []
        raise
    return payload.get("data") or []


def _clean(rec: dict) -> dict:
    def _i(v):
        return int(v) if v is not None else None

    def _f(v):
        return float(v) if v is not None else None

    def _s(v):
        return str(v) if v is not None else None

    return {
        "refYear": _i(rec.get("refYear")),
        "reporterCode": _i(rec.get("reporterCode")),
        "reporterISO": _s(rec.get("reporterISO")),
        "reporterDesc": _s(rec.get("reporterDesc")),
        "partnerCode": _i(rec.get("partnerCode")),
        "partnerISO": _s(rec.get("partnerISO")),
        "partnerDesc": _s(rec.get("partnerDesc")),
        "flowCode": _s(rec.get("flowCode")),
        "flowDesc": _s(rec.get("flowDesc")),
        "cmdCode": _s(rec.get("cmdCode")),
        "primaryValue": _f(rec.get("primaryValue")),
        "isReported": bool(rec.get("isReported")),
    }


def fetch_values(node_id: str) -> None:
    """Crawl the full bilateral matrix, one raw fragment per year.

    Stateless full re-pull with run-scoped resume: a year whose fragment is
    already committed under THIS run_id is skipped, so a supervisor-interrupted
    run resumes without re-fetching completed years and without persisting a
    cross-run watermark that would hole a fresh run's raw.
    """
    _subscription_key()
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag for frag, meta in list_raw_fragments(node_id).items()
        if meta.get("run_id") == run_id
    }

    reporters = _active_reporters()
    years = _available_years()
    print(f"UN Comtrade: {len(reporters)} active reporters, {len(years)} years "
          f"({len(done)} years already done this run)")

    for i, year in enumerate(years, 1):
        frag = str(year)
        if frag in done:
            continue  # committed earlier in this same run - resume past it

        rows = [_clean(r) for r in _fetch_year(year)]

        if rows:
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            save_raw_parquet(table, node_id, fragment=frag)
            print(f"  [{i}/{len(years)}] {year}: {len(rows):,} rows")
        else:
            # No data for this year. Write nothing
            # — an empty fragment would fail the nonempty-batch health check.
            print(f"  [{i}/{len(years)}] {year}: no data")


DOWNLOAD_SPECS = [
    NodeSpec(id="un-comtrade-values", fn=fetch_values, kind="download"),
]
