"""Department of Census and Statistics (Sri Lanka) connector.

DCS exposes no PxWeb/SDMX/REST/CKAN catalog API. The only auth-free,
machine-readable surfaces that deliver actual statistical data are the dashboard
PHP endpoints under https://www.statistics.gov.lk/DashBoard/, which return
JS-wrapped JSON (`var name=[...]`). We strip the assignment + BOM and JSON-parse
the array (the Prices arrays use JS empty-string `''` which we sanitise to null).

Fetch shape: stateless full re-pull. Every endpoint returns its whole table in
one small GET (tens-to-hundreds of KB) and there is no incremental/since filter
anywhere, so each run re-fetches the full corpus and the transform overwrites.
No state, no watermark.

Subsets:
  * srilanka_glance  -> one wide-annual subset per dictionary subcategory
                        (alldata.php is the data, SLGlance_Data.php the
                        code->title/units dictionary). Published long-format.
  * EIP/CCPI, EIP/NCPI -> monthly consumer price index (index value + MoM/YoY).
  * EIP/GDP            -> GDP by economic activity, quarterly+annual,
                          constant/current prices, value/share/growth.
  * EIP/PPI, EIP/IIP   -> monthly producer-price / industrial-production index.
  * Prices             -> weekly island-wide retail prices by product.
"""

import json
import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS

PREFIX = "department-of-census-and-statistics-"
BASE = "https://www.statistics.gov.lk/DashBoard/"

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


# --------------------------------------------------------------------------- #
# fetch helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text.lstrip("﻿")


def _js_array(text: str, name: str) -> list:
    """Extract a `name=[ ... ];` JS array literal and JSON-parse it."""
    m = re.search(re.escape(name) + r"\s*=\s*(\[.*?\])\s*;", text, re.S)
    if not m:
        raise ValueError(f"JS array {name!r} not found in payload")
    # JS empty-string literals ('') are not valid JSON -> treat as null.
    return json.loads(m.group(1).replace("''", "null"))


def _num(v):
    """Coerce a dashboard cell to float, or None when blank/non-numeric."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "")
    if s in ("", "-", "NA", "na", "n/a", "null", "NaN", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _eid(node_id: str) -> str:
    return node_id[len(PREFIX):]


def _d_month(s):
    """'Jan-2022' -> '2022-01-01'; bare year '2022' -> '2022-01-01'."""
    if not s:
        return None
    s = str(s).strip()
    if "-" in s:
        mon, _, yr = s.partition("-")
        m = _MONTHS.get(mon.strip().lower()[:3])
        if m and yr.strip().isdigit():
            return f"{int(yr):04d}-{m:02d}-01"
    if s.isdigit():
        return f"{int(s):04d}-01-01"
    return None


def _d_quarter(s):
    """'Q1-2015' -> '2015-01-01'."""
    if not s:
        return None
    q, _, yr = str(s).strip().partition("-")
    m = {"q1": 1, "q2": 4, "q3": 7, "q4": 10}.get(q.strip().lower())
    if m and yr.strip().isdigit():
        return f"{int(yr):04d}-{m:02d}-01"
    return None


def _d_year(s):
    s = str(s).strip() if s is not None else ""
    return f"{int(s):04d}-01-01" if s.isdigit() else None


def _glance_year(s):
    """Glance Date labels are 'YYYY' or fiscal/crop years 'YYYY/YY'. Return the
    leading 4-digit year as int, or None."""
    if s is None:
        return None
    m = re.match(r"\s*(\d{4})", str(s))
    return int(m.group(1)) if m else None


def _d_week(s):
    """'W1.Jan.2017' -> approx date (week index -> day within month)."""
    if not s:
        return None
    parts = str(s).strip().split(".")
    if len(parts) != 3:
        return None
    wk, mon, yr = parts
    w = "".join(ch for ch in wk if ch.isdigit())
    m = _MONTHS.get(mon.strip().lower()[:3])
    if not (w and m and yr.strip().isdigit()):
        return None
    day = min(1 + (int(w) - 1) * 7, 28)
    return f"{int(yr):04d}-{m:02d}-{day:02d}"


# --------------------------------------------------------------------------- #
# fetch functions
# --------------------------------------------------------------------------- #
_GLANCE_DATA = BASE + "srilanka_glance/alldata.php"
_GLANCE_DICT = BASE + "srilanka_glance/SLGlance_Data.php"


def fetch_glance(node_id: str) -> None:
    """One subset = one 'Sri Lanka at a Glance' subcategory, long-format annual."""
    sub = _eid(node_id)[len("glance-"):].upper()  # 'glance-pop' -> 'POP'
    dic = _js_array(_fetch_text(_GLANCE_DICT), "classifications")
    cols = {r["Code"]: r for r in dic if r.get("Subcategory_Code") == sub}
    if not cols:
        raise ValueError(f"no glance indicators for subcategory {sub!r}")
    data = _js_array(_fetch_text(_GLANCE_DATA), "datatable")
    rows = []
    for rec in data:
        period = rec.get("Date")
        yr = _glance_year(period)
        if yr is None:
            continue
        for code, meta in cols.items():
            val = _num(rec.get(code))
            if val is None:
                continue
            rows.append({
                "date": f"{yr:04d}-01-01",
                "year": yr,
                "period": period,
                "indicator_code": code,
                "indicator_title": meta.get("Title"),
                "units": meta.get("units"),
                "value": val,
            })
    save_raw_ndjson(rows, node_id)


def fetch_cpi(node_id: str) -> None:
    """CCPI / NCPI: monthly index value plus month-on-month and year-on-year %."""
    eid = _eid(node_id)  # 'ccpi' | 'ncpi'
    fname = "CCPI_Data.php" if eid == "ccpi" else "NCPI_Data.php"
    text = _fetch_text(BASE + "EIP/" + fname)
    codes = {c["Code"]: c for c in _js_array(text, eid + "_codes")}
    rows = []
    for measure, arr_name in (
        ("index", eid + "_m_val"),
        ("mom_pct", eid + "_mom"),
        ("yoy_pct", eid + "_yoy"),
    ):
        try:
            arr = _js_array(text, arr_name)
        except ValueError:
            continue
        for rec in arr:
            d = _d_month(rec.get("Date"))
            if not d:
                continue
            for code, meta in codes.items():
                val = _num(rec.get(code))
                if val is None:
                    continue
                rows.append({
                    "date": d,
                    "period": rec.get("Date"),
                    "measure": measure,
                    "category_code": code,
                    "category_title": meta.get("title"),
                    "weight": _num(meta.get("weight")),
                    "base_value": _num(meta.get("base_value")),
                    "value": val,
                })
    save_raw_ndjson(rows, node_id)


def fetch_index(node_id: str) -> None:
    """PPI / IIP: monthly index values by category."""
    eid = _eid(node_id)  # 'ppi' | 'iip'
    fname = "PPI_Data.php" if eid == "ppi" else "IIP_Data.php"
    text = _fetch_text(BASE + "EIP/" + fname)
    codes = {c["Code"]: c for c in _js_array(text, eid + "_codes")}
    rows = []
    for rec in _js_array(text, eid + "_m_val"):
        d = _d_month(rec.get("Date"))
        if not d:
            continue
        for code, meta in codes.items():
            val = _num(rec.get(code))
            if val is None:
                continue
            rows.append({
                "date": d,
                "period": rec.get("Date"),
                "category_code": code,
                "category_title": meta.get("title") or meta.get("Name"),
                "value": val,
            })
    save_raw_ndjson(rows, node_id)


_GDP_ARRAYS = [
    ("quarterly", "constant", "value", "gdp_qt_val_constant"),
    ("quarterly", "current", "value", "gdp_qt_val_current"),
    ("quarterly", "constant", "share", "gdp_qt_shr_constant"),
    ("quarterly", "current", "share", "gdp_qt_shr_current"),
    ("quarterly", "constant", "growth", "gdp_qt_grw_constant"),
    ("quarterly", "current", "growth", "gdp_qt_grw_current"),
    ("annual", "constant", "value", "gdp_yy_val_constant"),
    ("annual", "current", "value", "gdp_yy_val_current"),
    ("annual", "constant", "share", "gdp_yy_shr_constant"),
    ("annual", "current", "share", "gdp_yy_shr_current"),
    ("annual", "constant", "growth", "gdp_yy_grw_constant"),
    ("annual", "current", "growth", "gdp_yy_grw_current"),
]


def fetch_gdp(node_id: str) -> None:
    """GDP by economic activity: quarterly + annual, constant/current,
    value / share-of-GDP / growth-rate, all in one long-format table."""
    text = _fetch_text(BASE + "EIP/GDP_Data.php")
    codes = {c["Code"]: c for c in _js_array(text, "gdp_codes")}
    rows = []
    for freq, basis, measure, arr_name in _GDP_ARRAYS:
        try:
            arr = _js_array(text, arr_name)
        except ValueError:
            continue
        for rec in arr:
            raw = rec.get("Date")
            d = _d_quarter(raw) if freq == "quarterly" else _d_year(raw)
            if not d:
                continue
            for code, meta in codes.items():
                val = _num(rec.get(code))
                if val is None:
                    continue
                rows.append({
                    "date": d,
                    "period": raw,
                    "frequency": freq,
                    "price_basis": basis,
                    "measure": measure,
                    "sector_code": code,
                    "sector_title": meta.get("title"),
                    "sector_group": meta.get("category"),
                    "value": val,
                })
    save_raw_ndjson(rows, node_id)


def fetch_prices(node_id: str) -> None:
    """Weekly island-wide retail prices, long-format by product."""
    text = _fetch_text(BASE + "Prices/Prices_Data.php")
    pip = {p["product"]: p for p in _js_array(text, "pip")}
    rows = []
    for rec in _js_array(text, "prices"):
        wk = rec.get("Date")
        d = _d_week(wk)
        for prod, meta in pip.items():
            val = _num(rec.get(prod))
            if val is None:
                continue
            rows.append({
                "date": d,
                "week_label": wk,
                "product": prod,
                "product_name": (meta.get("name") or "").strip(),
                "category": meta.get("category"),
                "price_lkr": val,
            })
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# specs
# --------------------------------------------------------------------------- #
def _fn_for(eid: str):
    if eid.startswith("glance-"):
        return fetch_glance
    if eid in ("ccpi", "ncpi"):
        return fetch_cpi
    if eid in ("ppi", "iip"):
        return fetch_index
    if eid == "gdp":
        return fetch_gdp
    if eid == "weekly-retail-prices":
        return fetch_prices
    raise ValueError(f"no fetch fn for entity {eid!r}")


DOWNLOAD_SPECS = [
    NodeSpec(id=PREFIX + eid, fn=_fn_for(eid), kind="download")
    for eid in ENTITY_IDS
]


def _sql_for(eid: str, dep: str) -> str:
    if eid.startswith("glance-"):
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   year,
                   period,
                   indicator_code,
                   indicator_title,
                   units,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep}"
            WHERE value IS NOT NULL
        '''
    if eid in ("ccpi", "ncpi"):
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   period,
                   measure,
                   category_code,
                   category_title,
                   weight,
                   base_value,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep}"
            WHERE value IS NOT NULL
        '''
    if eid in ("ppi", "iip"):
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   period,
                   category_code,
                   category_title,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep}"
            WHERE value IS NOT NULL
        '''
    if eid == "gdp":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   period,
                   frequency,
                   price_basis,
                   measure,
                   sector_code,
                   sector_title,
                   sector_group,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep}"
            WHERE value IS NOT NULL
        '''
    # weekly-retail-prices
    return f'''
        SELECT CAST(date AS DATE) AS date,
               week_label,
               product,
               product_name,
               category,
               CAST(price_lkr AS DOUBLE) AS price_lkr
        FROM "{dep}"
        WHERE price_lkr IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_sql_for(_eid(spec.id), spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
