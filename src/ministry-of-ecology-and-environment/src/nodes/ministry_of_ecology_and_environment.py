"""Ministry of Ecology and Environment (China) — national air-quality monitoring.

Source: China National Environmental Monitoring Centre (CNEMC, under MEE) national
real-time air-quality publishing platform (https://air.cnemc.cn:18007). Undocumented
AJAX/JSON API, no auth, no pagination — each request returns the entire national-control
network (~1600 stations) in one JSON array.

Two published subsets:
  * stations              — reference catalog of monitoring stations (one row per station).
  * air_quality_readings  — long-format hourly readings (one row per station-hour).

The platform exposes only the current hour (GetAllAQIPublishLive) plus a short rolling
window of recent hours (GetAQIHistoryByConditionHis, one hour per call). There is NO deep
historical archive, so this is a snapshot-forward source: each run re-pulls the live hour
plus the retained rolling window and overwrites. Stateless full re-pull — no watermark.
"""

import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    post,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://air.cnemc.cn:18007"
_LIVE_URL = f"{BASE}/HourChangesPublish/GetAllAQIPublishLive"
_HIST_URL = f"{BASE}/HourChangesPublish/GetAQIHistoryByConditionHis"

# Headers the platform's XHR uses. ASCII-only.
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": BASE,
    "Referer": BASE + "/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

# How many hours of the rolling window to attempt to backfill each run, in addition to
# the live current hour. The platform retains only ~24-30h, so hours beyond that return
# an empty array and are skipped (not an error). 36 is a safe ceiling above the window.
_WINDOW_HOURS = 36

_DOTNET_DATE_RE = re.compile(r"/Date\((-?\d+)")


def _parse_time_ms(timepoint):
    """Extract the epoch-ms integer from a .NET '/Date(1782075600000)/' string."""
    if not timepoint:
        return None
    m = _DOTNET_DATE_RE.search(timepoint)
    return int(m.group(1)) if m else None


@transient_retry()
def _post_live():
    resp = post(_LIVE_URL, headers=_HEADERS, data=b"", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_hour(date_str):
    resp = post(
        _HIST_URL,
        headers={**_HEADERS, "Content-Type": "application/x-www-form-urlencoded"},
        data={"date": date_str},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _beijing_now_floor_hour():
    """Current Beijing time floored to the hour (the platform labels hours in CST, UTC+8)."""
    from datetime import datetime, timedelta, timezone

    cst = timezone(timedelta(hours=8))
    return datetime.now(tz=cst).replace(minute=0, second=0, microsecond=0)


def _annotate(rows):
    """Attach the parsed epoch-ms to each record (the .NET date is awkward for SQL)."""
    out = []
    for r in rows:
        r = dict(r)
        r["time_ms"] = _parse_time_ms(r.get("TimePoint"))
        out.append(r)
    return out


def fetch_stations(node_id: str) -> None:
    """Reference catalog: one row per national-control station, from the live snapshot."""
    rows = _annotate(_post_live())
    seen = {}
    for r in rows:
        code = r.get("StationCode")
        if code and code not in seen:
            seen[code] = {
                "StationCode": code,
                "PositionName": r.get("PositionName"),
                "Area": r.get("Area"),
                "CityCode": r.get("CityCode"),
                "ProvinceId": r.get("ProvinceId"),
                "Latitude": r.get("Latitude"),
                "Longitude": r.get("Longitude"),
            }
    save_raw_ndjson(list(seen.values()), node_id)


def fetch_air_quality_readings(node_id: str) -> None:
    """Long-format hourly readings: live current hour + retained rolling window, deduped
    on (StationCode, time_ms). Snapshot-forward; the published table is overwritten each run."""
    by_key = {}

    def _ingest(rows):
        for r in rows:
            code = r.get("StationCode")
            tms = r.get("time_ms")
            if code is None or tms is None:
                continue
            by_key.setdefault((code, tms), r)  # first writer wins; live precedes history

    # Live current hour first (authoritative, always available).
    _ingest(_annotate(_post_live()))

    # Then walk back over the rolling window. Empty hours (beyond retention) are skipped.
    base = _beijing_now_floor_hour()
    from datetime import timedelta

    for back in range(1, _WINDOW_HOURS + 1):
        hour = base - timedelta(hours=back)
        date_str = hour.strftime("%Y-%m-%d %H:00:00")
        hist = _post_hour(date_str)
        if not hist:
            continue
        _ingest(_annotate(hist))

    save_raw_ndjson(list(by_key.values()), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ministry-of-ecology-and-environment-stations",
        fn=fetch_stations,
        kind="download",
    ),
    NodeSpec(
        id="ministry-of-ecology-and-environment-air-quality-readings",
        fn=fetch_air_quality_readings,
        kind="download",
    ),
]


_STATIONS_ID = "ministry-of-ecology-and-environment-stations"
_READINGS_ID = "ministry-of-ecology-and-environment-air-quality-readings"

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_STATIONS_ID}-transform",
        deps=[_STATIONS_ID],
        sql=f'''
            SELECT DISTINCT
                CAST(StationCode AS VARCHAR)        AS station_code,
                CAST(PositionName AS VARCHAR)       AS station_name,
                CAST(Area AS VARCHAR)               AS area,
                TRY_CAST(CityCode AS INTEGER)       AS city_code,
                TRY_CAST(ProvinceId AS INTEGER)     AS province_id,
                TRY_CAST(Latitude AS DOUBLE)        AS latitude,
                TRY_CAST(Longitude AS DOUBLE)       AS longitude
            FROM "{_STATIONS_ID}"
            WHERE StationCode IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_READINGS_ID}-transform",
        deps=[_READINGS_ID],
        sql=f'''
            SELECT
                CAST(StationCode AS VARCHAR)              AS station_code,
                to_timestamp(time_ms / 1000.0)           AS observed_at,
                TRY_CAST(AQI AS INTEGER)                  AS aqi,
                NULLIF(CAST(Quality AS VARCHAR), '')      AS quality,
                NULLIF(NULLIF(CAST(PrimaryPollutant AS VARCHAR), ''), '—') AS primary_pollutant,
                TRY_CAST(PM2_5 AS DOUBLE)                 AS pm2_5,
                TRY_CAST(PM2_5_24h AS DOUBLE)             AS pm2_5_24h,
                TRY_CAST(PM10 AS DOUBLE)                  AS pm10,
                TRY_CAST(PM10_24h AS DOUBLE)              AS pm10_24h,
                TRY_CAST(SO2 AS DOUBLE)                   AS so2,
                TRY_CAST(SO2_24h AS DOUBLE)               AS so2_24h,
                TRY_CAST(NO2 AS DOUBLE)                   AS no2,
                TRY_CAST(NO2_24h AS DOUBLE)               AS no2_24h,
                TRY_CAST(O3 AS DOUBLE)                    AS o3,
                TRY_CAST(O3_24h AS DOUBLE)                AS o3_24h,
                TRY_CAST(O3_8h AS DOUBLE)                 AS o3_8h,
                TRY_CAST(O3_8h_24h AS DOUBLE)             AS o3_8h_24h,
                TRY_CAST(CO AS DOUBLE)                    AS co,
                TRY_CAST(CO_24h AS DOUBLE)                AS co_24h
            FROM "{_READINGS_ID}"
            WHERE StationCode IS NOT NULL AND time_ms IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY station_code, observed_at ORDER BY aqi DESC NULLS LAST
            ) = 1
        ''',
    ),
]
