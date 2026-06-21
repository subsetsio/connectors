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

Crawl shape — batched, resumable (one parquet batch per reporter):
  ~219 active reporters x ~25-35 available years ~= 6-8k calls. The public
  endpoint sustains ~1 req/sec (verified); we throttle to ~0.8 req/sec, so a
  full crawl is ~2-3h — within one CI run, and resumable if interrupted. State
  stores a per-reporter signature (hash of getDA period+checksum pairs); a
  reporter is re-fetched only when its signature changes (picks up source
  revisions) or has never been fetched. Raw is written per reporter before
  state advances, so an interrupt loses at most the in-flight reporter and the
  next run resumes. No self-imposed time/record budget — the supervisor caps
  wall-clock by interrupting the node; the per-reporter raw+state writes make
  that safe.

No incremental date filter exists (getDA carries no since cursor); refreshes
re-evaluate every reporter's signature. Net weight is omitted — it is 0/missing
for the TOTAL aggregation.
"""
import hashlib
import json

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    load_state,
    save_raw_parquet,
    save_state,
    transient_retry,
)

STATE_VERSION = 1

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


# Rate limiter sits on the innermost HTTP attempt so that EVERY attempt
# (including tenacity retries) is throttled — the public endpoint cooldown-bans
# sub-second bursts. ~0.8 req/sec (80% of the ~1 req/sec sustainable rate).
@sleep_and_retry
@limits(calls=4, period=5)
def _throttled_get(url: str, params: dict | None) -> httpx.Response:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


@transient_retry()
def _api_get(url: str, params: dict | None = None):
    return _throttled_get(url, params).json()


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


def _data_availability(reporter_code: int) -> list[dict]:
    """getDA rows for a reporter (which years/datasets have data). [] on 404."""
    try:
        payload = _api_get(DA_URL, {"reporterCode": str(reporter_code)})
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return []
        raise
    return payload.get("data") or []


def _signature(da_rows: list[dict]) -> str:
    """Stable hash of (period, datasetChecksum) pairs — changes when the source
    revises any of the reporter's annual datasets."""
    pairs = sorted(
        (row.get("period"), row.get("datasetChecksum")) for row in da_rows
    )
    return hashlib.sha256(
        json.dumps(pairs, default=str, sort_keys=True).encode()
    ).hexdigest()[:16]


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
    """Crawl the full bilateral matrix, one resumable parquet batch per reporter.

    Batch asset id = f"{node_id}-{reporterCode}" so the transform's dep view
    glob-unions every reporter batch automatically.
    """
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "reporters": {}}
    done = state.setdefault("reporters", {})

    reporters = _active_reporters()
    print(f"UN Comtrade: {len(reporters)} active reporters")

    for i, rep in enumerate(reporters, 1):
        code = rep["code"]
        da_rows = _data_availability(code)
        periods = sorted({
            int(row["period"]) for row in da_rows if row.get("period") is not None
        })
        sig = _signature(da_rows)

        if done.get(str(code)) == sig:
            continue  # already fetched at this revision — resume / incremental skip

        rows: list[dict] = []
        for year in periods:
            rows.extend(_clean(r) for r in _fetch_year(code, year))

        if rows:
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            save_raw_parquet(table, f"{node_id}-{code}")
            print(f"  [{i}/{len(reporters)}] {rep['name']} ({code}): "
                  f"{len(rows):,} rows over {len(periods)} years")
        else:
            print(f"  [{i}/{len(reporters)}] {rep['name']} ({code}): no data")

        # Raw written before state — a crash here re-fetches one reporter, never
        # records a phantom completion.
        done[str(code)] = sig
        save_state(node_id, state)


DOWNLOAD_SPECS = [
    NodeSpec(id="un-comtrade-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="un-comtrade-values-transform",
        deps=["un-comtrade-values"],
        sql='''
            SELECT
                CAST(refYear AS INTEGER)        AS year,
                CAST(reporterCode AS INTEGER)   AS reporter_code,
                any_value(reporterISO)          AS reporter_iso,
                any_value(reporterDesc)         AS reporter,
                CAST(partnerCode AS INTEGER)    AS partner_code,
                any_value(partnerISO)           AS partner_iso,
                any_value(partnerDesc)          AS partner,
                flowDesc                        AS flow,
                SUM(primaryValue)               AS trade_value_usd,
                bool_or(isReported)             AS is_reported
            FROM "un-comtrade-values"
            WHERE cmdCode = 'TOTAL'
              AND primaryValue IS NOT NULL
              AND refYear IS NOT NULL
              AND reporterCode IS NOT NULL
              AND partnerCode IS NOT NULL
              AND flowDesc IS NOT NULL
            GROUP BY refYear, reporterCode, partnerCode, flowDesc
        ''',
    ),
]
