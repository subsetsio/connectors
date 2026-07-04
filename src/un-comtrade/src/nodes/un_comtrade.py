"""UN Comtrade bilateral merchandise-trade flows (annual, HS, TOTAL commodity).

One published subset: `un-comtrade-values` — long-format annual bilateral trade
between every reporting economy and all of its partners (imports and exports),
at the TOTAL commodity aggregation, HS classification. Reporter and partner are
column values, not separate datasets, so this is a single ~3M-row table.

Access (see research `rest_preview`): the keyless public preview endpoint
https://comtradeapi.un.org/public/v1/preview/C/A/HS. No subscription key is
needed or available. The endpoint hard-caps every response at 500 records, so
the only viable partition is one call per (reporter, year): a single
(reporter, year) query with flowCode=M,X & cmdCode=TOTAL over all partners
returns ~200-450 rows — under the cap. The keyless getDA data-availability
endpoint (same host) tells us exactly which years each reporter has data for,
so we never waste calls on empty years and the period set is discovered from
the source (never hardcoded).

## Fetch shape — stateless full re-pull, one raw FRAGMENT per reporter

There is NO incremental cursor on this API (getDA carries no since/modifiedAfter
filter — verified), so per the download rubric this is a **stateless full
re-pull**: every fresh run re-crawls all reporters and all their years. We do
NOT keep a persistent per-reporter "already fetched" signature — that pattern is
a trap here, because raw is written into a *run-scoped* prefix
(`runs/<run_id>/raw/`) while such state would persist across runs, so a re-run
would skip "done" reporters and leave the new run's raw holed (the transform
then materializes on a fraction of the matrix). Correctness first: each run's
raw is complete and self-contained.

The full crawl is large (~219 reporters x ~25-35 years ~= 7k calls) and the
public endpoint's true sustainable rate is ~0.6 req/sec (measured: >~0.8/sec
draws sustained 429s), so a full crawl is ~3-4h — near, but under, one CI
window. To survive a supervisor interrupt we write one raw fragment per reporter
(`fragment=<reporterCode>` of the single `un-comtrade-values` asset) and RESUME
WITHIN THE RUN from the raw manifest: a reporter already committed under the
current RUN_ID is skipped. This is run-scoped resume (the firehose-continuation
pattern), not cross-run state — a brand-new run_id starts a clean full crawl,
while the supervisor's continuation of the same run_id picks up where it left
off. The transform's dep view glob-unions every `un-comtrade-values-*` fragment
automatically.

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
DATA_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

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


# Base pacing so `get`'s built-in 429 backoff rarely has to fire: the public
# endpoint 429s sustained bursts above ~0.7 req/sec (measured), so we pace at
# ~0.55 req/sec (11 calls / 20s). `subsets_utils.get` ALREADY retries transient
# errors + 429/5xx with exponential backoff and honours Retry-After — we do NOT
# stack a second retry layer on top (that multiplies the waits). ratelimit is
# per-process, which is fine: this connector's single download spec owns the
# whole rate budget in its own spawn subprocess.
@sleep_and_retry
@limits(calls=11, period=20)
def _throttled_get(url: str, params: dict | None) -> httpx.Response:
    return get(url, params=params, timeout=(10.0, 120.0))


def _api_get(url: str, params: dict | None = None):
    resp = _throttled_get(url, params)
    resp.raise_for_status()
    return resp.json()


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


def _available_years(reporter_code: int) -> list[int]:
    """Years for which this reporter has annual HS data, from keyless getDA.
    [] on 404 (reporter absent from the availability index)."""
    try:
        payload = _api_get(DA_URL, {"reporterCode": str(reporter_code)})
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return []
        raise
    return sorted({
        int(row["period"])
        for row in (payload.get("data") or [])
        if row.get("period") is not None
    })


def _fetch_year(reporter_code: int, year: int) -> list[dict]:
    """All-partner imports+exports for one (reporter, year). [] on 404."""
    params = {
        "reporterCode": str(reporter_code),
        "period": str(year),
        "flowCode": "M,X",
        "cmdCode": "TOTAL",
        "includeDesc": "true",
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
    """Crawl the full bilateral matrix, one raw fragment per reporter.

    Stateless full re-pull with run-scoped resume: a reporter whose fragment is
    already committed under THIS run_id is skipped, so a supervisor-interrupted
    run resumes without re-fetching completed reporters and without persisting a
    cross-run watermark that would hole a fresh run's raw.
    """
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag for frag, meta in list_raw_fragments(node_id).items()
        if meta.get("run_id") == run_id
    }

    reporters = _active_reporters()
    print(f"UN Comtrade: {len(reporters)} active reporters "
          f"({len(done)} already done this run)")

    for i, rep in enumerate(reporters, 1):
        code = rep["code"]
        frag = str(code)
        if frag in done:
            continue  # committed earlier in this same run — resume past it

        years = _available_years(code)
        rows: list[dict] = []
        for year in years:
            rows.extend(_clean(r) for r in _fetch_year(code, year))

        if rows:
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            save_raw_parquet(table, node_id, fragment=frag)
            print(f"  [{i}/{len(reporters)}] {rep['name']} ({code}): "
                  f"{len(rows):,} rows over {len(years)} years")
        else:
            # No data for this reporter (or all years 404/empty). Write nothing
            # — an empty fragment would fail the nonempty-batch health check.
            print(f"  [{i}/{len(reporters)}] {rep['name']} ({code}): no data")


DOWNLOAD_SPECS = [
    NodeSpec(id="un-comtrade-values", fn=fetch_values, kind="download"),
]
