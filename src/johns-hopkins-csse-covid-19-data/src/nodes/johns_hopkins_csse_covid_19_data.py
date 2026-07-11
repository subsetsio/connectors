"""Johns Hopkins CSSE COVID-19 Data connector.

Source: the archived (read-only since 2023-03-10) CSSEGISandData/COVID-19 GitHub
repo. Every path and byte is permanently frozen, so this is a stateless full
re-pull each run — there is no incremental filter and the corpus never changes.

Four subsets, each fetched via the stable raw.githubusercontent.com CSV URLs:

  * time_series_global   — the three global wide CSVs (confirmed/deaths/recovered),
                           melted to long (metric is a column value).
  * time_series_us       — the two US county-level wide CSVs (confirmed/deaths),
                           melted to long.
  * daily_reports_global — per-day global snapshot CSVs concatenated; headers
                           drifted over the pandemic so columns are normalized to
                           a canonical set before writing.
  * daily_reports_us     — per-day US state-level snapshot CSVs concatenated,
                           likewise header-normalized.
  * lookup_table         — UID/ISO/FIPS geography reference table.

The wide time-series files are melted row-by-row (streaming) so memory stays
bounded; the daily reports are ~1100 small files each, fetched sequentially and
streamed to a single ndjson.gz. All raw is line-delimited JSON (the daily-report
header drift makes a fixed parquet schema brittle); the SQL transforms re-type.
"""

import csv
import io
import json
from datetime import date, timedelta

from subsets_utils import NodeSpec, get, raw_writer, transient_retry

BASE = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"

SLUG = "johns-hopkins-csse-covid-19-data"


@transient_retry()
def _get_text(url: str) -> str | None:
    """Fetch a CSV as text. Returns None on a 404 (missing daily file); raises on
    any other permanent/transient HTTP error (transient ones are retried first)."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.text


def _iso_from_ts_header(h: str) -> str:
    """'1/22/20' -> '2020-01-22' (JHU time-series date column header)."""
    m, d, y = h.strip().split("/")
    return f"20{int(y):02d}-{int(m):02d}-{int(d):02d}"


def _daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


# ---------------------------------------------------------------------------
# Time series — wide CSVs melted to long
# ---------------------------------------------------------------------------

_GLOBAL_TS = [
    ("confirmed", "time_series_covid19_confirmed_global.csv"),
    ("deaths", "time_series_covid19_deaths_global.csv"),
    ("recovered", "time_series_covid19_recovered_global.csv"),
]

# (metric, filename, index where date columns begin). The deaths file inserts a
# Population column at index 11, so its dates start one column later.
_US_TS = [
    ("confirmed", "time_series_covid19_confirmed_US.csv", 11),
    ("deaths", "time_series_covid19_deaths_US.csv", 12),
]


def fetch_time_series_global(node_id: str) -> None:
    asset = node_id
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for metric, fname in _GLOBAL_TS:
            text = _get_text(f"{BASE}/csse_covid_19_time_series/{fname}")
            if text is None:
                raise RuntimeError(f"expected time-series file missing: {fname}")
            reader = csv.reader(io.StringIO(text))
            header = next(reader)
            # header: Province/State, Country/Region, Lat, Long, <dates...>
            date_iso = [_iso_from_ts_header(h) for h in header[4:]]
            for row in reader:
                province, country, lat, long = row[0], row[1], row[2], row[3]
                for i, v in enumerate(row[4:]):
                    if v == "":
                        continue
                    out.write(json.dumps({
                        "country_region": country or None,
                        "province_state": province or None,
                        "lat": lat or None,
                        "long": long or None,
                        "date": date_iso[i],
                        "metric": metric,
                        "value": v,
                    }) + "\n")


def fetch_time_series_us(node_id: str) -> None:
    asset = node_id
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for metric, fname, dstart in _US_TS:
            text = _get_text(f"{BASE}/csse_covid_19_time_series/{fname}")
            if text is None:
                raise RuntimeError(f"expected time-series file missing: {fname}")
            reader = csv.reader(io.StringIO(text))
            header = next(reader)
            # header: UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,
            #         Lat,Long_,Combined_Key,[Population],<dates...>
            date_iso = [_iso_from_ts_header(h) for h in header[dstart:]]
            for row in reader:
                population = row[11] if metric == "deaths" else ""
                for i, v in enumerate(row[dstart:]):
                    if v == "":
                        continue
                    out.write(json.dumps({
                        "uid": row[0] or None,
                        "iso2": row[1] or None,
                        "iso3": row[2] or None,
                        "fips": row[4] or None,
                        "admin2": row[5] or None,
                        "province_state": row[6] or None,
                        "combined_key": row[10] or None,
                        "lat": row[8] or None,
                        "long": row[9] or None,
                        "population": population or None,
                        "date": date_iso[i],
                        "metric": metric,
                        "value": v,
                    }) + "\n")


# ---------------------------------------------------------------------------
# Daily reports — per-day snapshot CSVs, header-normalized and concatenated
# ---------------------------------------------------------------------------

# header token (lower-cased, BOM-stripped) -> canonical key
_DAILY_GLOBAL_MAP = {
    "fips": "fips",
    "admin2": "admin2",
    "province/state": "province_state",
    "province_state": "province_state",
    "country/region": "country_region",
    "country_region": "country_region",
    "last update": "last_update",
    "last_update": "last_update",
    "latitude": "lat",
    "lat": "lat",
    "longitude": "long",
    "long_": "long",
    "confirmed": "confirmed",
    "deaths": "deaths",
    "recovered": "recovered",
    "active": "active",
    "combined_key": "combined_key",
    "incidence_rate": "incident_rate",
    "incident_rate": "incident_rate",
    "case-fatality_ratio": "case_fatality_ratio",
    "case_fatality_ratio": "case_fatality_ratio",
}
_DAILY_GLOBAL_KEYS = [
    "report_date", "fips", "admin2", "province_state", "country_region",
    "last_update", "lat", "long", "confirmed", "deaths", "recovered", "active",
    "combined_key", "incident_rate", "case_fatality_ratio",
]

_DAILY_US_MAP = {
    "province_state": "province_state",
    "country_region": "country_region",
    "last_update": "last_update",
    "lat": "lat",
    "long_": "long",
    "confirmed": "confirmed",
    "deaths": "deaths",
    "recovered": "recovered",
    "active": "active",
    "fips": "fips",
    "incidence_rate": "incident_rate",
    "incident_rate": "incident_rate",
    "total_test_results": "total_test_results",
    "people_hospitalized": "people_hospitalized",
    "case-fatality_ratio": "case_fatality_ratio",
    "case_fatality_ratio": "case_fatality_ratio",
    "uid": "uid",
    "iso3": "iso3",
    "testing_rate": "testing_rate",
    "hospitalization_rate": "hospitalization_rate",
    "people_tested": "people_tested",
    "mortality_rate": "mortality_rate",
}
_DAILY_US_KEYS = [
    "report_date", "province_state", "country_region", "last_update", "lat",
    "long", "confirmed", "deaths", "recovered", "active", "fips", "incident_rate",
    "total_test_results", "people_hospitalized", "case_fatality_ratio", "uid",
    "iso3", "testing_rate", "hospitalization_rate", "people_tested",
    "mortality_rate",
]


def _emit_daily(text, colmap, keys, report_iso, out):
    """Parse one daily-report CSV, normalizing drifting headers to `keys`. Every
    record carries all canonical keys (missing -> null) so the ndjson schema is
    stable across the ~1100 files."""
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        return
    header[0] = header[0].lstrip("\ufeff")
    idx_to_key = [colmap.get(h.strip().lower()) for h in header]
    for row in reader:
        rec = dict.fromkeys(keys)
        rec["report_date"] = report_iso
        for i, cell in enumerate(row):
            if i < len(idx_to_key):
                key = idx_to_key[i]
                if key:
                    rec[key] = cell if cell != "" else None
        out.write(json.dumps(rec) + "\n")


def fetch_daily_reports_global(node_id: str) -> None:
    asset = node_id
    start, end = date(2020, 1, 22), date(2023, 3, 9)
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for d in _daterange(start, end):
            fname = d.strftime("%m-%d-%Y")
            text = _get_text(f"{BASE}/csse_covid_19_daily_reports/{fname}.csv")
            if text is None:
                continue
            _emit_daily(text, _DAILY_GLOBAL_MAP, _DAILY_GLOBAL_KEYS, d.isoformat(), out)


def fetch_daily_reports_us(node_id: str) -> None:
    asset = node_id
    start, end = date(2020, 4, 12), date(2023, 3, 9)
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for d in _daterange(start, end):
            fname = d.strftime("%m-%d-%Y")
            text = _get_text(f"{BASE}/csse_covid_19_daily_reports_us/{fname}.csv")
            if text is None:
                continue
            _emit_daily(text, _DAILY_US_MAP, _DAILY_US_KEYS, d.isoformat(), out)


# ---------------------------------------------------------------------------
# Geography lookup
# ---------------------------------------------------------------------------

_LOOKUP_KEYS = [
    "uid", "iso2", "iso3", "code3", "fips", "admin2", "province_state",
    "country_region", "lat", "long", "combined_key", "population",
]

_LOOKUP_MAP = {
    "uid": "uid",
    "iso2": "iso2",
    "iso3": "iso3",
    "code3": "code3",
    "fips": "fips",
    "admin2": "admin2",
    "province_state": "province_state",
    "country_region": "country_region",
    "lat": "lat",
    "long_": "long",
    "combined_key": "combined_key",
    "population": "population",
}


def fetch_lookup_table(node_id: str) -> None:
    text = _get_text(f"{BASE}/UID_ISO_FIPS_LookUp_Table.csv")
    if text is None:
        raise RuntimeError("expected lookup file missing: UID_ISO_FIPS_LookUp_Table.csv")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    header[0] = header[0].lstrip("\ufeff")
    idx_to_key = [_LOOKUP_MAP.get(h.strip().lower()) for h in header]

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for row in reader:
            rec = dict.fromkeys(_LOOKUP_KEYS)
            for i, cell in enumerate(row):
                if i < len(idx_to_key):
                    key = idx_to_key[i]
                    if key:
                        rec[key] = cell if cell != "" else None
            out.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

_TS_GLOBAL = f"{SLUG}-time-series-global"
_TS_US = f"{SLUG}-time-series-us"
_DR_GLOBAL = f"{SLUG}-daily-reports-global"
_DR_US = f"{SLUG}-daily-reports-us"
_LOOKUP = f"{SLUG}-lookup-table"

DOWNLOAD_SPECS = [
    NodeSpec(id=_TS_GLOBAL, fn=fetch_time_series_global, kind="download"),
    NodeSpec(id=_TS_US, fn=fetch_time_series_us, kind="download"),
    NodeSpec(id=_DR_GLOBAL, fn=fetch_daily_reports_global, kind="download"),
    NodeSpec(id=_DR_US, fn=fetch_daily_reports_us, kind="download"),
    NodeSpec(id=_LOOKUP, fn=fetch_lookup_table, kind="download"),
]
