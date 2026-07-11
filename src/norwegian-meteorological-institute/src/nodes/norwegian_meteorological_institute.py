"""Norwegian Meteorological Institute (api.met.no WeatherAPI) — raw fetches.

One download spec per accepted product. The accepted set is exactly the
products that return SQL-readable tabular data (JSON / XML / fixed-width
numeric text); imagery, GRIB/METGM binary grids, weather charts, and
free-text bulletins were rejected upstream at accept.

Fetch strategy per product family:

- Point-forecast products (locationforecast, nowcast, oceanforecast,
  airqualityforecast, subseasonal, sunrise) are queried by lat/lon. There is
  no entity universe inside a product, so we pull a fixed curated location set
  (src/constants.py) every run and overwrite — forecasts are rewritten each
  cycle, so full re-pull is the only correct shape.
- spotwind is a single XML product covering all regions x flight levels.
- metalerts is the full current-alert GeoJSON feed.
- tidalwater is a fixed-width numeric water-level table per harbor.
- iceberg is a growing archive of daily iceberg-observation snapshots
  (one dated file each, immutable once published). Fetched incrementally:
  each date is a fragment, and dates already committed to the raw manifest
  are skipped, so only new days are pulled on a refresh.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import httpx

from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://api.met.no/weatherapi"
SLUG = "norwegian-meteorological-institute"

# sunrise is astronomy: how many days ahead to enumerate per location.
SUNRISE_WINDOW_DAYS = 10


def _fetched_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


@transient_retry()
def _get(url: str, **kwargs):
    resp = get(url, timeout=(10.0, 120.0), **kwargs)
    resp.raise_for_status()
    return resp


def _is_permanent_4xx(err: httpx.HTTPStatusError) -> bool:
    """A location outside a product's domain returns a 4xx (not 429) — skip it."""
    r = err.response
    return r is not None and 400 <= r.status_code < 500 and r.status_code != 429


def _get_json(url: str, **kwargs):
    resp = _get(url, **kwargs)
    return resp.json(), resp


def _get_text(url: str, **kwargs) -> tuple[str, object]:
    resp = _get(url, **kwargs)
    return resp.text, resp


def _available(product: str, version: str) -> list[dict]:
    data, _ = _get_json(f"{BASE}/{product}/{version}/available.json")
    if not isinstance(data, list):
        raise ValueError(f"{product}: expected available.json list, got {type(data).__name__}")
    return data


# --------------------------------------------------------------------------- #
# METJSON point-forecast products (shared timeseries shape)
# --------------------------------------------------------------------------- #

_WINDOW_BLOCKS = ("next_1_hours", "next_6_hours", "next_12_hours", "next_24_hours")


def _flatten_metjson(name: str, lat: float, lon: float, doc: dict, fetched_at: str) -> list[dict]:
    """Flatten a METJSON forecast document into one row per timeseries step."""
    props = doc.get("properties") or {}
    updated_at = (props.get("meta") or {}).get("updated_at")
    rows = []
    for step in props.get("timeseries") or []:
        row = {
            "location": name,
            "lat": lat,
            "lon": lon,
            "time": step.get("time"),
            "updated_at": updated_at,
            "fetched_at": fetched_at,
        }
        data = step.get("data") or {}
        instant = ((data.get("instant") or {}).get("details")) or {}
        for k, v in instant.items():
            row[k] = v
        for block in _WINDOW_BLOCKS:
            blk = data.get(block)
            if not blk:
                continue
            symbol = (blk.get("summary") or {}).get("symbol_code")
            if symbol is not None:
                row[f"{block}_symbol_code"] = symbol
            for k, v in (blk.get("details") or {}).items():
                row[f"{block}_{k}"] = v
        rows.append(row)
    return rows


def _fetch_point_forecast(node_id: str, path: str, locations) -> None:
    fetched_at = _fetched_at()
    rows: list[dict] = []
    for name, lat, lon in locations:
        url = f"{BASE}/{path}?lat={lat:.4f}&lon={lon:.4f}"
        try:
            doc, _ = _get_json(url)
        except httpx.HTTPStatusError as err:
            if _is_permanent_4xx(err):
                continue  # location outside this product's domain
            raise
        rows.extend(_flatten_metjson(name, lat, lon, doc, fetched_at))
    save_raw_ndjson(rows, node_id)


def fetch_locationforecast(node_id: str) -> None:
    from constants import LAND_LOCATIONS

    _fetch_point_forecast(node_id, "locationforecast/2.0/compact", LAND_LOCATIONS)


def fetch_nowcast(node_id: str) -> None:
    from constants import LAND_LOCATIONS

    _fetch_point_forecast(node_id, "nowcast/2.0/complete", LAND_LOCATIONS)


def fetch_oceanforecast(node_id: str) -> None:
    from constants import SEA_LOCATIONS

    _fetch_point_forecast(node_id, "oceanforecast/2.0/complete", SEA_LOCATIONS)


def fetch_subseasonal(node_id: str) -> None:
    from constants import LAND_LOCATIONS

    _fetch_point_forecast(node_id, "subseasonal/1.0/complete", LAND_LOCATIONS)


# --------------------------------------------------------------------------- #
# airqualityforecast — data.time[] with a variables map
# --------------------------------------------------------------------------- #


def fetch_airqualityforecast(node_id: str) -> None:
    from constants import LAND_LOCATIONS

    fetched_at = _fetched_at()
    rows: list[dict] = []
    for name, lat, lon in LAND_LOCATIONS:
        url = f"{BASE}/airqualityforecast/0.1/?lat={lat:.4f}&lon={lon:.4f}"
        try:
            doc, _ = _get_json(url)
        except httpx.HTTPStatusError as err:
            if _is_permanent_4xx(err):
                continue
            raise
        for step in (doc.get("data") or {}).get("time") or []:
            row = {
                "location": name,
                "lat": lat,
                "lon": lon,
                "from_time": step.get("from"),
                "to_time": step.get("to"),
                "fetched_at": fetched_at,
            }
            for var, obj in (step.get("variables") or {}).items():
                if isinstance(obj, dict):
                    row[var] = obj.get("value")
            rows.append(row)
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# sunrise — one astronomy document per (location, date)
# --------------------------------------------------------------------------- #


def _sunrise_event(props: dict, key: str) -> dict:
    ev = props.get(key) or {}
    return {
        f"{key}_time": ev.get("time"),
        f"{key}_azimuth": ev.get("azimuth"),
        f"{key}_elevation": ev.get("disc_centre_elevation"),
        f"{key}_visible": ev.get("visible"),
    }


def fetch_sunrise(node_id: str) -> None:
    from constants import LAND_LOCATIONS

    fetched_at = _fetched_at()
    today = datetime.now(timezone.utc).date()
    dates = [(today + timedelta(days=d)).isoformat() for d in range(SUNRISE_WINDOW_DAYS)]
    rows: list[dict] = []
    for name, lat, lon in LAND_LOCATIONS:
        for date in dates:
            url = f"{BASE}/sunrise/3.0/sun?lat={lat:.4f}&lon={lon:.4f}&date={date}"
            try:
                doc, _ = _get_json(url)
            except httpx.HTTPStatusError as err:
                if _is_permanent_4xx(err):
                    continue
                raise
            props = doc.get("properties") or {}
            row = {
                "location": name,
                "lat": lat,
                "lon": lon,
                "date": date,
                "body": props.get("body"),
                "fetched_at": fetched_at,
            }
            for key in ("sunrise", "sunset", "solarnoon", "solarmidnight"):
                row.update(_sunrise_event(props, key))
            rows.append(row)
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# spotwind — single XML product (region x valid time x flight level)
# --------------------------------------------------------------------------- #


def _spot_num(value):
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fetch_spotwind(node_id: str) -> None:
    fetched_at = _fetched_at()
    text, _ = _get_text(f"{BASE}/spotwind/1.1/")
    root = ET.fromstring(text)
    rows: list[dict] = []
    for product in root.iter("product"):
        observation = product.get("observation")
        for time_el in product.iter("time"):
            valid = time_el.get("valid")
            for loc in time_el.iter("location"):
                loc_name = loc.get("name")
                for sw in loc.iter("spotWind"):
                    rows.append(
                        {
                            "observation": observation,
                            "valid_time": valid,
                            "location": loc_name,
                            "flight_level": _spot_num(sw.get("flightlevel")),
                            "wind_direction": _spot_num(sw.get("windDirection")),
                            "wind_speed": _spot_num(sw.get("windSpeed")),
                            "temperature": _spot_num(sw.get("temperature")),
                            "fetched_at": fetched_at,
                        }
                    )
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# metalerts — current weather-alert GeoJSON feed
# --------------------------------------------------------------------------- #


def fetch_metalerts(node_id: str) -> None:
    data, resp = _get_json(f"{BASE}/metalerts/2.0/all.json?lang=en")
    rows = []
    fetched_at = _fetched_at()
    for idx, feature in enumerate(data.get("features", [])):
        props = feature.get("properties") or {}
        interval = (feature.get("when") or {}).get("interval") or []
        rows.append(
            {
                "alert_id": props.get("id"),
                "feature_index": idx,
                "title": props.get("title"),
                "description": props.get("description"),
                "event": props.get("event"),
                "area": props.get("area"),
                "geographic_domain": props.get("geographicDomain"),
                "risk_matrix_color": props.get("riskMatrixColor"),
                "severity": props.get("severity"),
                "certainty": props.get("certainty"),
                "status": props.get("status"),
                "awareness_level": props.get("awareness_level"),
                "awareness_type": props.get("awareness_type"),
                "published_at": resp.headers.get("last-modified"),
                "interval_start": interval[0] if len(interval) > 0 else None,
                "interval_end": interval[1] if len(interval) > 1 else None,
                "geometry_type": (feature.get("geometry") or {}).get("type"),
                "geometry_json": _json_dumps(feature.get("geometry")),
                "properties_json": _json_dumps(props),
                "fetched_at": fetched_at,
            }
        )
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# tidalwater — fixed-width numeric water-level table per harbor
# --------------------------------------------------------------------------- #


def _parse_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_tidal_rows(harbor: str, updated, text: str, fetched_at: str) -> list[dict]:
    rows = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("AAR MND DAG"):
            in_table = True
            continue
        if not in_table or not stripped[:4].isdigit():
            continue
        parts = stripped.split()
        if len(parts) < 13:
            continue
        year, month, day, hour, minute = (int(parts[i]) for i in range(5))
        observed_at = datetime(year, month, day, hour, minute, tzinfo=timezone.utc).isoformat()
        rows.append(
            {
                "harbor": harbor,
                "updated": updated,
                "observed_at": observed_at,
                "surge": _parse_float(parts[5]),
                "tide": _parse_float(parts[6]),
                "total": _parse_float(parts[7]),
                "p0": _parse_float(parts[8]),
                "p25": _parse_float(parts[9]),
                "p50": _parse_float(parts[10]),
                "p75": _parse_float(parts[11]),
                "p100": _parse_float(parts[12]),
                "fetched_at": fetched_at,
            }
        )
    return rows


def fetch_tidalwater(node_id: str) -> None:
    rows = []
    fetched_at = _fetched_at()
    for item in _available("tidalwater", "1.1"):
        params = item.get("params") or {}
        harbor = params.get("harbor")
        uri = item.get("uri")
        if not harbor or not uri:
            raise ValueError(f"tidalwater available item missing harbor or uri: {item!r}")
        text, resp = _get_text(uri)
        rows.extend(
            _parse_tidal_rows(harbor, item.get("updated") or resp.headers.get("last-modified"), text, fetched_at)
        )
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# iceberg — growing archive of daily iceberg-observation snapshots
# --------------------------------------------------------------------------- #


def _iceberg_available_dates() -> list[str]:
    data, _ = _get_json(f"{BASE}/iceberg/0.1/available.json")
    dates = []
    for item in data if isinstance(data, list) else []:
        date = (item.get("params") or {}).get("date")
        if date:
            dates.append(date)
    return sorted(set(dates))


def fetch_iceberg(node_id: str) -> None:
    done = set(list_raw_fragments(node_id, "ndjson.zst").keys())
    for date in _iceberg_available_dates():
        fragment = date.replace("-", "")
        if fragment in done:
            continue  # already committed on a prior run — immutable, skip
        fetched_at = _fetched_at()
        try:
            doc, _ = _get_json(f"{BASE}/iceberg/0.1/?date={date}")
        except httpx.HTTPStatusError as err:
            if _is_permanent_4xx(err):
                continue
            raise
        rows = []
        for feature in doc.get("features") or []:
            geom = feature.get("geometry") or {}
            coords = geom.get("coordinates") or [None, None]
            props = feature.get("properties") or {}
            rows.append(
                {
                    "date": date,
                    "instant": (feature.get("when") or {}).get("instant"),
                    "lon": coords[0] if len(coords) > 0 else None,
                    "lat": coords[1] if len(coords) > 1 else None,
                    "brgare": props.get("BRGARE"),
                    "ia_bcn": props.get("IA_BCN"),
                    "ia_bln": props.get("IA_BLN"),
                    "ais_chk": props.get("ais_chk"),
                    "title": props.get("title"),
                    "fetched_at": fetched_at,
                }
            )
        save_raw_ndjson(rows, node_id, fragment=fragment)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-airqualityforecast", fn=fetch_airqualityforecast, kind="download"),
    NodeSpec(id=f"{SLUG}-iceberg", fn=fetch_iceberg, kind="download"),
    NodeSpec(id=f"{SLUG}-locationforecast", fn=fetch_locationforecast, kind="download"),
    NodeSpec(id=f"{SLUG}-metalerts", fn=fetch_metalerts, kind="download"),
    NodeSpec(id=f"{SLUG}-nowcast", fn=fetch_nowcast, kind="download"),
    NodeSpec(id=f"{SLUG}-oceanforecast", fn=fetch_oceanforecast, kind="download"),
    NodeSpec(id=f"{SLUG}-spotwind", fn=fetch_spotwind, kind="download"),
    NodeSpec(id=f"{SLUG}-subseasonal", fn=fetch_subseasonal, kind="download"),
    NodeSpec(id=f"{SLUG}-sunrise", fn=fetch_sunrise, kind="download"),
    NodeSpec(id=f"{SLUG}-tidalwater", fn=fetch_tidalwater, kind="download"),
]
