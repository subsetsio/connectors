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
    get,
    is_transient,
    transient_retry,
    save_raw_parquet,
)
from constants import CLM_STATIONS, TIDE_STATIONS, RYES_STATIONS

BASE = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
ERROR_SENTINEL = "Please include valid parameters"

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
# weather-radiation-report (RYES) - per-date JSON, stateless full re-pull,
# written as one parquet batch per calendar month (overwritten each run).
#
# Deliberately stateless: a watermark resume is unsafe here because raw batches
# are not guaranteed to survive a failed prior run while state does, which would
# silently skip months whose raw is gone. Re-pulling the whole 2019-09..yesterday
# range each run (throttled, with 403-aware backoff) guarantees full coverage.
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
    cur = RYES_SOURCE_MIN
    end = datetime.now(tz=HKT).date() - timedelta(days=1)  # frozen for this run

    month_rows = []
    month_key = None

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
            flush()              # one parquet batch per calendar month
            month_key = mk

        payload = _fetch_json(
            {"dataType": "RYES", "rformat": "json",
             "date": cur.strftime("%Y%m%d"), "lang": "en"}
        )
        month_rows.extend(_parse_ryes_day(payload, cur.strftime("%Y%m%d")))
        cur += timedelta(days=1)
        time.sleep(RYES_THROTTLE_S)  # stay under the source's volume-based 403 block

    flush()


# --------------------------------------------------------------------------- #
# Endpoints beyond opendata.php (weather / earthquake / lunar-calendar)
# --------------------------------------------------------------------------- #
WEATHER_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
LUNAR_URL = "https://data.weather.gov.hk/weatherAPI/opendata/lunardate.php"


def _iso_date(s):
    """'20260711' -> '2026-07-11' (ISO date), or '' if not an 8-digit date."""
    s = str(s or "").strip()
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else s


def _iso_ts(s):
    """'202607110600' -> '2026-07-11T06:00:00' (ISO ts), or '' if not 12 digits."""
    s = str(s or "").strip()
    if len(s) == 12 and s.isdigit():
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[8:10]}:{s[10:12]}:00"
    return s


@transient_retry()
def _fetch_url_text(url, params) -> str:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_url_json(url, params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------------- #
# nine-day-forecast (weather.php dataType=fnd) - snapshot, overwrite each run
# --------------------------------------------------------------------------- #
_FND_SCHEMA = pa.schema([
    ("update_time", pa.string()),
    ("general_situation", pa.string()),
    ("forecast_date", pa.string()),   # YYYYMMDD
    ("week", pa.string()),
    ("forecast_wind", pa.string()),
    ("forecast_weather", pa.string()),
    ("max_temp_c", pa.float64()),
    ("min_temp_c", pa.float64()),
    ("max_rh_pct", pa.float64()),
    ("min_rh_pct", pa.float64()),
    ("forecast_icon", pa.int32()),
    ("psr", pa.string()),
])


def _num(d):
    """Extract a numeric {value,unit} entry, or None."""
    if isinstance(d, dict) and d.get("value") not in (None, ""):
        try:
            return float(d["value"])
        except (TypeError, ValueError):
            return None
    return None


def fetch_nine_day_forecast(node_id: str) -> None:
    asset = node_id
    d = _fetch_url_json(WEATHER_URL, {"dataType": "fnd", "lang": "en"})
    update_time = str(d.get("updateTime") or "")
    general = str(d.get("generalSituation") or "")
    rows = []
    for f in d.get("weatherForecast") or []:
        icon = f.get("ForecastIcon")
        rows.append({
            "update_time": update_time,
            "general_situation": general,
            "forecast_date": _iso_date(f.get("forecastDate")),
            "week": str(f.get("week") or ""),
            "forecast_wind": str(f.get("forecastWind") or ""),
            "forecast_weather": str(f.get("forecastWeather") or ""),
            "max_temp_c": _num(f.get("forecastMaxtemp")),
            "min_temp_c": _num(f.get("forecastMintemp")),
            "max_rh_pct": _num(f.get("forecastMaxrh")),
            "min_rh_pct": _num(f.get("forecastMinrh")),
            "forecast_icon": int(icon) if isinstance(icon, int) else None,
            "psr": str(f.get("PSR") or ""),
        })
    assert rows, f"{asset}: no forecast rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_FND_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# current-weather-report (weather.php dataType=rhrread) - snapshot, long format
# --------------------------------------------------------------------------- #
_RHR_SCHEMA = pa.schema([
    ("update_time", pa.string()),
    ("category", pa.string()),   # temperature | humidity | rainfall_max
    ("place", pa.string()),
    ("value", pa.float64()),
    ("unit", pa.string()),
])


def fetch_current_weather_report(node_id: str) -> None:
    asset = node_id
    d = _fetch_url_json(WEATHER_URL, {"dataType": "rhrread", "lang": "en"})
    update_time = str(d.get("updateTime") or "")
    rows = []

    def _emit(category, block, value_key):
        for rec in (block.get("data") if isinstance(block, dict) else None) or []:
            v = rec.get(value_key)
            try:
                val = float(v)
            except (TypeError, ValueError):
                continue
            rows.append({
                "update_time": update_time,
                "category": category,
                "place": str(rec.get("place") or ""),
                "value": val,
                "unit": str(rec.get("unit") or ""),
            })

    _emit("temperature", d.get("temperature"), "value")
    _emit("humidity", d.get("humidity"), "value")
    _emit("rainfall_max", d.get("rainfall"), "max")
    assert rows, f"{asset}: no current-weather rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_RHR_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# lightning-count (opendata.php dataType=LHL, CSV) - snapshot (latest hour)
# --------------------------------------------------------------------------- #
_LHL_SCHEMA = pa.schema([
    ("period_start", pa.string()),     # ISO ts of the reporting window start
    ("period_end", pa.string()),       # ISO ts of the reporting window end
    ("type", pa.string()),
    ("region", pa.string()),
    ("count", pa.int64()),
])


def fetch_lightning_count(node_id: str) -> None:
    asset = node_id
    csv_rows = _csv_rows(_fetch_text({"dataType": "LHL", "lang": "en", "rformat": "csv"}))
    assert csv_rows, f"{asset}: no lightning CSV returned"
    rows = []
    for r in csv_rows[1:]:  # skip header
        if len(r) < 4:
            continue
        try:
            cnt = int(float(r[3].strip()))
        except (ValueError, IndexError):
            continue
        span = r[0].strip().split("-")
        rows.append({
            "period_start": _iso_ts(span[0]) if span else "",
            "period_end": _iso_ts(span[1]) if len(span) > 1 else "",
            "type": r[1].strip(),
            "region": r[2].strip(),
            "count": cnt,
        })
    assert rows, f"{asset}: no lightning rows parsed"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_LHL_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# visibility-10min-mean (opendata.php dataType=LTMV, CSV) - snapshot
# --------------------------------------------------------------------------- #
_LTMV_SCHEMA = pa.schema([
    ("observed_at", pa.string()),     # ISO ts (from YYYYMMDDHHMM)
    ("station", pa.string()),
    ("visibility", pa.string()),      # e.g. "28 km" / ">50 km"; typed in transform
])


def fetch_visibility_10min_mean(node_id: str) -> None:
    asset = node_id
    csv_rows = _csv_rows(_fetch_text({"dataType": "LTMV", "lang": "en", "rformat": "csv"}))
    assert csv_rows, f"{asset}: no visibility CSV returned"
    rows = []
    for r in csv_rows[1:]:  # skip header
        if len(r) < 3 or not r[0].strip().isdigit():
            continue
        rows.append({
            "observed_at": _iso_ts(r[0].strip()),
            "station": r[1].strip(),
            "visibility": r[2].strip(),
        })
    assert rows, f"{asset}: no visibility rows parsed"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_LTMV_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# gregorian-lunar-calendar (lunardate.php) - one request per date over the
# valid window (discovered each run: the API serves a rolling ~6-year window).
# Stateless full re-pull; days outside the served window return "Not Available".
# --------------------------------------------------------------------------- #
_LUNAR_SCHEMA = pa.schema([
    ("date", pa.string()),         # YYYY-MM-DD
    ("lunar_year", pa.string()),   # Gan-Zhi + zodiac (Chinese)
    ("lunar_date", pa.string()),   # lunar month/day (Chinese)
])
_LUNAR_THROTTLE_S = 0.1


def _discover_lunar_years():
    """Return the Gregorian years the lunardate API currently serves (it exposes
    a rolling window that drifts with the calendar, so we never hardcode it)."""
    current = datetime.now(tz=HKT).year
    years = []
    for year in range(current - 8, current + 8):
        txt = _fetch_url_text(LUNAR_URL, {"date": f"{year}-01-01"})
        if txt.lstrip().startswith("{"):
            years.append(year)
    if not years:
        raise AssertionError("lunardate: discovered no valid years - API shape changed?")
    return years


def fetch_gregorian_lunar_calendar(node_id: str) -> None:
    asset = node_id
    years = _discover_lunar_years()
    rows = []
    for year in years:
        cur = date(year, 1, 1)
        end = date(year, 12, 31)
        while cur <= end:
            txt = _fetch_url_text(LUNAR_URL, {"date": cur.isoformat()})
            s = txt.lstrip()
            if s.startswith("{"):
                import json as _json
                try:
                    obj = _json.loads(s)
                except ValueError:
                    obj = None
                if isinstance(obj, dict) and obj.get("LunarDate"):
                    rows.append({
                        "date": cur.isoformat(),
                        "lunar_year": str(obj.get("LunarYear") or ""),
                        "lunar_date": str(obj.get("LunarDate") or ""),
                    })
            cur += timedelta(days=1)
            time.sleep(_LUNAR_THROTTLE_S)
    assert rows, f"{asset}: no lunar-calendar rows fetched"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_LUNAR_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# stations - reference catalog of station codes used across the datasets.
# HKO exposes no machine-readable station endpoint, so this is derived from the
# documented station sets (constants.py); one row per (code, dataset group).
# --------------------------------------------------------------------------- #
_STATIONS_SCHEMA = pa.schema([
    ("station_code", pa.string()),
    ("dataset_group", pa.string()),   # climate | tide
])


def fetch_stations(node_id: str) -> None:
    asset = node_id
    rows = [{"station_code": s, "dataset_group": "climate"} for s in CLM_STATIONS]
    rows += [{"station_code": s, "dataset_group": "tide"} for s in TIDE_STATIONS]
    assert rows, f"{asset}: no station rows built"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA), asset)


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
    NodeSpec(id="hong-kong-observatory-nine-day-forecast",
             fn=fetch_nine_day_forecast, kind="download"),
    NodeSpec(id="hong-kong-observatory-current-weather-report",
             fn=fetch_current_weather_report, kind="download"),
    NodeSpec(id="hong-kong-observatory-lightning-count",
             fn=fetch_lightning_count, kind="download"),
    NodeSpec(id="hong-kong-observatory-visibility-10min-mean",
             fn=fetch_visibility_10min_mean, kind="download"),
    NodeSpec(id="hong-kong-observatory-gregorian-lunar-calendar",
             fn=fetch_gregorian_lunar_calendar, kind="download"),
    NodeSpec(id="hong-kong-observatory-stations",
             fn=fetch_stations, kind="download"),
]
