"""Environment Agency (England) — Hydrology API.

Source: https://environment.data.gov.uk/hydrology (Epimorphics linked-data
platform, Open Government Licence v3, no auth).

Three assets:

- ``stations``  reference catalog, one row per monitoring station (~9.5k).
- ``measures``  series catalog, one row per measure = station x parameter x
                period x statistic (~32k).
- ``readings``  long-format observations, one row per (measure, date).

Readings scope. The corpus is ~32k measures at periods from 15-minute to
daily with decades of history — far too large to re-pull in full every run.
We take the DAILY statistic (period=86400 s) over a rolling
``READINGS_WINDOW_DAYS`` window. The bulk endpoint returns every measure's
daily readings for a date window in one request, so we page by fixed date
chunks (~105 requests) rather than per-measure (~9.6k requests).

Because each run brings a rolling window rather than the complete dataset,
the published readings table is written with ``write_mode: merge`` on
(measure_id, date) — history accumulates across runs instead of being
truncated to the window. Measured: a 7-day chunk is ~51k rows / ~23 s, so a
730-day window is ~5M rows in ~1 h.
"""

import csv
import datetime as _dt
import io

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet, raw_parquet_writer, transient_retry

_BASE = "https://environment.data.gov.uk/hydrology"

# Readings scope: daily statistic, rolling window, chunked by date.
READINGS_PERIOD = 86400          # daily, in seconds
READINGS_WINDOW_DAYS = 730       # ~2 years per run; merge accumulates the rest
READINGS_CHUNK_DAYS = 7          # ~51k rows/request, well under the 2M hard cap


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #

@transient_retry()
def _get_json(path: str, **params):
    resp = get(f"{_BASE}/{path}", params=params, timeout=(10.0, 300.0),
               headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_csv_text(path: str, **params) -> str:
    resp = get(f"{_BASE}/{path}", params=params, timeout=(10.0, 600.0),
               headers={"Accept": "text/csv"})
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# Flatten helpers — the linked-data records nest {@id, label} structs
# --------------------------------------------------------------------------- #

def _last_seg(uri):
    return uri.rsplit("/", 1)[-1] if isinstance(uri, str) else None


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _id_of(v):
    """Last URI segment of a {@id: ...} struct or a bare string."""
    if isinstance(v, dict):
        return _last_seg(v.get("@id"))
    return _last_seg(v)


def _label_of(v):
    """label of a {@id, label} struct, else last URI segment, else str."""
    if isinstance(v, dict):
        return v.get("label") or _last_seg(v.get("@id"))
    return v if isinstance(v, str) else None


def _str(v):
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, list):
        return ", ".join(s for s in (_str(x) for x in v) if s) or None
    if isinstance(v, dict):
        return _label_of(v)
    return str(v)


def _to_int(v):
    try:
        return int(v) if v is not None and v != "" else None
    except (ValueError, TypeError):
        return None


def _to_float(v):
    try:
        return float(v) if v is not None and v != "" else None
    except (ValueError, TypeError):
        return None


# --------------------------------------------------------------------------- #
# stations
# --------------------------------------------------------------------------- #

_STATIONS_SCHEMA = pa.schema([
    ("station_guid", pa.string()),
    ("name", pa.string()),
    ("notation", pa.string()),
    ("wiski_id", pa.string()),
    ("river_name", pa.string()),
    ("easting", pa.int64()),
    ("northing", pa.int64()),
    ("lat", pa.float64()),
    ("long", pa.float64()),
    ("date_opened", pa.string()),
    ("status", pa.string()),
    ("observed_properties", pa.string()),
    ("n_measures", pa.int64()),
])


def fetch_stations(node_id: str) -> None:
    asset = node_id
    items = _get_json("id/stations.json", _limit=1_000_000).get("items", [])
    rows = []
    for s in items:
        status = _as_list(s.get("status"))
        rows.append({
            "station_guid": _str(s.get("stationGuid") or s.get("notation")),
            "name": _str(s.get("label")),
            "notation": _str(s.get("notation")),
            "wiski_id": _str(s.get("wiskiID")),
            "river_name": _str(s.get("riverName")),
            "easting": _to_int(s.get("easting")),
            "northing": _to_int(s.get("northing")),
            "lat": _to_float(s.get("lat")),
            "long": _to_float(s.get("long")),
            "date_opened": _str(s.get("dateOpened")),
            "status": ", ".join(x for x in (_label_of(v) for v in status) if x) or None,
            "observed_properties": ", ".join(
                x for x in (_id_of(v) for v in _as_list(s.get("observedProperty"))) if x
            ) or None,
            "n_measures": len(_as_list(s.get("measures"))),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# measures
# --------------------------------------------------------------------------- #

_MEASURES_SCHEMA = pa.schema([
    ("measure_id", pa.string()),
    ("name", pa.string()),
    ("parameter", pa.string()),
    ("parameter_name", pa.string()),
    ("period", pa.int64()),
    ("period_name", pa.string()),
    ("value_type", pa.string()),
    ("value_statistic", pa.string()),
    ("observation_type", pa.string()),
    ("observed_property", pa.string()),
    ("observed_property_label", pa.string()),
    ("station_guid", pa.string()),
    ("station_label", pa.string()),
    ("unit", pa.string()),
    ("unit_name", pa.string()),
])


def fetch_measures(node_id: str) -> None:
    asset = node_id
    items = _get_json("id/measures.json", _limit=2_000_000).get("items", [])
    rows = []
    for m in items:
        station = m.get("station") if isinstance(m.get("station"), dict) else {}
        rows.append({
            "measure_id": _str(m.get("notation")),
            "name": _str(m.get("label")),
            "parameter": _str(m.get("parameter")),
            "parameter_name": _str(m.get("parameterName")),
            "period": _to_int(m.get("period")),
            "period_name": _str(m.get("periodName")),
            "value_type": _str(m.get("valueType")),
            "value_statistic": _label_of(m.get("valueStatistic")),
            "observation_type": _label_of(m.get("observationType")),
            "observed_property": _id_of(m.get("observedProperty")),
            "observed_property_label": _label_of(m.get("observedProperty")),
            "station_guid": _last_seg(station.get("@id")) if station else None,
            "station_label": _str(station.get("label")) if station else None,
            "unit": _id_of(m.get("unit")),
            "unit_name": _str(m.get("unitName")),
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_MEASURES_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# readings
# --------------------------------------------------------------------------- #

_READINGS_SCHEMA = pa.schema([
    ("measure_id", pa.string()),
    ("station_guid", pa.string()),
    ("date", pa.string()),
    ("value", pa.float64()),
    ("completeness", pa.string()),
    ("quality", pa.string()),
])

_GUID_LEN = 36  # measure notation is "<station_guid>-<parameter>-..."


def _date_chunks(start: _dt.date, end: _dt.date, step_days: int):
    cur = start
    while cur <= end:
        chunk_end = min(cur + _dt.timedelta(days=step_days - 1), end)
        yield cur, chunk_end
        cur = chunk_end + _dt.timedelta(days=1)


def _parse_readings_csv(text: str) -> list[dict]:
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        mid = _last_seg(r.get("measure"))
        rows.append({
            "measure_id": mid,
            "station_guid": mid[:_GUID_LEN] if mid and len(mid) > _GUID_LEN else None,
            "date": r.get("date") or None,
            "value": _to_float(r.get("value")),
            "completeness": r.get("completeness") or None,
            "quality": r.get("quality") or None,
        })
    return rows


def fetch_readings(node_id: str) -> None:
    asset = node_id
    today = _dt.date.today()
    start = today - _dt.timedelta(days=READINGS_WINDOW_DAYS)
    total = 0
    with raw_parquet_writer(asset, _READINGS_SCHEMA) as writer:
        for chunk_start, chunk_end in _date_chunks(start, today, READINGS_CHUNK_DAYS):
            text = _get_csv_text(
                "data/readings.csv",
                period=READINGS_PERIOD,
                **{"mineq-date": chunk_start.isoformat(),
                   "maxeq-date": chunk_end.isoformat()},
                _limit=5_000_000,
            )
            rows = _parse_readings_csv(text)
            if not rows:
                continue
            writer.write_table(pa.Table.from_pylist(rows, schema=_READINGS_SCHEMA))
            total += len(rows)
    print(f"  -> {asset}: {total} daily readings over {READINGS_WINDOW_DAYS}d")


DOWNLOAD_SPECS = [
    NodeSpec(id="environment-agency-stations", fn=fetch_stations, kind="download"),
    NodeSpec(id="environment-agency-measures", fn=fetch_measures, kind="download"),
    NodeSpec(id="environment-agency-readings", fn=fetch_readings, kind="download"),
]
