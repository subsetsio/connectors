"""India-WRIS connector.

India-WRIS (National Water Informatics Centre) exposes water-resources
observations through one REST endpoint per dashboard THEME:

    POST https://indiawris.gov.in/Dataset/<Module Name>
        ?agencyName=&stateName=&districtName=&startdate=&enddate=
        &download=false&page=&size=

filtered by (agency, state, district) over a date window, returning
{statusCode, message, data: [ ...observation rows... ]}. We build a whole-theme
snapshot by enumerating states from the master endpoint and pulling every
state's full history, paginated, writing one ndjson batch per state (the data
is too large per theme to hold in one file). The reference `stations` entity is
the station registry, assembled from the station-master endpoints.

Geography is discovered live (never hardcoded); the date window runs from a
conservative SOURCE_MIN_DATE floor to today. Per the firehose pattern the fetch
fn writes raw + state per state batch and resumes from a per-state watermark.

NOTE: the API host (indiawris.gov.in) was unreachable from the authoring
sandbox, so field-name mapping below is defensive (multiple candidate keys per
canonical field) and reconciled against the live cloud run + the tests/ specs.
"""

import json
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    transient_retry,
    save_raw_ndjson,
    load_state,
    save_state,
)
from constants import THEMES, STATION_DATASETS, SOURCE_MIN_DATE

BASE = "https://indiawris.gov.in"
HEADERS = {"accept": "application/json", "Referer": "https://indiawris.gov.in/"}
PAGE_SIZE = 1000
MAX_PAGES = 5000          # safety ceiling per (state, agency); raises if hit
STATE_VERSION = 1


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _post_json(url, *, params=None, body=None):
    resp = post(url, params=params, json=body if body is not None else {},
                headers=HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_json(url, *, params=None):
    resp = get(url, params=params, headers=HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _rows(payload):
    """Pull the row list out of a WRIS response envelope."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        d = payload.get("data")
        if isinstance(d, list):
            return d
    return []


def _g(row, *keys):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return None


def _f(v):
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _s(v):
    if v is None:
        return None
    return str(v).strip() or None


def _slug(name):
    out = "".join(c.lower() if c.isalnum() else "-" for c in str(name))
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-") or "unknown"


# --------------------------------------------------------------------------- #
# Master lookups
# --------------------------------------------------------------------------- #
def _list_states():
    """Return list of state name strings from the master endpoint."""
    payload = _post_json(f"{BASE}/masterState/StateList")
    out = []
    for r in _rows(payload):
        if isinstance(r, str):
            out.append(r)
        elif isinstance(r, dict):
            name = _g(r, "stateName", "state_name", "state", "name", "value", "label")
            if name:
                out.append(str(name))
    # de-dup, keep order
    seen, uniq = set(), []
    for s in out:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq


def _canon_obs(row, theme, state, agency):
    """Normalize one observation row to a stable canonical schema. The full
    original row is preserved as a JSON string in `record`."""
    return {
        "theme": theme,
        "station_code": _s(_g(row, "stationCode", "station_code", "stationcode", "code", "id")),
        "station_name": _s(_g(row, "stationName", "station_name", "stationname", "name")),
        "latitude": _f(_g(row, "latitude", "lat")),
        "longitude": _f(_g(row, "longitude", "long", "lon", "lng")),
        "state": _s(_g(row, "state", "stateName", "state_name") or state),
        "district": _s(_g(row, "district", "districtName", "district_name")),
        "agency": _s(_g(row, "agencyName", "agency", "agency_name") or agency),
        "observed_date": _s(_g(row, "dataTime", "date", "datetime", "dataDate",
                               "obsDate", "observationDate", "time")),
        "parameter": _s(_g(row, "parameter", "parameterName", "wqParameter", "param")),
        "value": _f(_g(row, "dataValue", "value", "data_value", "rainfall",
                       "level", "discharge", "storage", "reading")),
        "unit": _s(_g(row, "unit", "units", "uom")),
        "record": json.dumps(row, default=str, ensure_ascii=False),
    }


def _fetch_filter_rows(module, *, state, agency, startdate, enddate):
    """All rows for one (module, state, agency) over a date window, paginated."""
    rows = []
    for page in range(MAX_PAGES):
        params = {
            "agencyName": agency,
            "stateName": state,
            "districtName": "",
            "startdate": startdate,
            "enddate": enddate,
            "download": "false",
            "page": str(page),
            "size": str(PAGE_SIZE),
        }
        payload = _post_json(f"{BASE}/Dataset/{module}", params=params)
        batch = _rows(payload)
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
    else:
        raise RuntimeError(
            f"MAX_PAGES={MAX_PAGES} hit for module={module!r} state={state!r} "
            f"agency={agency!r} — source grew past safety ceiling; raise the cap "
            f"or narrow the window."
        )
    return rows


# --------------------------------------------------------------------------- #
# Theme fetcher (one spec per observation theme)
# --------------------------------------------------------------------------- #
def fetch_theme(node_id: str) -> None:
    theme = node_id[len("india-wris-"):]
    cfg = THEMES[theme]
    module = cfg["module"]
    agencies = cfg["agencies"]

    state_key = node_id
    state = load_state(state_key)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "done_states": []}
    done = set(state.get("done_states", []))

    enddate = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    states = _list_states()
    if not states:
        raise RuntimeError(f"{node_id}: masterState returned no states")

    for st in states:
        if st in done:
            continue
        canon = []
        for agency in agencies:
            raw = _fetch_filter_rows(
                module, state=st, agency=agency,
                startdate=SOURCE_MIN_DATE, enddate=enddate,
            )
            for r in raw:
                canon.append(_canon_obs(r, theme, st, agency))
        # Write raw FIRST (one batch per state), then advance state.
        if canon:
            save_raw_ndjson(canon, f"{node_id}-{_slug(st)}")
        done.add(st)
        save_state(state_key, {
            "schema_version": STATE_VERSION,
            "done_states": sorted(done),
        })


# --------------------------------------------------------------------------- #
# Stations reference fetcher
# --------------------------------------------------------------------------- #
def _canon_station(row, dataset, agency):
    return {
        "dataset": dataset,
        "agency": _s(_g(row, "agency", "agencyName", "agency_name") or agency),
        "station_code": _s(_g(row, "stationCode", "station_code", "station_Code",
                              "stationcode", "code")),
        "station_name": _s(_g(row, "stationName", "station_Name", "station_name", "name")),
        "state": _s(_g(row, "state", "stateName", "state_name")),
        "district": _s(_g(row, "district", "districtName", "district_name")),
        "latitude": _f(_g(row, "latitude", "lat")),
        "longitude": _f(_g(row, "longitude", "long", "lon", "lng")),
        "data_available_from": _s(_g(row, "data_available_from", "dataAvailableFrom",
                                     "availableFrom", "startDate")),
        "data_available_till": _s(_g(row, "data_available_Till", "data_available_till",
                                     "dataAvailableTill", "availableTill", "endDate")),
        "record": json.dumps(row, default=str, ensure_ascii=False),
    }


def fetch_stations(node_id: str) -> None:
    asset = node_id
    out = []
    for datasetcode, agency in STATION_DATASETS:
        payload = _post_json(
            f"{BASE}/masterStationDS/stationDSList",
            body={"datasetcode": datasetcode, "agencyid": agency, "AgencyCode": agency},
        )
        for r in _rows(payload):
            if isinstance(r, dict):
                out.append(_canon_station(r, datasetcode, agency))
    if not out:
        raise RuntimeError(f"{node_id}: no stations returned across station datasets")
    save_raw_ndjson(out, asset)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id=f"india-wris-{theme}", fn=fetch_theme, kind="download")
    for theme in THEMES
] + [
    NodeSpec(id="india-wris-stations", fn=fetch_stations, kind="download"),
]


# Thin parse-and-type pass. observed_date formats vary across themes, so we
# TRY_CAST to a date (null on failure) rather than hard-cast. A row is kept if
# it carries either a numeric value or a named parameter.
def _obs_sql(download_id: str) -> str:
    return f'''
        SELECT
            theme,
            station_code,
            station_name,
            CAST(latitude  AS DOUBLE) AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            state,
            district,
            agency,
            observed_date,
            TRY_CAST(observed_date AS DATE) AS observed_on,
            parameter,
            CAST(value AS DOUBLE) AS value,
            unit
        FROM "{download_id}"
        WHERE value IS NOT NULL OR parameter IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"india-wris-{theme}-transform",
        deps=[f"india-wris-{theme}"],
        sql=_obs_sql(f"india-wris-{theme}"),
    )
    for theme in THEMES
] + [
    SqlNodeSpec(
        id="india-wris-stations-transform",
        deps=["india-wris-stations"],
        sql='''
            SELECT
                station_code,
                station_name,
                dataset,
                agency,
                state,
                district,
                CAST(latitude  AS DOUBLE) AS latitude,
                CAST(longitude AS DOUBLE) AS longitude,
                data_available_from,
                data_available_till
            FROM "india-wris-stations"
            WHERE station_code IS NOT NULL
        ''',
    ),
]
