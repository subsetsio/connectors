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
import re
import urllib.parse
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from subsets_utils import get, post, transient_retry

BASE = "https://panama.aquaticinformatics.net"
PORTAL_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://panama.aquaticinformatics.net/",
}

# Stations / labels that are NOT observed measurements. The "SIMULACIONES"
# station holds model what-if scenario runs (e.g. drought forecast cadets), the
# "Tst*" stations are test rigs, and any series whose label advertises a
# forecast/simulation is a model output, not a gauge reading. None of these
# belong in a published observations table.
EXCLUDE_LOCATIONS = {"SIMULACIONES"}
EXCLUDE_LOC_PREFIXES = ("Tst",)
FORECAST_LABEL_RE = re.compile(r"forecast|pron[oó]s|simulac", re.IGNORECASE)

_UNIT_RE = re.compile(r"Value\s*\(([^)]*)\)")


@transient_retry()
def _post(path: str, data: dict):
    r = post(BASE + path, data=data, headers=PORTAL_HEADERS, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r


@transient_retry()
def _get(url: str, timeout=(10.0, 300.0)):
    r = get(url, headers=PORTAL_HEADERS, timeout=timeout)
    r.raise_for_status()
    return r


def watershed_of(location_folder: str | None) -> str:
    """The watershed grouping, e.g. 'All Locations.Cuenca Gatun' -> 'Cuenca Gatun'."""
    parts = (location_folder or "").split(".")
    return parts[1] if len(parts) > 1 else (parts[0] or "")


def fetch_locations() -> dict:
    """Map LocationIdentifier -> station record (with coords, type, watershed)."""
    data = _post(
        "/Data/Data_List",
        {"sort": "", "page": 1, "pageSize": 5000, "group": "", "filter": ""},
    ).json()["Data"]
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
        raw = _post("/Data/Datasets", {"locationId": rec["LocationId"]}).json()
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
    q = urllib.parse.urlencode(
        {"DataSet": series_id, "DateRange": "EntirePeriodOfRecord"}
    )
    resp = _get(f"{BASE}/Export/DataSet?{q}")
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    payload = zf.read(zf.namelist()[0])

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
