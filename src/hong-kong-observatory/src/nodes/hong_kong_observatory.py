"""Hong Kong Observatory Open Data connector.

Single REST surface: https://data.weather.gov.hk/weatherAPI/opendata/opendata.php
All fetches are GET, no auth, CSV (or JSON for RYES). Six published subsets:

- daily-temperature      CLMTEMP/CLMMAXT/CLMMINT per station, full history (1884+ for HKO).
- astronomical-tides-hourly        HHOT, per station x year (forward predictions).
- astronomical-tides-high-low      HLT,  per station x year.
- sun-times              SRS, per year.
- moon-times             MRS, per year.
- weather-radiation-report  RYES, per date (2019-09-10..yesterday) -> incremental.

Year ranges for the prediction datasets (tides/sun/moon) drift with time, so the
valid year set is *discovered* each run by probing a candidate window and keeping
the years the API accepts (an out-of-range year/station returns a fixed error page,
which we detect via ERROR_SENTINEL). Temperature stations are fetched with no year
param, returning the station's whole history in one request.

RYES is the only expensive backfill (one request per date). It is incremental:
a date watermark in state, batched per calendar month, so the first run backfills
and later runs only fetch new days. Everything else is a stateless full re-pull.
"""

import csv
import io
import time
from datetime import date, datetime, timedelta, timezone

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
    SqlNodeSpec,
    get,
    is_transient,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)
from constants import CLM_STATIONS, TIDE_STATIONS, RYES_STATIONS

BASE = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
ERROR_SENTINEL = "Please include valid parameters"
STATE_VERSION = 1

# Hong Kong is UTC+8; "yesterday" / "today" are computed in HKT.
HKT = timezone(timedelta(hours=8))
RYES_SOURCE_MIN = date(2019, 9, 10)
RYES_THROTTLE_S = 0.4  # polite delay between per-date RYES requests


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _fetch_text(params) -> str:
    resp = get(BASE, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _ryes_retryable(exc):
    """RYES blocks on sustained request volume with HTTP 403, which clears after
    a pause — so we retry 403 (with long backoff) on top of the usual transient
    set. The per-request throttle below keeps us under the block threshold."""
    if is_transient(exc):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 403


@retry(
    retry=retry_if_exception(_ryes_retryable),
    wait=wait_exponential(multiplier=2, min=4, max=120),
    stop=stop_after_attempt(8),
    reraise=True,
)
def _fetch_json(params):
    resp = get(BASE, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _csv_rows(text):
    """Yield CSV rows from an HKO response, or None if the response is an error
    page. Strips the UTF-8 BOM."""
    if ERROR_SENTINEL in text or len(text) < 50:
        return None
    return list(csv.reader(io.StringIO(text.lstrip("﻿"))))


def _discover_years(data_type, ref_station=None):
    """Probe a generous candidate window and return the years the API serves
    for this data_type (predictions shift over time, so we never hardcode)."""
    current = datetime.now(tz=HKT).year
    years = []
    for year in range(current - 12, current + 5):
        params = {"dataType": data_type, "rformat": "csv", "year": year}
        if ref_station:
            params["station"] = ref_station
        rows = _csv_rows(_fetch_text(params))
        if rows and len(rows) > 2:
            years.append(year)
    if not years:
        raise AssertionError(f"{data_type}: discovered no valid years - API shape changed?")
    return years


# --------------------------------------------------------------------------- #
# daily-temperature  (CLMTEMP / CLMMAXT / CLMMINT)
# --------------------------------------------------------------------------- #
_TEMP_MEASURES = {"CLMTEMP": "mean", "CLMMAXT": "max", "CLMMINT": "min"}

_TEMP_SCHEMA = pa.schema([
    ("station", pa.string()),
    ("measure", pa.string()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("day", pa.int32()),
    ("value", pa.string()),        # "***" / "#" possible -> typed in transform
    ("completeness", pa.string()),
])


def fetch_daily_temperature(node_id: str) -> None:
    asset = node_id
    rows = []
    for data_type, measure in _TEMP_MEASURES.items():
        for station in CLM_STATIONS:
            csv_rows = _csv_rows(_fetch_text(
                {"dataType": data_type, "rformat": "csv", "station": station}
            ))
            if not csv_rows:
                continue  # station has no data for this measure
            for r in csv_rows:
                if len(r) < 4 or not (r[0].isdigit() and len(r[0]) == 4):
                    continue  # title / header / legend line
                rows.append({
                    "station": station,
                    "measure": measure,
                    "year": int(r[0]),
                    "month": int(r[1]),
                    "day": int(r[2]),
                    "value": r[3].strip(),
                    "completeness": (r[4].strip() if len(r) > 4 else ""),
                })
    assert rows, f"{asset}: no temperature rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_TEMP_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# astronomical-tides-hourly  (HHOT) - wide MM,DD,01..24 -> long
# --------------------------------------------------------------------------- #
_HHOT_SCHEMA = pa.schema([
    ("station", pa.string()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("day", pa.int32()),
    ("hour", pa.int32()),
    ("height_m", pa.string()),
])


def fetch_tides_hourly(node_id: str) -> None:
    asset = node_id
    years = _discover_years("HHOT", ref_station=TIDE_STATIONS[0])
    rows = []
    for station in TIDE_STATIONS:
        for year in years:
            csv_rows = _csv_rows(_fetch_text(
                {"dataType": "HHOT", "rformat": "csv", "station": station, "year": year}
            ))
            if not csv_rows:
                continue
            header = csv_rows[0]  # MM,DD,01,...,24
            hours = header[2:]
            for r in csv_rows[1:]:
                if len(r) < 3 or r[0] == "MM" or not r[0].isdigit():
                    continue
                month, day = int(r[0]), int(r[1])
                for h_label, val in zip(hours, r[2:]):
                    if val.strip() == "":
                        continue
                    rows.append({
                        "station": station, "year": year,
                        "month": month, "day": day,
                        "hour": int(h_label), "height_m": val.strip(),
                    })
    assert rows, f"{asset}: no hourly-tide rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_HHOT_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# astronomical-tides-high-low  (HLT) - up to 4 (time,height) events per day
# --------------------------------------------------------------------------- #
_HLT_SCHEMA = pa.schema([
    ("station", pa.string()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("day", pa.int32()),
    ("event", pa.int32()),
    ("time", pa.string()),
    ("height_m", pa.string()),
])


def fetch_tides_high_low(node_id: str) -> None:
    asset = node_id
    years = _discover_years("HLT", ref_station=TIDE_STATIONS[0])
    rows = []
    for station in TIDE_STATIONS:
        for year in years:
            csv_rows = _csv_rows(_fetch_text(
                {"dataType": "HLT", "rformat": "csv", "station": station, "year": year}
            ))
            if not csv_rows:
                continue
            for r in csv_rows[1:]:  # skip header (Month,Date,Time,Height(m),...)
                if len(r) < 4 or r[0] == "Month" or not r[0].isdigit():
                    continue
                month, day = int(r[0]), int(r[1])
                pairs = r[2:]
                for idx in range(0, len(pairs) - 1, 2):
                    t, h = pairs[idx].strip(), pairs[idx + 1].strip()
                    if t == "" and h == "":
                        continue
                    rows.append({
                        "station": station, "year": year,
                        "month": month, "day": day,
                        "event": idx // 2 + 1, "time": t, "height_m": h,
                    })
    assert rows, f"{asset}: no high-low-tide rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_HLT_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# sun-times (SRS) / moon-times (MRS) - YYYY-MM-DD,RISE,TRAN.,SET
# --------------------------------------------------------------------------- #
_ALMANAC_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("rise", pa.string()),
    ("transit", pa.string()),
    ("set", pa.string()),
])


def _fetch_almanac(asset, data_type):
    years = _discover_years(data_type)
    rows = []
    for year in years:
        csv_rows = _csv_rows(_fetch_text(
            {"dataType": data_type, "rformat": "csv", "year": year}
        ))
        if not csv_rows:
            continue
        for r in csv_rows[1:]:  # skip header
            if len(r) < 4 or not r[0][:4].isdigit():
                continue
            rows.append({
                "date": r[0].strip(),
                "rise": r[1].strip(),
                "transit": r[2].strip(),
                "set": r[3].strip(),
            })
    assert rows, f"{asset}: no {data_type} rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_ALMANAC_SCHEMA), asset)


def fetch_sun_times(node_id: str) -> None:
    _fetch_almanac(node_id, "SRS")


def fetch_moon_times(node_id: str) -> None:
    _fetch_almanac(node_id, "MRS")


# --------------------------------------------------------------------------- #
# weather-radiation-report (RYES) - per-date JSON, incremental, month batches
# --------------------------------------------------------------------------- #
_RYES_STATIONS_BY_LEN = sorted(RYES_STATIONS, key=len, reverse=True)

_RYES_SCHEMA = pa.schema([
    ("report_date", pa.string()),   # YYYYMMDD
    ("station", pa.string()),
    ("metric", pa.string()),
    ("value", pa.string()),
])


def _split_ryes_key(key):
    """Split a flat key like 'ChekLapKokMaxTemp' into (station, attribute) using
    longest-prefix matching. Returns None for non-station (global) keys."""
    for st in _RYES_STATIONS_BY_LEN:
        if key.startswith(st):
            return st, key[len(st):]
    return None


def _parse_ryes_day(payload, queried_date):
    if not isinstance(payload, dict) or not payload:
        return []
    report_date = str(payload.get("ReportTimeInfoDate") or queried_date)
    out = []
    for key, val in payload.items():
        split = _split_ryes_key(key)
        if not split:
            continue                       # global key (BulletinDate, NoteDesc, ...)
        station, attr = split
        if attr == "LocationName" or val in (None, ""):
            continue
        out.append({
            "report_date": report_date,
            "station": station,
            "metric": attr,
            "value": str(val).strip(),
        })
    return out


def fetch_weather_radiation_report(node_id: str) -> None:
    asset = node_id
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")  # last fully-fetched date, ISO 'YYYY-MM-DD'

    # Re-fetch from the start of the watermark's month so the current partial
    # month is rewritten as it fills in; otherwise start at the source minimum.
    if watermark:
        wm = date.fromisoformat(watermark)
        start = wm.replace(day=1)
    else:
        start = RYES_SOURCE_MIN
    end = datetime.now(tz=HKT).date() - timedelta(days=1)  # frozen for this run

    cur = max(start, RYES_SOURCE_MIN)
    month_rows = []
    month_key = None
    last_done = watermark

    def flush():
        nonlocal month_rows
        if month_rows and month_key:
            save_raw_parquet(
                pa.Table.from_pylist(month_rows, schema=_RYES_SCHEMA),
                f"{asset}-{month_key}",
            )
        month_rows = []

    while cur <= end:
        mk = cur.strftime("%Y%m")
        if month_key is None:
            month_key = mk
        elif mk != month_key:
            flush()
            save_state(asset, {"schema_version": STATE_VERSION, "watermark": last_done})
            month_key = mk

        payload = _fetch_json(
            {"dataType": "RYES", "rformat": "json",
             "date": cur.strftime("%Y%m%d"), "lang": "en"}
        )
        month_rows.extend(_parse_ryes_day(payload, cur.strftime("%Y%m%d")))
        last_done = cur.isoformat()
        cur += timedelta(days=1)
        time.sleep(RYES_THROTTLE_S)  # stay under the source's volume-based 403 block

    flush()
    if last_done:
        save_state(asset, {"schema_version": STATE_VERSION, "watermark": last_done})


# --------------------------------------------------------------------------- #
# DOWNLOAD_SPECS - one per entity-union entry
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="hong-kong-observatory-daily-temperature",
             fn=fetch_daily_temperature, kind="download"),
    NodeSpec(id="hong-kong-observatory-astronomical-tides-hourly",
             fn=fetch_tides_hourly, kind="download"),
    NodeSpec(id="hong-kong-observatory-astronomical-tides-high-low",
             fn=fetch_tides_high_low, kind="download"),
    NodeSpec(id="hong-kong-observatory-sun-times",
             fn=fetch_sun_times, kind="download"),
    NodeSpec(id="hong-kong-observatory-moon-times",
             fn=fetch_moon_times, kind="download"),
    NodeSpec(id="hong-kong-observatory-weather-radiation-report",
             fn=fetch_weather_radiation_report, kind="download"),
]


# --------------------------------------------------------------------------- #
# TRANSFORM_SPECS - one published Delta table per subset
# --------------------------------------------------------------------------- #
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="hong-kong-observatory-daily-temperature-transform",
        deps=["hong-kong-observatory-daily-temperature"],
        sql='''
            SELECT
                station,
                measure,
                make_date(year, month, day) AS date,
                CAST(TRY_CAST(value AS DOUBLE) AS DOUBLE) AS temperature_c,
                completeness
            FROM "hong-kong-observatory-daily-temperature"
            WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="hong-kong-observatory-astronomical-tides-hourly-transform",
        deps=["hong-kong-observatory-astronomical-tides-hourly"],
        sql='''
            SELECT
                station,
                make_date(year, month, day) AS date,
                hour,
                CAST(TRY_CAST(height_m AS DOUBLE) AS DOUBLE) AS height_m
            FROM "hong-kong-observatory-astronomical-tides-hourly"
            WHERE TRY_CAST(height_m AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="hong-kong-observatory-astronomical-tides-high-low-transform",
        deps=["hong-kong-observatory-astronomical-tides-high-low"],
        sql='''
            SELECT
                station,
                make_date(year, month, day) AS date,
                event,
                time,
                CAST(TRY_CAST(height_m AS DOUBLE) AS DOUBLE) AS height_m
            FROM "hong-kong-observatory-astronomical-tides-high-low"
            WHERE TRY_CAST(height_m AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="hong-kong-observatory-sun-times-transform",
        deps=["hong-kong-observatory-sun-times"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                NULLIF(rise, '')    AS rise,
                NULLIF(transit, '') AS transit,
                NULLIF("set", '')   AS "set"
            FROM "hong-kong-observatory-sun-times"
            WHERE TRY_CAST(date AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="hong-kong-observatory-moon-times-transform",
        deps=["hong-kong-observatory-moon-times"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                NULLIF(rise, '')    AS rise,
                NULLIF(transit, '') AS transit,
                NULLIF("set", '')   AS "set"
            FROM "hong-kong-observatory-moon-times"
            WHERE TRY_CAST(date AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="hong-kong-observatory-weather-radiation-report-transform",
        deps=["hong-kong-observatory-weather-radiation-report"],
        sql='''
            SELECT
                strptime(report_date, '%Y%m%d')::DATE AS date,
                station,
                metric,
                CAST(TRY_CAST(value AS DOUBLE) AS DOUBLE) AS value
            FROM "hong-kong-observatory-weather-radiation-report"
            WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
