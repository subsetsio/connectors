"""Open-Meteo connector.

Open-Meteo is a per-coordinate REST weather/climate API family (one hostname per
product, identical query/response conventions, no auth for non-commercial use,
and NO catalog endpoint). We publish four products, each sampled at a fixed
curated set of global cities (see src/constants.py). Location is a column on the
long-format table, never a per-location node.

Products (one DOWNLOAD_SPEC + one TRANSFORM_SPEC each):
  - archive-daily        ERA5/ERA5-Land daily reanalysis, 1940-present
  - climate-projections  downscaled CMIP6 daily projections, 1950-2050, x models
  - flood                GloFAS daily river discharge, 1984-present
  - air-quality          CAMS hourly air quality, 2013-present

Fetch shape: stateless full re-pull. Each refresh re-fetches every location's
full history in one request (start_date..end_date) and overwrites. There is no
watermark — the archive/climate/flood/AQ ranges are bounded and re-pulling picks
up reanalysis revisions for free. The archive node is the slow one (~30s per
location for the full 1940-present daily range); all products run as independent
nodes, so wall-clock is the single slowest node, not the sum.
"""

from datetime import datetime, timedelta, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import LOCATIONS, CLIMATE_MODELS

# Documented dataset bounds (constants of the upstream datasets, not arbitrary
# year ranges). Open-Meteo docs: ERA5 from 1940, GloFAS from 1984, CAMS air
# quality from 2013, CMIP6 downscaled projections 1950-2050.
ARCHIVE_START = "1940-01-01"
FLOOD_START = "1984-01-01"
AIR_QUALITY_START = "2013-01-01"
CLIMATE_START = "1950-01-01"
CLIMATE_END = "2050-12-31"

# Reanalysis products lag real time; pull up to a few days before today.
ARCHIVE_LATENCY_DAYS = 6

ARCHIVE_DAILY_VARS = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "precipitation_sum", "rain_sum", "snowfall_sum",
    "wind_speed_10m_max", "wind_gusts_10m_max",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration",
]
CLIMATE_DAILY_VARS = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "precipitation_sum", "wind_speed_10m_mean",
    "shortwave_radiation_sum", "relative_humidity_2m_mean",
]
FLOOD_DAILY_VARS = ["river_discharge"]
AIR_QUALITY_HOURLY_VARS = [
    "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
    "sulphur_dioxide", "ozone", "aerosol_optical_depth", "dust", "uv_index",
]


def _today_utc():
    return datetime.now(tz=timezone.utc).date()


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/network, then reraises
def _request(base_url: str, params: dict) -> dict:
    resp = get(base_url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_point(base_url: str, lat: float, lon: float, granularity: str,
                 variables: list, extra: dict) -> dict:
    """Fetch one product time series for one coordinate. Returns the granularity
    block ({'time': [...], var: [...]}) or {} if the source reports an error for
    this point (e.g. ocean cell with no land data)."""
    params = {
        "latitude": lat,
        "longitude": lon,
        granularity: ",".join(variables),
        "timezone": "GMT",
        "timeformat": "iso8601",
    }
    params.update(extra)
    data = _request(base_url, params)
    if isinstance(data, dict) and data.get("error"):
        print(f"open-meteo: source error at ({lat},{lon}) on {base_url}: "
              f"{data.get('reason')!r} -- skipping point")
        return {}
    return data.get(granularity, {}) or {}


def _rows_for_point(block: dict, variables: list, time_key: str,
                    base_cols: dict) -> list:
    """Flatten an Open-Meteo granularity block (parallel arrays) into one dict
    per timestamp, prefixed with the location's base columns."""
    times = block.get(time_key, [])
    cols = {v: block.get(v, [None] * len(times)) for v in variables}
    rows = []
    for i, t in enumerate(times):
        row = dict(base_cols)
        row[time_key] = t
        for v in variables:
            val = cols[v][i] if i < len(cols[v]) else None
            row[v] = float(val) if isinstance(val, (int, float)) else None
        rows.append(row)
    return rows


def _location_schema(time_field: pa.DataType, time_name: str, variables: list,
                     extra_fields=()) -> pa.Schema:
    fields = [
        ("name", pa.string()),
        ("country", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
    ]
    fields.extend(extra_fields)
    fields.append((time_name, time_field))
    fields.extend((v, pa.float64()) for v in variables)
    return pa.schema(fields)


# ---- per-product fetch functions --------------------------------------------

def fetch_archive_daily(node_id: str) -> None:
    asset = node_id
    end = (_today_utc() - timedelta(days=ARCHIVE_LATENCY_DAYS)).isoformat()
    schema = _location_schema(pa.string(), "date", ARCHIVE_DAILY_VARS)
    rows = []
    for name, country, lat, lon in LOCATIONS:
        block = _fetch_point(
            "https://archive-api.open-meteo.com/v1/archive", lat, lon, "daily",
            ARCHIVE_DAILY_VARS, {"start_date": ARCHIVE_START, "end_date": end})
        rows.extend(_rows_for_point(
            block, ARCHIVE_DAILY_VARS, "date",
            {"name": name, "country": country, "latitude": lat, "longitude": lon}))
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


def fetch_climate_projections(node_id: str) -> None:
    asset = node_id
    schema = _location_schema(
        pa.string(), "date", CLIMATE_DAILY_VARS,
        extra_fields=[("model", pa.string())])
    rows = []
    for name, country, lat, lon in LOCATIONS:
        for model in CLIMATE_MODELS:
            block = _fetch_point(
                "https://climate-api.open-meteo.com/v1/climate", lat, lon, "daily",
                CLIMATE_DAILY_VARS,
                {"start_date": CLIMATE_START, "end_date": CLIMATE_END, "models": model})
            rows.extend(_rows_for_point(
                block, CLIMATE_DAILY_VARS, "date",
                {"name": name, "country": country, "latitude": lat,
                 "longitude": lon, "model": model}))
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


def fetch_flood(node_id: str) -> None:
    asset = node_id
    end = (_today_utc() - timedelta(days=1)).isoformat()
    schema = _location_schema(pa.string(), "date", FLOOD_DAILY_VARS)
    rows = []
    for name, country, lat, lon in LOCATIONS:
        block = _fetch_point(
            "https://flood-api.open-meteo.com/v1/flood", lat, lon, "daily",
            FLOOD_DAILY_VARS, {"start_date": FLOOD_START, "end_date": end})
        rows.extend(_rows_for_point(
            block, FLOOD_DAILY_VARS, "date",
            {"name": name, "country": country, "latitude": lat, "longitude": lon}))
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


def fetch_air_quality(node_id: str) -> None:
    asset = node_id
    end = (_today_utc() - timedelta(days=1)).isoformat()
    schema = _location_schema(pa.string(), "time", AIR_QUALITY_HOURLY_VARS)
    rows = []
    for name, country, lat, lon in LOCATIONS:
        block = _fetch_point(
            "https://air-quality-api.open-meteo.com/v1/air-quality", lat, lon,
            "hourly", AIR_QUALITY_HOURLY_VARS,
            {"start_date": AIR_QUALITY_START, "end_date": end})
        rows.extend(_rows_for_point(
            block, AIR_QUALITY_HOURLY_VARS, "time",
            {"name": name, "country": country, "latitude": lat, "longitude": lon}))
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="open-meteo-archive-daily", fn=fetch_archive_daily, kind="download"),
    NodeSpec(id="open-meteo-climate-projections", fn=fetch_climate_projections, kind="download"),
    NodeSpec(id="open-meteo-flood", fn=fetch_flood, kind="download"),
    NodeSpec(id="open-meteo-air-quality", fn=fetch_air_quality, kind="download"),
]


# ---- transforms: one published Delta table per subset -----------------------

def _daily_cast(variables: list) -> str:
    return ",\n            ".join(f'CAST({v} AS DOUBLE) AS {v}' for v in variables)


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="open-meteo-archive-daily-transform",
        deps=["open-meteo-archive-daily"],
        sql=f'''
        SELECT
            name,
            country,
            CAST(latitude AS DOUBLE)  AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            CAST(date AS DATE)        AS date,
            {_daily_cast(ARCHIVE_DAILY_VARS)}
        FROM "open-meteo-archive-daily"
        ''',
    ),
    SqlNodeSpec(
        id="open-meteo-climate-projections-transform",
        deps=["open-meteo-climate-projections"],
        sql=f'''
        SELECT
            name,
            country,
            CAST(latitude AS DOUBLE)  AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            model,
            CAST(date AS DATE)        AS date,
            {_daily_cast(CLIMATE_DAILY_VARS)}
        FROM "open-meteo-climate-projections"
        ''',
    ),
    SqlNodeSpec(
        id="open-meteo-flood-transform",
        deps=["open-meteo-flood"],
        sql=f'''
        SELECT
            name,
            country,
            CAST(latitude AS DOUBLE)  AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            CAST(date AS DATE)        AS date,
            {_daily_cast(FLOOD_DAILY_VARS)}
        FROM "open-meteo-flood"
        WHERE river_discharge IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="open-meteo-air-quality-transform",
        deps=["open-meteo-air-quality"],
        sql=f'''
        SELECT
            name,
            country,
            CAST(latitude AS DOUBLE)  AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            CAST(time AS TIMESTAMP)   AS time,
            {_daily_cast(AIR_QUALITY_HOURLY_VARS)}
        FROM "open-meteo-air-quality"
        ''',
    ),
]
