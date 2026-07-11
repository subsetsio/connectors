"""National Bank of Slovakia — download nodes.

Six datasets across three unauthenticated access surfaces:

  * MEDB Macroeconomic Database — the core statistical corpus (~4,369 series):
      - `medb-series`  : series catalog + taxonomy, from the public
                          Elasticsearch proxy (nbs.sk/elastic/medb_*).
      - `medb-values`  : long-format observations melted from the single ~71 MB
                          bulk XLSX dump (M/Q/A "Level" sheets).
  * Exchange rates:
      - `exchange-rate-foreign-monthly` : NBS's own "selected foreign currencies"
                          monthly XML (~150 exotic currencies the ECB does not
                          quote daily), restricted to the euro era (2009+) so
                          every rate is EUR-based (NBS's pre-2009 exports are
                          SKK-based). Written as year fragments so a steady-state
                          refresh only re-pulls the current year.
  * DSW supervised-entity reporting — one cp1250 ZIP of three CSVs:
      - `dsw-report-data`, `dsw-subject-history`, `dsw-subject-union`.

WAF note: nbs.sk fronts a burst-throttling WAF that 403s cloud IPs above
~125 req/min (observed in a prior cloud run). The per-date daily reference-rate
feed (~4,700 requests) was deferred at the accept stage for that reason; the
surfaces used here are all low-request (bulk downloads + ~210 paced monthly
docs), and the monthly walk is paced + browser-UA'd to stay well under the
ceiling.
"""
from __future__ import annotations

import datetime as _dt
import time

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    post,
    configure_http,
    transient_retry,
    save_raw_parquet,
    list_raw_fragments,
)
from utils import (
    melt_level_sheet,
    parse_dsw_report,
    parse_dsw_generic,
    parse_fx_foreign_xml,
)

SLUG = "national-bank-of-slovakia"
FX_START_YEAR = 2009  # Slovakia adopted the euro 2009-01-01; rates are EUR-based from then.

# Browser-like UA + gentle inter-request spacing keep the paced monthly walk
# well under the WAF's ~125 req/min burst ceiling (see module docstring).
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_FX_DELAY_S = 6.0  # ~10 req/min — the rate a prior cloud run confirmed the WAF sustains


def _now_utc() -> _dt.datetime:
    return _dt.datetime.now(tz=_dt.timezone.utc)


# ---------------------------------------------------------------------------
# MEDB — series catalog (Elasticsearch proxy)
# ---------------------------------------------------------------------------
_ELASTIC = "https://nbs.sk/elastic"


@transient_retry()
def _es_all(index: str) -> list[dict]:
    """Fetch every document of a medb_* index via from/size paging."""
    out: list[dict] = []
    frm, size = 0, 5000
    while True:
        resp = post(f"{_ELASTIC}/{index}/_search",
                    json={"size": size, "from": frm}, timeout=(10.0, 120.0))
        resp.raise_for_status()
        hits = resp.json()["hits"]["hits"]
        out.extend(h["_source"] for h in hits)
        if len(hits) < size:
            break
        frm += size
        if frm >= 100000:  # safety ceiling — the DB is ~4.4k docs
            raise RuntimeError(f"{index}: paging exceeded 100000 docs")
    return out


_SERIES_SCHEMA = pa.schema([
    ("timeseries_id", pa.string()),
    ("name_en", pa.string()),
    ("name_sk", pa.string()),
    ("detail", pa.string()),
    ("source", pa.string()),
    ("subarea_id", pa.string()),
    ("subarea_en", pa.string()),
    ("area_id", pa.string()),
    ("area_en", pa.string()),
    ("macrosector_id", pa.string()),
    ("macrosector_en", pa.string()),
])


def fetch_medb_series(node_id: str) -> None:
    macrosectors = {d["macroSectorId"]: d for d in _es_all("medb_macrosectors")}
    areas = {d["areaId"]: d for d in _es_all("medb_areas")}
    subareas = {d["subAreaId"]: d for d in _es_all("medb_subareas")}
    series = _es_all("medb_timeseries")

    rows = []
    for s in series:
        sub = subareas.get(s.get("subAreaId"), {})
        area = areas.get(sub.get("areaId"), {})
        ms = macrosectors.get(area.get("macroSectorId"), {})
        rows.append({
            "timeseries_id": s.get("timeSeriesId"),
            "name_en": s.get("nameEn"),
            "name_sk": s.get("nameSk"),
            "detail": s.get("detail"),
            "source": s.get("source"),
            "subarea_id": s.get("subAreaId"),
            "subarea_en": sub.get("nameEn"),
            "area_id": sub.get("areaId"),
            "area_en": area.get("nameEn"),
            "macrosector_id": area.get("macroSectorId"),
            "macrosector_en": ms.get("nameEn"),
        })
    table = pa.Table.from_pylist(rows, schema=_SERIES_SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------------------
# MEDB — values (bulk XLSX melt, written as per-frequency fragments)
# ---------------------------------------------------------------------------
_MEDB_XLSX = "https://nbs.sk/wp-json/nbs/v1/medb/download"

_VALUES_SCHEMA = pa.schema([
    ("frequency", pa.string()),
    ("series_key", pa.string()),
    ("classcode", pa.string()),
    ("variable", pa.string()),
    ("detail", pa.string()),
    ("source", pa.string()),
    ("period_label", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
])


@transient_retry()
def _download_medb_xlsx() -> bytes:
    resp = get(_MEDB_XLSX, timeout=(30.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_medb_values(node_id: str) -> None:
    import io
    import openpyxl

    content = _download_medb_xlsx()
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    total = 0
    try:
        for sheet, freq in (("M Level", "M"), ("Q Level", "Q"), ("A Level", "A")):
            rows = melt_level_sheet(wb[sheet], freq)
            if not rows:
                raise RuntimeError(f"MEDB {freq}: melt produced 0 rows")
            table = pa.Table.from_pylist(rows, schema=_VALUES_SCHEMA)
            save_raw_parquet(table, node_id, fragment=freq)
            total += len(rows)
    finally:
        wb.close()
    if total == 0:
        raise RuntimeError("MEDB values: no observations parsed")


# ---------------------------------------------------------------------------
# Exchange rates — selected foreign currencies (monthly XML, year fragments)
# ---------------------------------------------------------------------------
_FX_FOREIGN = "https://nbs.sk/export/en/exchange-rate-foreign/{month}/xml"

_FX_FOREIGN_SCHEMA = pa.schema([
    ("valid_from", pa.date32()),
    ("month_number", pa.int32()),
    ("country", pa.string()),
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _fetch_fx_foreign_month(year: int, month: int) -> list[dict]:
    resp = get(_FX_FOREIGN.format(month=f"{year}-{month:02d}"), timeout=(10.0, 60.0))
    resp.raise_for_status()
    return parse_fx_foreign_xml(resp.content)


def fetch_exchange_rate_foreign_monthly(node_id: str) -> None:
    configure_http(headers={"User-Agent": _USER_AGENT})
    now = _now_utc()
    current_year = now.year
    done = set(list_raw_fragments(node_id, "parquet").keys())

    for year in range(FX_START_YEAR, current_year + 1):
        # Past years are immutable once fetched — skip if a fragment exists.
        if year < current_year and str(year) in done:
            continue
        last_month = 12 if year < current_year else now.month
        rows: list[dict] = []
        for month in range(1, last_month + 1):
            rows.extend(_fetch_fx_foreign_month(year, month))
            time.sleep(_FX_DELAY_S)
        if rows:
            table = pa.Table.from_pylist(rows, schema=_FX_FOREIGN_SCHEMA)
            save_raw_parquet(table, node_id, fragment=str(year))


# ---------------------------------------------------------------------------
# DSW — supervised financial entity reporting (one ZIP of three cp1250 CSVs)
# ---------------------------------------------------------------------------
_DSW_ZIP = "https://nbs.sk/wp-json/nbs/v1/dsw/download"


@transient_retry()
def _download_dsw_zip() -> bytes:
    resp = get(_DSW_ZIP, timeout=(30.0, 300.0))
    resp.raise_for_status()
    return resp.content


_DSW_REPORT_SCHEMA = pa.schema([
    ("period", pa.date32()),
    ("subject_code", pa.string()),
    ("val_type", pa.string()),
    ("currency", pa.string()),
    ("num_value", pa.float64()),
    ("subject_name_act", pa.string()),
    ("subject_name_hist", pa.string()),
    ("deputy_subject_code", pa.string()),
    ("deputy_subject_name", pa.string()),
    ("grp_name", pa.string()),
    ("grp_parent_name", pa.string()),
])

_DSW_HISTORY_COLS = [
    "deputy_subject_code", "deputy_subject_name", "subject_code",
    "subject_name_act", "subject_name_hist", "name_from", "name_till",
    "valid_from", "valid_till", "grp_parent_name", "grp_name",
    "in_grp_from", "in_grp_till",
]
_DSW_UNION_COLS = [
    "subject_code", "successor_subject_code", "union_date",
    "subject_name_act", "subject_name_hist", "succ_subject_name_act",
    "succ_subject_name_hist", "deputy_subject_name", "succ_deputy_subject_name",
    "grp_parent_name", "grp_name",
]


def fetch_dsw_report_data(node_id: str) -> None:
    rows = parse_dsw_report(_download_dsw_zip())
    if not rows:
        raise RuntimeError("DSW report: 0 rows parsed")
    table = pa.Table.from_pylist(rows, schema=_DSW_REPORT_SCHEMA)
    save_raw_parquet(table, node_id)


def _dsw_reference(node_id: str, member: str, cols: list[str]) -> None:
    rows = parse_dsw_generic(_download_dsw_zip(), member)
    schema = pa.schema([(c, pa.string()) for c in cols])
    norm = [{c: r.get(c) for c in cols} for r in rows]
    table = pa.Table.from_pylist(norm, schema=schema)
    save_raw_parquet(table, node_id)


def fetch_dsw_subject_history(node_id: str) -> None:
    _dsw_reference(node_id, "dsw_subject_history.csv", _DSW_HISTORY_COLS)


def fetch_dsw_subject_union(node_id: str) -> None:
    _dsw_reference(node_id, "dsw_subject_union.csv", _DSW_UNION_COLS)


# ---------------------------------------------------------------------------
# Specs — one per accepted collect entity (exchange-rate-daily deferred)
# ---------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-medb-series", fn=fetch_medb_series, kind="download"),
    NodeSpec(id=f"{SLUG}-medb-values", fn=fetch_medb_values, kind="download"),
    NodeSpec(id=f"{SLUG}-exchange-rate-foreign-monthly",
             fn=fetch_exchange_rate_foreign_monthly, kind="download"),
    NodeSpec(id=f"{SLUG}-dsw-report-data", fn=fetch_dsw_report_data, kind="download"),
    NodeSpec(id=f"{SLUG}-dsw-subject-history", fn=fetch_dsw_subject_history, kind="download"),
    NodeSpec(id=f"{SLUG}-dsw-subject-union", fn=fetch_dsw_subject_union, kind="download"),
]
