"""Australian Bureau of Meteorology — Water Data Online (KISTERS KiWIS).

Three published subsets, all sourced from the public KiWIS QueryServices API
(https://www.bom.gov.au/waterdata/services, anonymous, JSON):

  * ``stations``   — the national water monitoring-station register (one fetch,
                     getStationList). Reference geography.
  * ``timeseries`` — the catalog of the canonical daily series we publish values
                     for (one row per ts_id; getTimeseriesList per parameter,
                     filtered to the canonical daily ts_name). Reference/metadata.
  * ``values``     — long-format daily observations for every series in the
                     catalog (getTimeseriesValues). The flagship subset.

`values` is a continuation-resumable firehose. The full corpus is ~35k daily
series and hundreds of millions of observations — far more than one
getTimeseriesValues request (it caps total returned data points at ~60k) and
more than one 6h CI job. So we batch a bounded number of series over bounded
date windows sized to stay under the point cap, write one raw parquet per
(parameter, series-chunk), and drive progress through the orchestrator's
**continuation** mechanism rather than durable cross-run state.

Resume model — this is the crucial bit:

  * Raw assets are *run-scoped* (``runs/<RUN_ID>/raw/…``); state files are
    *durable* (``data/state/…``). A continuation chain reuses the same RUN_ID,
    so completed chunks' raw parquets accumulate within the chain. A *fresh*
    dispatch gets a new RUN_ID and an empty raw dir.
  * Therefore resume is keyed on ``raw_asset_exists(chunk_asset)`` — "is this
    chunk already materialised in THIS run?" — never on a durable "complete"
    flag. (Skipping on durable state was the original bug: a fresh run inherited
    the prior chain's "all complete" markers, skipped every chunk, wrote zero
    raw, and the transform failed with "no raw files found".)
  * When a soft wall-clock budget (just under the orchestrator's
    ``DAG_TIME_BUDGET``) is spent with chunks still unwritten, the node returns
    ``True`` to request a continuation; the runner re-triggers with the same
    RUN_ID and we pick up at the first chunk whose raw is missing. When every
    chunk's raw exists, the node returns ``None`` (done) and the downstream
    transform runs over the full accumulated corpus.

No incremental server-side query is used — getTimeseriesValues takes from/to but
we re-derive each chunk's window from its members' coverage and pull the full
span; the published Delta table is overwritten from raw each successful run.
"""
import os
import time
import pyarrow as pa
from datetime import date, timedelta

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_asset_exists,
)

from constants import BASE_URL, PARAM_DAILY_TSNAME

# getTimeseriesValues caps total data points per request (~60k observed). Daily
# series carry ~1 point/day, so keep n_series * window_days under the cap; a
# denser-than-expected window is caught by the split-on-500 fallback below.
SERIES_PER_CALL = 80
WINDOW_DAYS = 730  # ~2y; 80 * 730 = 58_400 worst-case points, under the ~60k cap

# Coverage fallbacks when a series reports no from/to (sparse/empty series).
GLOBAL_START = date(1900, 1, 1)

# Safety ceiling: a single (chunk, window) sub-request that keeps 500ing even
# after splitting down to a 1-day window is a real failure, not source size.
MIN_WINDOW_DAYS = 1

# Yield for continuation this many seconds before the orchestrator's hard
# DAG_TIME_BUDGET deadline, so we always stop on a clean chunk boundary (a
# completed raw parquet) rather than being SIGKILLed mid-write.
CONTINUATION_MARGIN_S = 900.0


# --------------------------------------------------------------------------- #
# KiWIS transport
# --------------------------------------------------------------------------- #
@transient_retry()
def _kiwis(request: str, *, read_timeout: float = 180.0, **params):
    """One KiWIS QueryServices GET, returning parsed JSON. Retries transient
    network errors / 429 / 5xx with backoff (5xx from an over-large
    getTimeseriesValues window is handled separately by the caller, which
    shrinks the window before this decorator's retries would matter)."""
    query = {
        "service": "kisters",
        "type": "QueryServices",
        "request": request,
        "datasource": "0",
        "format": "json",
    }
    query.update(params)
    resp = get(BASE_URL, params=query, timeout=(15.0, read_timeout))
    resp.raise_for_status()
    return resp.json()


def _table(payload):
    """KiWIS table responses are [header_row, *data_rows]. Return (header, rows)."""
    if isinstance(payload, list) and payload and isinstance(payload[0], list):
        return payload[0], payload[1:]
    return [], []


def _to_float(s):
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _iso_date(s):
    """Parse the leading YYYY-MM-DD of a KiWIS timestamp like
    '1987-01-24T09:00:00.000+10:00'. Returns a date or None."""
    if not s:
        return None
    try:
        return date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# stations
# --------------------------------------------------------------------------- #
STATIONS_SCHEMA = pa.schema([
    ("station_no", pa.string()),
    ("station_id", pa.string()),
    ("station_name", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
])


def fetch_stations(node_id: str) -> None:
    payload = _kiwis(
        "getStationList",
        returnfields="station_no,station_id,station_name,station_latitude,station_longitude",
        read_timeout=240.0,
    )
    header, data = _table(payload)
    idx = {name: header.index(name) for name in header}
    rows = []
    for r in data:
        rows.append({
            "station_no": r[idx["station_no"]],
            "station_id": r[idx["station_id"]],
            "station_name": r[idx["station_name"]],
            "latitude": _to_float(r[idx["station_latitude"]]),
            "longitude": _to_float(r[idx["station_longitude"]]),
        })
    table = pa.Table.from_pylist(rows, schema=STATIONS_SCHEMA)
    save_raw_parquet(table, node_id)


# --------------------------------------------------------------------------- #
# timeseries catalog (also the universe `values` iterates)
# --------------------------------------------------------------------------- #
TIMESERIES_SCHEMA = pa.schema([
    ("ts_id", pa.string()),
    ("ts_name", pa.string()),
    ("ts_unitname", pa.string()),
    ("station_no", pa.string()),
    ("station_name", pa.string()),
    ("parametertype_name", pa.string()),
    ("from_date", pa.string()),
    ("to_date", pa.string()),
])


def _canonical_series(parameter: str, ts_name: str) -> list[dict]:
    """All canonical daily series for one parameter, with coverage."""
    payload = _kiwis(
        "getTimeseriesList",
        parametertype_name=parameter,
        ts_name=ts_name,
        returnfields="ts_id,ts_name,ts_unitname,station_no,station_name,parametertype_name,coverage",
        read_timeout=240.0,
    )
    header, data = _table(payload)
    idx = {name: header.index(name) for name in header}
    out = []
    for r in data:
        out.append({
            "ts_id": r[idx["ts_id"]],
            "ts_name": r[idx["ts_name"]],
            "ts_unitname": r[idx.get("ts_unitname", -1)] if "ts_unitname" in idx else "",
            "station_no": r[idx["station_no"]],
            "station_name": r[idx.get("station_name", -1)] if "station_name" in idx else "",
            "parametertype_name": r[idx["parametertype_name"]],
            "from_date": r[idx["from"]] if "from" in idx else "",
            "to_date": r[idx["to"]] if "to" in idx else "",
        })
    return out


def fetch_timeseries(node_id: str) -> None:
    rows = []
    for parameter, ts_name in sorted(PARAM_DAILY_TSNAME.items()):
        try:
            rows.extend(_canonical_series(parameter, ts_name))
        except httpx.HTTPStatusError as exc:
            print(f"  skip timeseries parameter={parameter!r}: HTTP {exc.response.status_code}")
    table = pa.Table.from_pylist(rows, schema=TIMESERIES_SCHEMA)
    save_raw_parquet(table, node_id)


# --------------------------------------------------------------------------- #
# values firehose
# --------------------------------------------------------------------------- #
VALUES_SCHEMA = pa.schema([
    ("ts_id", pa.string()),
    ("timestamp", pa.string()),
    ("value", pa.float64()),
])


def _fetch_window(ts_ids: list[str], start: date, end: date) -> list[dict]:
    """Observations for `ts_ids` within [start, end]. Splits the date range on
    a cap-induced 500 so an unexpectedly dense window still completes."""
    try:
        payload = _kiwis(
            "getTimeseriesValues",
            ts_id=",".join(ts_ids),
            read_timeout=240.0,
            **{"from": start.isoformat(), "to": end.isoformat()},
        )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 500 and (end - start).days > MIN_WINDOW_DAYS:
            mid = start + (end - start) / 2
            return _fetch_window(ts_ids, start, mid) + _fetch_window(
                ts_ids, mid + timedelta(days=1), end)
        raise

    rows = []
    for block in payload:
        tsid = block.get("ts_id")
        for point in block.get("data") or []:
            if len(point) < 2:
                continue
            value = _to_float(point[1])
            if value is None:
                continue
            rows.append({"ts_id": tsid, "timestamp": point[0], "value": value})
    return rows


def _chunk_bounds(members: list[dict]) -> tuple[date, date]:
    froms = [_iso_date(m["from_date"]) for m in members]
    tos = [_iso_date(m["to_date"]) for m in members]
    start = min((d for d in froms if d), default=GLOBAL_START)
    end = max((d for d in tos if d), default=date.today())
    if end < start:
        end = date.today()
    return start, end


def _param_slug(parameter: str) -> str:
    keep = [c if c.isalnum() else "-" for c in parameter.lower()]
    return "".join(keep).strip("-").replace("--", "-") or "param"


def _soft_deadline() -> float | None:
    """monotonic() time after which we should yield for a continuation, leaving
    CONTINUATION_MARGIN_S of headroom before the orchestrator's hard
    DAG_TIME_BUDGET. None (no budget) means run to completion in one process —
    the local/dev path."""
    try:
        budget = float(os.environ.get("DAG_TIME_BUDGET", "0"))
    except ValueError:
        budget = 0.0
    if budget <= 0:
        return None
    return time.monotonic() + max(budget - CONTINUATION_MARGIN_S, 60.0)


def fetch_values(node_id: str):
    """Materialise every (parameter, series-chunk) as one raw parquet, resuming
    on raw existence and yielding via continuation when the time budget is spent.

    Returns True to request a continuation (chunks still unwritten in this run),
    or None when the full corpus is materialised."""
    deadline = _soft_deadline()
    pending = 0   # chunks still needing a fetch when we yielded
    written = 0   # chunks materialised this invocation

    for parameter, ts_name in sorted(PARAM_DAILY_TSNAME.items()):
        try:
            series = _canonical_series(parameter, ts_name)
        except httpx.HTTPStatusError as exc:
            print(f"  skip values parameter={parameter!r}: HTTP {exc.response.status_code}")
            continue
        series.sort(key=lambda m: m["ts_id"])
        pslug = _param_slug(parameter)
        chunks = [series[i:i + SERIES_PER_CALL]
                  for i in range(0, len(series), SERIES_PER_CALL)]

        for ci, members in enumerate(chunks):
            asset = f"{node_id}-{pslug}-{ci:05d}"
            # Resume on run-scoped raw: a chunk already written in THIS run (or
            # an earlier link of this continuation chain, same RUN_ID) is done.
            if raw_asset_exists(asset):
                continue

            # Out of time — defer the rest to a continuation (same RUN_ID, so the
            # chunks we've written persist and we'll skip them next invocation).
            if deadline is not None and time.monotonic() >= deadline:
                pending += 1
                continue

            ts_ids = [m["ts_id"] for m in members]
            start, end = _chunk_bounds(members)
            rows: list[dict] = []
            w_start = start
            while w_start <= end:
                w_end = min(w_start + timedelta(days=WINDOW_DAYS - 1), end)
                try:
                    rows.extend(_fetch_window(ts_ids, w_start, w_end))
                except httpx.HTTPStatusError as exc:
                    print(f"  values {asset} window {w_start}..{w_end}: "
                          f"HTTP {exc.response.status_code}; skipped")
                w_start = w_end + timedelta(days=1)

            # Write raw even when empty: the parquet's existence is the resume
            # marker, so an all-gap chunk isn't re-attempted every continuation.
            table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
            save_raw_parquet(table, asset)
            written += 1

    if pending:
        print(f"  values: wrote {written} chunk(s) this run, {pending} still "
              f"pending — requesting continuation")
        return True
    print(f"  values: corpus complete ({written} chunk(s) written this run)")
    return None


# --------------------------------------------------------------------------- #
# DAG
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="australian-bureau-of-meteorology-stations", fn=fetch_stations, kind="download"),
    NodeSpec(id="australian-bureau-of-meteorology-timeseries", fn=fetch_timeseries, kind="download"),
    NodeSpec(id="australian-bureau-of-meteorology-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="australian-bureau-of-meteorology-stations-transform",
        deps=["australian-bureau-of-meteorology-stations"],
        sql='''
            SELECT
                station_no,
                station_name,
                station_id,
                latitude,
                longitude
            FROM "australian-bureau-of-meteorology-stations"
            WHERE station_no IS NOT NULL AND station_no <> ''
            QUALIFY row_number() OVER (PARTITION BY station_no ORDER BY station_name) = 1
        ''',
    ),
    SqlNodeSpec(
        id="australian-bureau-of-meteorology-timeseries-transform",
        deps=["australian-bureau-of-meteorology-timeseries"],
        sql='''
            SELECT
                ts_id,
                station_no,
                parametertype_name AS parameter,
                ts_name,
                ts_unitname AS unit,
                TRY_CAST(substr(from_date, 1, 10) AS DATE) AS coverage_from,
                TRY_CAST(substr(to_date, 1, 10) AS DATE)   AS coverage_to
            FROM "australian-bureau-of-meteorology-timeseries"
            WHERE ts_id IS NOT NULL AND ts_id <> ''
            QUALIFY row_number() OVER (PARTITION BY ts_id ORDER BY to_date DESC) = 1
        ''',
    ),
    SqlNodeSpec(
        id="australian-bureau-of-meteorology-values-transform",
        deps=[
            "australian-bureau-of-meteorology-values",
            "australian-bureau-of-meteorology-timeseries",
        ],
        sql='''
            SELECT
                v.ts_id,
                t.station_no,
                t.parametertype_name AS parameter,
                t.ts_name,
                t.ts_unitname        AS unit,
                TRY_CAST(substr(v.timestamp, 1, 10) AS DATE) AS date,
                CAST(v.value AS DOUBLE)                       AS value
            FROM "australian-bureau-of-meteorology-values" v
            LEFT JOIN "australian-bureau-of-meteorology-timeseries" t USING (ts_id)
            WHERE v.value IS NOT NULL
              AND TRY_CAST(substr(v.timestamp, 1, 10) AS DATE) IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY v.ts_id, TRY_CAST(substr(v.timestamp, 1, 10) AS DATE)
                ORDER BY v.timestamp DESC
            ) = 1
        ''',
    ),
]
