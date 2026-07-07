import json
from datetime import datetime, timezone

from subsets_utils import NodeSpec, get, save_raw_ndjson


BASE = "https://api.met.no/weatherapi"
SLUG = "norwegian-meteorological-institute"


def _fetched_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json(), resp


def _get_text(url: str) -> tuple[str, object]:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text, resp


def _available(product: str, version: str) -> list[dict]:
    data, _ = _get_json(f"{BASE}/{product}/{version}/available.json")
    if not isinstance(data, list):
        raise ValueError(f"{product}: expected available.json list, got {type(data).__name__}")
    return data


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


def fetch_textforecast(node_id: str) -> None:
    rows = []
    fetched_at = _fetched_at()
    for item in _available("textforecast", "3.0"):
        forecast = (item.get("params") or {}).get("forecast")
        uri = item.get("uri")
        if not forecast or not uri:
            raise ValueError(f"textforecast available item missing forecast or uri: {item!r}")
        data, resp = _get_json(uri)
        features = data.get("features") or []
        if not features:
            rows.append(
                {
                    "forecast": forecast,
                    "feature_index": None,
                    "lang": data.get("lang"),
                    "last_change": data.get("lastChange") or resp.headers.get("last-modified"),
                    "geometry_type": None,
                    "geometry_json": None,
                    "properties_json": None,
                    "fetched_at": fetched_at,
                }
            )
            continue
        for idx, feature in enumerate(features):
            props = feature.get("properties") or {}
            rows.append(
                {
                    "forecast": forecast,
                    "feature_index": idx,
                    "lang": data.get("lang"),
                    "last_change": data.get("lastChange") or resp.headers.get("last-modified"),
                    "geometry_type": (feature.get("geometry") or {}).get("type"),
                    "geometry_json": _json_dumps(feature.get("geometry")),
                    "properties_json": _json_dumps(props),
                    "fetched_at": fetched_at,
                }
            )
    save_raw_ndjson(rows, node_id)


def fetch_aviationforecast(node_id: str) -> None:
    rows = []
    fetched_at = _fetched_at()
    for item in _available("aviationforecast", "2.0"):
        uri = item.get("uri")
        endpoint = item.get("endpoint")
        params = item.get("params") or {}
        if not uri or not endpoint:
            raise ValueError(f"aviationforecast available item missing endpoint or uri: {item!r}")
        text, resp = _get_text(uri)
        rows.append(
            {
                "endpoint": endpoint,
                "icao": params.get("icao"),
                "wmoheader": params.get("wmoheader"),
                "updated": item.get("updated") or resp.headers.get("last-modified"),
                "content": text,
                "content_length": len(text),
                "fetched_at": fetched_at,
            }
        )
    save_raw_ndjson(rows, node_id)


def _parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_tidal_rows(harbor: str, updated: str | None, text: str, fetched_at: str) -> list[dict]:
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
        rows.extend(_parse_tidal_rows(harbor, item.get("updated") or resp.headers.get("last-modified"), text, fetched_at))
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-aviationforecast", fn=fetch_aviationforecast, kind="download"),
    NodeSpec(id=f"{SLUG}-metalerts", fn=fetch_metalerts, kind="download"),
    NodeSpec(id=f"{SLUG}-textforecast", fn=fetch_textforecast, kind="download"),
    NodeSpec(id=f"{SLUG}-tidalwater", fn=fetch_tidalwater, kind="download"),
]
