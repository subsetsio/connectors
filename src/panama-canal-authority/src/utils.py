"""Shared helpers for the Panama Canal Authority (ACP) AQUARIUS WebPortal.

The portal (https://panama.aquaticinformatics.net/) exposes hydrology /
meteorology / oceanography time-series for the Panama Canal watershed via three
anonymous endpoints:

  POST /Data/Data_List              -> all monitoring stations (one request)
  POST /Data/Datasets  locationId=N -> the time-series at one station
  GET  /Export/DataSet?DataSet=..   -> a ZIP wrapping one CSV (Timestamp,Value)

Both node fetches share the catalog crawl + the per-station filtering here.
"""

import io
import json
import math
import re
import urllib.parse
import zipfile
from concurrent.futures import ThreadPoolExecutor

import httpx
from subsets_utils import get, post, transient_retry

BASE = "https://panama.aquaticinformatics.net"
PORTAL_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://panama.aquaticinformatics.net/",
}

# Stations / labels that are NOT observed measurements. The "SIMULACIONES"
# station holds model what-if scenario runs (e.g. drought forecast cadets), the
# "Tst*" stations are test rigs, and any series whose label advertises a
# forecast/simulation/idealized curve is a model output, not a gauge reading.
# "Idealizada" tide series are harmonic tide predictions (they project years into
# the future, e.g. to 2029) — model output, unlike the "Telem Radar/Shaft" gauge
# readings at real stations. None of these belong in a published observations table.
EXCLUDE_LOCATIONS = {"SIMULACIONES"}
EXCLUDE_LOC_PREFIXES = ("Tst",)
FORECAST_LABEL_RE = re.compile(r"forecast|pron[oó]s|simulac|idealiz", re.IGNORECASE)

_UNIT_RE = re.compile(r"Value\s*\(([^)]*)\)")


@transient_retry()
def _post(path: str, data: dict):
    r = post(BASE + path, data=data, headers=PORTAL_HEADERS, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r


def _json_response(r: httpx.Response, endpoint: str):
    """Parse portal JSON, retrying the occasional empty/HTML 200 response."""
    if not r.content.strip():
        raise httpx.RemoteProtocolError(f"empty JSON response from {endpoint}")
    try:
        return r.json()
    except json.JSONDecodeError as e:
        ctype = r.headers.get("content-type", "?")
        preview = r.text[:120].replace("\n", " ")
        raise httpx.RemoteProtocolError(
            f"invalid JSON response from {endpoint} (ct={ctype}, body={preview!r})"
        ) from e


@transient_retry()
def _post_json(path: str, data: dict, endpoint: str):
    return _json_response(_post(path, data), endpoint)


@transient_retry()
def _export_payload(series_id: str) -> bytes:
    """Fetch one series' export ZIP and return the inner CSV bytes.

    Under sustained load the portal occasionally answers a 200 with a non-ZIP
    body (a redirect/rate-limit HTML page) instead of the export. That is a
    transient hiccup, so we raise a transient-classified error to make
    `transient_retry` back off and retry rather than crashing the whole node on
    one bad response.
    """
    q = urllib.parse.urlencode({"DataSet": series_id, "DateRange": "EntirePeriodOfRecord"})
    r = get(f"{BASE}/Export/DataSet?{q}", headers=PORTAL_HEADERS, timeout=(10.0, 300.0))
    r.raise_for_status()
    content = r.content
    if content[:2] != b"PK":
        ctype = r.headers.get("content-type", "?")
        raise httpx.RemoteProtocolError(
            f"non-zip export for {series_id} (ct={ctype}, {len(content)} bytes)"
        )
    zf = zipfile.ZipFile(io.BytesIO(content))
    return zf.read(zf.namelist()[0])


def watershed_of(location_folder: str | None) -> str:
    """The watershed grouping, e.g. 'All Locations.Cuenca Gatun' -> 'Cuenca Gatun'."""
    parts = (location_folder or "").split(".")
    return parts[1] if len(parts) > 1 else (parts[0] or "")


def fetch_locations() -> dict:
    """Map LocationIdentifier -> station record (with coords, type, watershed)."""
    payload = _post_json(
        "/Data/Data_List",
        {"sort": "", "page": 1, "pageSize": 5000, "group": "", "filter": ""},
        "/Data/Data_List",
    )
    data = payload["Data"]
    return {l["LocationIdentifier"]: l for l in data if l.get("LocationIdentifier")}


def _keep(loc_ident: str, label: str) -> bool:
    if loc_ident in EXCLUDE_LOCATIONS:
        return False
    if any(loc_ident.startswith(p) for p in EXCLUDE_LOC_PREFIXES):
        return False
    if FORECAST_LABEL_RE.search(label or ""):
        return False
    return True


def fetch_series() -> list[dict]:
    """Crawl every station's datasets; return the kept observed series.

    Each item: {series_id, parameter, label, location_identifier, location_name,
    location_type, watershed, latitude, longitude, start_time, end_time, timezone}.
    """
    locations = fetch_locations()

    def _datasets(loc_ident: str, rec: dict) -> list[dict]:
        out = []
        raw = _post_json(
            "/Data/Datasets",
            {"locationId": rec["LocationId"]},
            f"/Data/Datasets locationId={rec['LocationId']}",
        )
        for s in raw:
            wv = s.get("WidgetVariables") or {}
            ident = wv.get("Identifier") or s.get("DisplayText")
            label = wv.get("Label") or s.get("Id") or ""
            if not ident or not _keep(loc_ident, label):
                continue
            out.append(
                {
                    "series_id": ident,
                    "parameter": s.get("ParameterName"),
                    "label": label,
                    "location_identifier": loc_ident,
                    "location_name": rec.get("Location"),
                    "location_type": rec.get("LocType"),
                    "watershed": watershed_of(rec.get("LocationFolder")),
                    "latitude": rec.get("LocY"),
                    "longitude": rec.get("LocX"),
                    "start_time": s.get("StartTime"),
                    "end_time": s.get("EndTime"),
                    "timezone": s.get("Timezone"),
                }
            )
        return out

    series: list[dict] = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        for group in ex.map(lambda kv: _datasets(*kv), locations.items()):
            series.extend(group)
    # Stable order so reruns produce identical raw.
    series.sort(key=lambda s: s["series_id"])
    return series


def export_daily(series_id: str):
    """Export a series' full period of record and roll it up to a daily summary.

    Returns (unit, rows) where each row is
    (date_iso, value_mean, value_min, value_max, value_sum, n_obs).
    Native resolution ranges from sub-hourly telemetry to already-daily series;
    we collapse every series to one row per calendar day so the published table
    is a clean, uniform daily product instead of 285M mixed-frequency points.
    """
    payload = _export_payload(series_id)

    unit = None
    # date -> [sum, count, min, max]
    agg: dict[str, list] = {}
    text = io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8", errors="replace")
    for line in text:
        if not line or line[0] == "#":
            continue
        if unit is None and line.startswith("Timestamp"):
            m = _UNIT_RE.search(line)
            unit = m.group(1).strip() if m else ""
            continue
        comma = line.find(",")
        if comma < 10:
            continue
        day = line[:10]  # YYYY-MM-DD
        rest = line[comma + 1 :]
        c2 = rest.find(",")
        token = (rest if c2 == -1 else rest[:c2]).strip()
        if not token:
            continue
        try:
            v = float(token)
        except ValueError:
            continue
        # The portal emits "NaN" for missing/flagged readings; float() parses it
        # happily and one NaN would poison the whole day's sum/mean. Drop any
        # non-finite value so each day aggregates only real observations.
        if not math.isfinite(v):
            continue
        slot = agg.get(day)
        if slot is None:
            agg[day] = [v, 1, v, v]
        else:
            slot[0] += v
            slot[1] += 1
            if v < slot[2]:
                slot[2] = v
            if v > slot[3]:
                slot[3] = v

    rows = [
        (day, s[0] / s[1], s[2], s[3], s[0], s[1])
        for day, s in sorted(agg.items())
    ]
    return (unit or ""), rows
