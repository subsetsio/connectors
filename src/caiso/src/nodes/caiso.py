"""California ISO (CAISO) OASIS connector.

OASIS exposes one public endpoint — `GET /oasisapi/SingleZip` — that serves a
fixed set of named reports ("querynames"). Each request returns a ZIP wrapping a
single report file (CSV when `resultformat=6`). A request is scoped by a GMT
datetime window plus report-specific parameters; there is no bulk dump, so the
only way to obtain history is to walk the window forward in chunks.

Shape: **date-windowed firehose** (one spec per report). Each report's fetch fn
walks `HISTORY_START -> today` in report-appropriate windows, writes one raw
ndjson batch per (window, market_run) and saves a date watermark after each, so a
supervisor interrupt resumes cleanly across the 6h-capped run chain. Within a
report, `market_run_id` (DAM/RTM/RTPD/HASP/...), node, AS region, fuel region,
TAC area etc. are *column values*, not separate specs — a single PRC_LMP report
covers the day-ahead and RUC markets across every requested node.

Volume control: the nodal LMP reports (PRC_LMP / PRC_HASP_LMP / PRC_INTVL_LMP /
PRC_RTPD_LMP) carry ~2,400 nodes — full nodal history is billions of rows, so we
bound them to the benchmark APNodes analysts actually price against (the three
trading hubs and the four default LAPs). Every other report is system / region /
interface level and is fetched in full. `HISTORY_START` is the connector's
history horizon (a documented constant, like the incremental pattern's
SOURCE_MIN); the upper bound is discovered dynamically so it never goes stale.

OASIS returns *errors as a 200 ZIP* containing an XML report (not an HTTP error),
so each response is classified: CSV -> rows; "invalid parameters" XML -> that
market_run is dead for this report (skipped for the rest of the run); throttle /
processing XML -> transient (retried with backoff); anything else / no data ->
empty window. Values are coerced column-wise to int/float/str so the ndjson
carries real types; the SQL transforms are thin parse-and-publish passes.
"""

from datetime import datetime, timezone, date, timedelta
import csv
import io
import time
import xml.etree.ElementTree as ET
import zipfile

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
    save_raw_ndjson,
    load_state,
    save_state,
)

SLUG = "caiso"
STATE_VERSION = 1
BASE = "https://oasis.caiso.com/oasisapi/SingleZip"

# Initial backfill horizon. OASIS is aggressively throttled and serves only
# date-windowed requests, so a multi-year first backfill across every report
# cannot finish inside the run's time budget. We seed the first run with a recent
# rolling window; the saved watermark then makes every subsequent run extend
# coverage forward, so the published span grows monotonically run over run. Lower
# this (or backfill in stages) to reach further back in history.
INITIAL_BACKFILL_DAYS = 90


def _history_start() -> date:
    return datetime.now(timezone.utc).date() - timedelta(days=INITIAL_BACKFILL_DAYS)

# Benchmark APNodes for the nodal price reports: the three CAISO trading hubs plus
# the four default load-aggregation points. These are the headline prices; the
# full ~2,400-node set is intentionally out of scope (volume).
BENCHMARK_NODES = [
    "TH_NP15_GEN-APND",
    "TH_SP15_GEN-APND",
    "TH_ZP26_GEN-APND",
    "DLAP_PGAE-APND",
    "DLAP_SCE-APND",
    "DLAP_SDGE-APND",
    "DLAP_VEA-APND",
]

# A polite gap between requests. Each report runs in its own subprocess and OASIS
# throttles aggressive clients, so we pace requests and let backoff absorb the rest.
REQUEST_SPACING_S = 2.0


# Report config keyed by OASIS queryname:
#   window_days   — date-window size (kept under per-report query caps; smaller
#                   for higher-frequency reports).
#   market_runs   — market_run_id values to iterate, or [None] when the report
#                   takes no market_run_id. Invalid values self-prune at runtime.
#   params        — fixed report-specific query params (the documented "ALL" filters).
#   node_bounded  — True -> restrict to BENCHMARK_NODES via the `node` param.
def _r(window_days, market_runs, params=None, node_bounded=False):
    return {
        "window_days": window_days,
        "market_runs": market_runs,
        "params": params or {},
        "node_bounded": node_bounded,
    }


REPORTS = {
    # Prices — nodal LMP (benchmark nodes only)
    "PRC_LMP":       _r(30, ["DAM", "RUC"], node_bounded=True),
    "PRC_HASP_LMP":  _r(14, ["HASP"], node_bounded=True),
    "PRC_INTVL_LMP": _r(7,  ["RTM"], node_bounded=True),
    "PRC_RTPD_LMP":  _r(14, ["RTPD"], node_bounded=True),
    # Prices — system / region level
    "PRC_AS":        _r(30, ["DAM", "HASP"], {"anc_type": "ALL", "anc_region": "ALL"}),
    "PRC_INTVL_AS":  _r(14, ["RTM"], {"anc_type": "ALL", "anc_region": "ALL"}),
    "PRC_CNSTR":     _r(14, ["DAM", "HASP", "RTM"], {"ti_id": "ALL"}),
    "PRC_FUEL":      _r(30, [None], {"fuel_region_id": "ALL"}),
    # System demand & forecasts
    "SLD_FCST":      _r(30, ["DAM", "2DA", "7DA", "ACTUAL", "RTM"]),
    "SLD_REN_FCST":  _r(14, ["DAM", "RTD", "RTPD", "ACTUAL"]),
    "SLD_FCST_PEAK": _r(30, [None]),
    # Ancillary services
    "AS_RESULTS":    _r(30, ["DAM", "HASP"], {"anc_type": "ALL", "anc_region": "ALL"}),
    "AS_REQ":        _r(30, ["DAM", "HASP"], {"anc_type": "ALL", "anc_region": "ALL"}),
    "AS_OP_RSRV":    _r(30, [None]),
    # Energy accounting & commitment
    "ENE_SLRS":      _r(30, ["DAM", "RUC", "HASP", "RTM"], {"tac_zone_name": "ALL", "schedule": "ALL"}),
    "ENE_EA":        _r(30, [None], {"energy_type": "ALL", "opr_interval": "ALL"}),
    "ENE_LOSS":      _r(30, ["DAM", "HASP"]),
    "ENE_DISP":      _r(30, [None]),
    "CMMT_RA_MLC":   _r(30, ["DAM", "RTM"]),
    # Convergence (virtual) bidding aggregates
    "ENE_CB_AWARDS":     _r(30, [None]),
    "ENE_CB_CLR_AWARDS": _r(30, [None]),
    "ENE_CB_MKT_SUM":    _r(30, [None]),
    # Transmission
    "TRNS_USAGE":    _r(30, ["DAM", "HASP"], {"ti_id": "ALL", "ti_direction": "ALL"}),
    "TRNS_ATC":      _r(30, ["DAM", "HASP"], {"ti_id": "ALL", "ti_direction": "ALL"}),
    "TRNS_OUTAGE":   _r(30, [None], {"ti_id": "ALL", "ti_direction": "ALL"}),
}

# The entity union (rank-active subsets) — must equal REPORTS' keys exactly.
ENTITY_IDS = list(REPORTS.keys())


# ---------------------------------------------------------------------------
# HTTP with retry/backoff. OASIS surfaces some failures as a 200 ZIP carrying an
# error XML; the transient ones raise _TransientReport so the decorator retries.
# ---------------------------------------------------------------------------

class _TransientReport(Exception):
    """An in-band OASIS error that warrants a retry (throttle / processing)."""


_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (_TransientReport, *_TRANSIENT_EXC)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


def _err_desc(xml_text: str) -> str:
    """Pull the ERR_DESC out of an OASIS error report (namespace-agnostic)."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return ""
    for el in root.iter():
        if el.tag.rsplit("}", 1)[-1] == "ERR_DESC" and el.text:
            return el.text.strip()
    return ""


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=5, max=240),
    reraise=True,
)
def _fetch_window(params: dict) -> tuple[str, list[dict]]:
    """Fetch one SingleZip request. Returns (status, rows):
      ("ok", rows)   — CSV report parsed
      ("empty", [])  — valid request, no data for this window
      ("dead", [])   — invalid parameters (this market_run is unusable here)
    Raises _TransientReport / httpx errors for retryable failures. A throttled
    OASIS often hangs the read rather than 429-ing, so the read timeout is kept
    short enough to drop, back off, and retry (letting the throttle clear)."""
    resp = get(BASE, params=params, timeout=(10.0, 90.0))
    resp.raise_for_status()
    try:
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
    except zipfile.BadZipFile:
        raise _TransientReport("response was not a valid zip")
    name = zf.namelist()[0]
    raw = zf.read(name)
    if name.lower().endswith(".csv"):
        return ("ok", _parse_csv(raw.decode("utf-8-sig")))
    # Otherwise an XML report — either an error or an empty/no-data payload.
    desc = _err_desc(raw.decode("utf-8", "replace"))
    low = desc.lower()
    if not desc or "no data" in low or "not found" in low:
        return ("empty", [])
    if "invalid" in low:
        return ("dead", [])
    # throttle / processing / timeout / resubmit -> retry
    raise _TransientReport(f"OASIS transient error: {desc}")


# ---------------------------------------------------------------------------
# CSV parsing + column-wise type coercion (keeps ndjson batches unionable).
# ---------------------------------------------------------------------------

def _parse_csv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames:
        reader.fieldnames = [(f or "").strip() for f in reader.fieldnames]
    return [dict(row) for row in reader]


def _is_int(v) -> bool:
    try:
        int(v)
        return True
    except (TypeError, ValueError):
        return False


def _is_float(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def _typed_rows(rows: list[dict]) -> list[dict]:
    if not rows:
        return []
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    coltype: dict[str, str] = {}
    for c in cols:
        nonempty = [r.get(c) for r in rows if r.get(c) not in (None, "")]
        if not nonempty:
            coltype[c] = "str"
        elif all(_is_int(v) for v in nonempty):
            coltype[c] = "int"
        elif all(_is_float(v) for v in nonempty):
            coltype[c] = "float"
        else:
            coltype[c] = "str"
    out = []
    for r in rows:
        d = {}
        for c in cols:
            v = r.get(c)
            if v is None or v == "":
                d[c] = None
            elif coltype[c] == "int":
                d[c] = int(v)
            elif coltype[c] == "float":
                d[c] = float(v)
            else:
                d[c] = v
        out.append(d)
    return out


# ---------------------------------------------------------------------------
# Fetch — one generic date-windowed firehose for every report.
# ---------------------------------------------------------------------------

def _queryname(node_id: str) -> str:
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


def _gmt(d: date) -> str:
    # OASIS expects GMT; PST midnight (08:00Z) anchors the operating day window.
    return f"{d:%Y%m%d}T08:00-0000"


def fetch_report(node_id: str) -> None:
    qn = _queryname(node_id)
    cfg = REPORTS[qn]

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    start = _history_start()
    watermark = state.get("watermark")  # ISO date of last completed window end
    if watermark:
        # Re-fetch the trailing window so the previously-partial latest day
        # completes; overwriting its batch is idempotent (deterministic key).
        cur = date.fromisoformat(watermark) - timedelta(days=cfg["window_days"])
        if cur < start:
            cur = start
    else:
        cur = start
    end = datetime.now(timezone.utc).date()

    dead: set = set()
    window = timedelta(days=cfg["window_days"])

    while cur <= end:
        win_end = min(cur + window - timedelta(days=1), end)
        start_s = _gmt(cur)
        end_s = _gmt(win_end + timedelta(days=1))  # exclusive upper edge
        for mrid in cfg["market_runs"]:
            if mrid in dead:
                continue
            params = {
                "queryname": qn,
                "version": "1",
                "resultformat": "6",
                "startdatetime": start_s,
                "enddatetime": end_s,
            }
            params.update(cfg["params"])
            if mrid is not None:
                params["market_run_id"] = mrid
            if cfg["node_bounded"]:
                params["node"] = ",".join(BENCHMARK_NODES)

            try:
                status, rows = _fetch_window(params)
            except Exception as e:
                # Retries exhausted (persistent throttle/timeout on this window).
                # Skip it rather than aborting the whole connector — the DAG fails
                # the entire run on any single node failure, and a few dropped
                # windows are recoverable on a later run. Log loudly.
                print(f"[{SLUG}] {qn} {cur:%Y%m%d} mrid={mrid}: "
                      f"skipping window after {type(e).__name__}: {str(e)[:80]}")
                continue
            finally:
                time.sleep(REQUEST_SPACING_S)
            if status == "dead":
                # Invalid market_run for this report — stop requesting it.
                print(f"[{SLUG}] {qn}: market_run_id={mrid} invalid; skipping")
                dead.add(mrid)
                continue
            if rows:
                tag = (mrid or "all").lower().replace("_", "-")
                batch = f"{node_id}-{cur:%Y%m%d}-{tag}"
                save_raw_ndjson(_typed_rows(rows), batch)
        # Raw written before state advances.
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": win_end.isoformat()})
        cur = win_end + timedelta(days=1)


# ---------------------------------------------------------------------------
# Specs — one download + one thin publishing transform per report.
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_report,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Each report's batches share the column set; DISTINCT collapses exact duplicates
# produced by the trailing-window overlap re-fetch. The dep view glob-unions every
# `<id>-<window>-<run>` batch file automatically.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT DISTINCT * FROM "{s.id}"',
        temporal="INTERVALENDTIME_GMT",
    )
    for s in DOWNLOAD_SPECS
]
