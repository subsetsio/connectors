"""Colorado Avalanche Information Center (CAIC) avalanche accidents connector.

Two genuinely distinct record-level tables, per research + rank:

  - us-avalanche-fatalities  -- the canonical comprehensive table. A single
    curator-maintained Google-Drive .xlsx workbook; its first sheet 'Data' is
    one row per fatal US avalanche accident, 1951-present, all states. The
    workbook's other 7 sheets are QUERY/pivot-derived aggregates of 'Data' and
    are deliberately ignored. Parsed with openpyxl(data_only=True): columns
    YYYY/MM/DD are =YEAR/MONTH/DAY formulas whose cached values are present in
    the export, but they are redundant with the Date column so we drop them.

  - colorado-accident-detail -- the Accident Explorer Apps-Script feed. JSON
    {debugInfo, data:[...]} covering a rolling recent window (~5 avalanche
    years) of Colorado accidents with a richer per-accident schema (avalanche
    type, aspect, elevation, slope, trigger, R/D size scales, numbers
    caught/buried/killed). Narrower than the flagship but carries detail it
    lacks.

Both sources are tiny (<200KB) with no incremental query support, so each is a
stateless full re-pull every run; revisions are picked up for free.
"""

import io
from datetime import date, datetime

import openpyxl
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

XLSX_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1k6Q7_i6GFGeiHwIl-ai7ghS4_K8-7kQ1/export?format=xlsx"
)
GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyZPqzls-14RINmRDddhRwoSW4DylOPrVybRky82qxL5fm7p_QVmZKuQFbBwN6oBdF9aw/"
    "exec?path=Sheet1&action=read"
)

FATALITIES_ID = "caic-avalanche-accidents-us-avalanche-fatalities"
DETAIL_ID = "caic-avalanche-accidents-colorado-accident-detail"

# Source spreadsheet header -> our raw column name. Formula helper columns
# YYYY/MM/DD are intentionally omitted (redundant with Date).
_FATALITY_COLUMNS = {
    "AvyYear": "avy_year",
    "Date": "date",
    "Location": "location",
    "Setting": "setting",
    "State": "state",
    "lat": "lat",
    "lon": "lon",
    "PrimaryActivity": "primary_activity",
    "TravelMode": "travel_mode",
    "Killed": "killed",
    "Description": "description",
}

_FATALITY_SCHEMA = pa.schema([
    ("avy_year", pa.int64()),
    ("date", pa.date32()),
    ("location", pa.string()),
    ("setting", pa.string()),
    ("state", pa.string()),
    ("lat", pa.float64()),
    ("lon", pa.float64()),
    ("primary_activity", pa.string()),
    ("travel_mode", pa.string()),
    ("killed", pa.int64()),
    ("description", pa.string()),
])

_DETAIL_SCHEMA = pa.schema([
    ("acc_id", pa.string()),
    ("acc_date", pa.date32()),
    ("acc_activity", pa.string()),
    ("travel_mode", pa.string()),
    ("acc_location", pa.string()),
    ("acc_lat", pa.float64()),
    ("acc_lon", pa.float64()),
    ("acc_no_caught", pa.int64()),
    ("acc_no_buried", pa.int64()),
    ("acc_no_killed", pa.int64()),
    ("atype", pa.string()),
    ("aspect", pa.string()),
    ("elevation", pa.float64()),
    ("slope", pa.float64()),
    ("rscale", pa.float64()),
    ("dscale", pa.float64()),
    ("trigger", pa.string()),
    ("trig_desc", pa.string()),
    ("surface", pa.string()),
    ("report", pa.string()),
])

# Safety ceiling: the workbook holds ~1016 rows and grows slowly. A row count
# far past this signals a contract change (wrong sheet, merged feed) — raise.
_MAX_FATALITY_ROWS = 50000


def _to_int(v):
    if v is None or v == "":
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _to_str(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _to_date(v):
    """Coerce a cell/JSON value to a date. Handles datetime objects (openpyxl)
    and ISO date/datetime strings ('2025-02-22T08:00:00.000Z')."""
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v)
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _fetch_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_fatalities(node_id: str) -> None:
    raw = _fetch_bytes(XLSX_URL)
    wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    ws = wb["Data"]
    it = ws.iter_rows(values_only=True)
    header = list(next(it))
    # Map our wanted columns to their position in the source header.
    idx = {src: header.index(src) for src in _FATALITY_COLUMNS if src in header}
    missing = set(_FATALITY_COLUMNS) - set(idx)
    if missing:
        raise RuntimeError(f"{node_id}: 'Data' sheet missing columns: {sorted(missing)}")

    width = len(header)
    rows = []
    for row in it:
        # read_only mode trims trailing empty cells, yielding ragged rows.
        row = list(row)
        if len(row) < width:
            row += [None] * (width - len(row))
        d = _to_date(row[idx["Date"]])
        if d is None:
            continue  # trailing/blank rows
        rows.append({
            "avy_year": _to_int(row[idx["AvyYear"]]),
            "date": d,
            "location": _to_str(row[idx["Location"]]),
            "setting": _to_str(row[idx["Setting"]]),
            "state": _to_str(row[idx["State"]]),
            "lat": _to_float(row[idx["lat"]]),
            "lon": _to_float(row[idx["lon"]]),
            "primary_activity": _to_str(row[idx["PrimaryActivity"]]),
            "travel_mode": _to_str(row[idx["TravelMode"]]),
            "killed": _to_int(row[idx["Killed"]]),
            "description": _to_str(row[idx["Description"]]),
        })
        if len(rows) > _MAX_FATALITY_ROWS:
            raise RuntimeError(
                f"{node_id}: exceeded {_MAX_FATALITY_ROWS} rows — source grew "
                "past expectations or the wrong sheet was parsed"
            )

    table = pa.Table.from_pylist(rows, schema=_FATALITY_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_detail(node_id: str) -> None:
    payload = _fetch_json(GAS_URL)
    data = payload.get("data", [])
    rows = []
    for r in data:
        rows.append({
            "acc_id": _to_str(r.get("acc_id")),
            "acc_date": _to_date(r.get("acc_date")),
            "acc_activity": _to_str(r.get("acc_activity")),
            "travel_mode": _to_str(r.get("travel_mode")),
            "acc_location": _to_str(r.get("acc_location")),
            "acc_lat": _to_float(r.get("acc_lat")),
            "acc_lon": _to_float(r.get("acc_lon")),
            "acc_no_caught": _to_int(r.get("acc_no_caught")),
            "acc_no_buried": _to_int(r.get("acc_no_buried")),
            "acc_no_killed": _to_int(r.get("acc_no_killed")),
            "atype": _to_str(r.get("atype")),
            "aspect": _to_str(r.get("aspect")),
            "elevation": _to_float(r.get("elevation")),
            "slope": _to_float(r.get("slope")),
            "rscale": _to_float(r.get("Rscale")),
            "dscale": _to_float(r.get("Dscale")),
            "trigger": _to_str(r.get("trigger")),
            "trig_desc": _to_str(r.get("trigDesc")),
            "surface": _to_str(r.get("surface")),
            "report": _to_str(r.get("report")),
        })
    table = pa.Table.from_pylist(rows, schema=_DETAIL_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=FATALITIES_ID, fn=fetch_fatalities, kind="download"),
    NodeSpec(id=DETAIL_ID, fn=fetch_detail, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=FATALITIES_ID + "-transform",
        deps=[FATALITIES_ID],
        sql=f'''
            SELECT
                CAST(avy_year AS INTEGER)              AS avalanche_year,
                date                                   AS accident_date,
                EXTRACT(year FROM date)::INTEGER       AS year,
                EXTRACT(month FROM date)::INTEGER       AS month,
                location,
                setting,
                state,
                CASE WHEN lat = 0 AND lon = 0 THEN NULL ELSE lat END AS latitude,
                CASE WHEN lat = 0 AND lon = 0 THEN NULL ELSE lon END AS longitude,
                primary_activity,
                travel_mode,
                CAST(killed AS INTEGER)                AS killed,
                description
            FROM "{FATALITIES_ID}"
            WHERE date IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=DETAIL_ID + "-transform",
        deps=[DETAIL_ID],
        sql=f'''
            SELECT
                acc_id,
                acc_date                               AS accident_date,
                EXTRACT(year FROM acc_date)::INTEGER   AS year,
                acc_activity                           AS activity,
                travel_mode,
                acc_location                           AS location,
                acc_lat                                AS latitude,
                acc_lon                                AS longitude,
                CAST(acc_no_caught AS INTEGER)         AS number_caught,
                CAST(acc_no_buried AS INTEGER)         AS number_buried,
                CAST(acc_no_killed AS INTEGER)         AS number_killed,
                atype                                  AS avalanche_type,
                aspect,
                elevation                              AS elevation_ft,
                slope                                  AS slope_angle,
                rscale                                 AS relative_size,
                dscale                                 AS destructive_size,
                trigger,
                trig_desc                              AS trigger_description,
                surface                                AS bed_surface,
                report                                 AS report_url
            FROM "{DETAIL_ID}"
            WHERE acc_date IS NOT NULL
        ''',
    ),
]
