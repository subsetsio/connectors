"""Federal Reserve Bank of Atlanta — research-and-data products.

Mechanism: bulk_download. Each entity is one (or a small set of) machine-readable
data file(s) on the Atlanta Fed CDN — mostly multi-sheet Excel workbooks, a couple
of CSVs, and the China macroeconomy panel as dated ZIP releases. The corpus is
small (tens of MB total) and the files are overwritten in place on each release,
so every fetch is a stateless full re-pull: re-download the file, parse the data
sheet defensively, and normalize to a tidy long/record shape saved as NDJSON. No
incremental query is available or needed. The SQL transforms only cast/clean the
already-normalized raw, because the workbooks themselves are not SQL-readable.

The dominant raw shape is long (date, series, value), produced by melting a wide
time-series sheet (sticky CPI, wage growth, Wu-Xia, Taylor-rule inputs, underlying
inflation, both China panels). The remainder keep a bespoke tidy shape that matches
the source (GDPNow nowcast evolution, deflation probabilities, HOAM, labor-force
participation flows, market probability tracker, CRE index, GDP-based recession
index).
"""

import csv
import io
import math
import re
import zipfile
from datetime import date, datetime

import openpyxl
import xlrd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import CHINA_PAGE, ENTITY_IDS, URLS

SLUG = "federal-reserve-bank-of-atlanta"
PREFIX = SLUG + "-"

_NULLISH = {"", "na", "n/a", "#n/a", ".", "nan", "null", "none"}


# --------------------------------------------------------------------------- #
# HTTP                                                                         #
# --------------------------------------------------------------------------- #
@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# Parsing helpers                                                             #
# --------------------------------------------------------------------------- #
def _ws_rows(content: bytes, sheet: str | None = None) -> list[tuple]:
    """All rows of one worksheet as value tuples (read-only, evaluated)."""
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        ws = wb[sheet] if sheet else wb.worksheets[0]
        return [tuple(r) for r in ws.iter_rows(values_only=True)]
    finally:
        wb.close()


def _num(v) -> float | None:
    """Coerce a cell to float, mapping the source's many null sentinels to None."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        return None if math.isnan(f) else f
    s = str(v).strip()
    if s.lower() in _NULLISH:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _iso(v) -> str | None:
    """Coerce a cell to an ISO date string (YYYY-MM-DD)."""
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date):
        return v.isoformat()
    s = str(v).strip()
    if not s:
        return None
    # 'YYYY-MM' -> first of month
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-01"
    # 'YYYY-MM-DD' (optionally with a trailing time component)
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # 'YYYYMMDD'
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def _quarter_iso(v) -> str | None:
    """Parse a quarter label -> first day of that quarter.

    Handles both orders: '1967:Q4' / '2020Q1' (year first) and 'Q1 1998'
    (quarter first).
    """
    if v is None:
        return None
    s = str(v)
    m = re.search(r"(\d{4})\D*Q\s*([1-4])", s)  # year-first
    if not m:
        m2 = re.search(r"Q\s*([1-4])\D*(\d{4})", s)  # quarter-first
        if m2:
            year, q = int(m2.group(2)), int(m2.group(1))
            return f"{year:04d}-{(q - 1) * 3 + 1:02d}-01"
        return None
    year, q = int(m.group(1)), int(m.group(2))
    return f"{year:04d}-{(q - 1) * 3 + 1:02d}-01"


def _decimal_year_iso(dec: float, freq: str) -> str:
    """Decimal year (1949.25, 1949.0833..) -> ISO date for the given frequency."""
    year = int(math.floor(dec))
    frac = dec - year
    if freq == "Q":
        month = int(round(frac * 4)) * 3 + 1
    elif freq == "M":
        month = int(round(frac * 12)) + 1
    else:  # annual
        month = 1
    month = min(max(month, 1), 12)
    return f"{year:04d}-{month:02d}-01"


def _melt(rows, header_row=0, date_col=0, first_data_col=1):
    """Melt a wide date-indexed sheet into (date, series, value) records.

    Series names are read from `header_row`; data begins on the next row, with the
    observation date in `date_col`. Null sentinels and blank series are dropped.
    """
    if len(rows) <= header_row:
        return []
    header = rows[header_row]
    out = []
    for r in rows[header_row + 1:]:
        if date_col >= len(r):
            continue
        d = _iso(r[date_col])
        if not d:
            continue
        for j in range(first_data_col, len(header)):
            name = header[j]
            if name is None or not str(name).strip():
                continue
            val = _num(r[j]) if j < len(r) else None
            if val is None:
                continue
            out.append({"date": d, "series": str(name).strip(), "value": val})
    return out


# --------------------------------------------------------------------------- #
# Per-entity handlers — each returns a list[dict] of tidy raw records         #
# --------------------------------------------------------------------------- #
def _h_sticky_price_cpi(_asset):
    rows = _ws_rows(_fetch_bytes(URLS["sticky-price-cpi"]), "Data")
    return _melt(rows, header_row=0)


def _h_wage_growth_tracker(_asset):
    # data_overall: row 0 is a source banner, row 1 the cut names, data from row 2.
    rows = _ws_rows(_fetch_bytes(URLS["wage-growth-tracker"]), "data_overall")
    return _melt(rows, header_row=1)


def _h_wu_xia(_asset):
    # Data: row 0 holds the two series names, data from row 1.
    rows = _ws_rows(_fetch_bytes(URLS["wu-xia-shadow-federal-funds-rate"]), "Data")
    return _melt(rows, header_row=0)


def _h_taylor_rule(_asset):
    # Union the underlying-input sheets: each has descriptions on row 0, series
    # codes on row 1, dates in column A from row 2. Series codes are unique.
    content = _fetch_bytes(URLS["taylor-rule"])
    out = []
    for sheet in (
        "FedFundsRates",
        "InflationTargetMeasures",
        "NaturalRateMeasures",
        "GapMeasures",
        "InflationMeasures",
    ):
        rows = _ws_rows(content, sheet)
        out.extend(_melt(rows, header_row=1))
    return out


def _h_underlying_inflation(_asset):
    # ChartData: repeating per-measure blocks. Row 1 marks each block with 'DATE';
    # the column to its right is the measure's 12-month value, named on row 0.
    rows = _ws_rows(_fetch_bytes(URLS["underlying-inflation-dashboard"]), "ChartData")
    if len(rows) < 3:
        return []
    label_row, head_row = rows[0], rows[1]
    date_cols = [j for j, c in enumerate(head_row) if str(c).strip().upper() == "DATE"]
    out = []
    for dc in date_cols:
        vc = dc + 1
        measure = label_row[vc] if vc < len(label_row) else None
        if not measure:
            continue
        measure = str(measure).strip()
        for r in rows[2:]:
            d = _iso(r[dc]) if dc < len(r) else None
            v = _num(r[vc]) if vc < len(r) else None
            if d and v is not None:
                out.append({"date": d, "measure": measure, "value": v})
    return out


def _h_deflation_probabilities(_asset):
    # Data: repeating 4-column blocks (date, lower bound, probability, blank) for
    # successive reference-price horizons. Row 0 carries the horizon description.
    rows = _ws_rows(_fetch_bytes(URLS["deflation-probabilities"]), "Data")
    if len(rows) < 4:
        return []
    label_row = rows[0]
    ncols = max(len(r) for r in rows)
    out = []
    for o in range(0, ncols, 4):
        horizon = label_row[o + 1] if o + 1 < len(label_row) else None
        horizon = str(horizon).strip() if horizon else None
        for r in rows[3:]:
            d = _iso(r[o]) if o < len(r) else None
            if not d:
                continue
            lb = _num(r[o + 1]) if o + 1 < len(r) else None
            prob = _num(r[o + 2]) if o + 2 < len(r) else None
            if prob is None and lb is None:
                continue
            out.append(
                {
                    "date": d,
                    "horizon": horizon,
                    "lower_bound": lb,
                    "probability": prob,
                }
            )
    return out


def _h_gdpnow(_asset):
    # Contributions: row 1 is the header; data from row 2. The columns are the
    # evolution of the current-quarter nowcast and its component contributions.
    rows = _ws_rows(_fetch_bytes(URLS["gdpnow"]), "Contributions")
    out = []
    for r in rows[2:]:
        if not r or len(r) < 11:
            continue
        d = _iso(r[0])
        if not d:
            continue
        out.append(
            {
                "date": d,
                "forecast_quarter": _iso(r[1]),
                "pce": _num(r[2]),
                "nonresidential_fixed_investment": _num(r[3]),
                "residential_investment": _num(r[4]),
                "change_in_inventories": _num(r[5]),
                "net_exports": _num(r[6]),
                "government": _num(r[7]),
                "change_in_gdp_forecast": _num(r[8]),
                "gdp_forecast": _num(r[9]),
                "previous_gdp_forecast": _num(r[10]) if len(r) > 10 else None,
                "data_releases": (str(r[11]).strip() if len(r) > 11 and r[11] else None),
            }
        )
    return out


def _h_hoam(_asset):
    # HOAM_CBSA_Data: one row per metro per month (header on row 0).
    rows = _ws_rows(_fetch_bytes(URLS["home-ownership-affordability-monitor"]), "Sheet1")
    out = []
    for r in rows[1:]:
        if len(r) < 5 or not r[0] or not r[2]:
            continue
        out.append(
            {
                "cbsa_name": str(r[0]).strip(),
                "cbsa_code": str(r[1]).strip() if r[1] is not None else None,
                "date": _iso(r[2]),
                "affordability": _num(r[3]),
                "housing_cost_share_of_income": _num(r[4]),
            }
        )
    return out


def _h_lfpd(_asset):
    # trends-over-time / bydate_qtrly: 4 banner rows, header on row 4, data after.
    # Columns: date, Age, Race, Education, Gender, then participation-flow values.
    content = _fetch_bytes(URLS["labor-force-participation-dynamics"])
    rows = _ws_rows(content, "bydate_qtrly")
    if len(rows) < 6:
        return []
    header = rows[4]
    comp_idx = [j for j in range(5, len(header)) if header[j] and str(header[j]).strip()]
    out = []
    for r in rows[5:]:
        d = _quarter_iso(r[0]) if r else None
        if not d:
            continue
        age = str(r[1]).strip() if len(r) > 1 and r[1] is not None else None
        race = str(r[2]).strip() if len(r) > 2 and r[2] is not None else None
        edu = str(r[3]).strip() if len(r) > 3 and r[3] is not None else None
        gender = str(r[4]).strip() if len(r) > 4 and r[4] is not None else None
        for j in comp_idx:
            val = _num(r[j]) if j < len(r) else None
            if val is None:
                continue
            out.append(
                {
                    "date": d,
                    "age": age,
                    "race_ethnicity": race,
                    "education": edu,
                    "gender": gender,
                    "component": str(header[j]).strip(),
                    "value": val,
                }
            )
    return out


def _h_market_probability_tracker(_asset):
    # DATA sheet is already tidy long: date, reference_start, target_range, field,
    # value. openpyxl read-only misreads this workbook's dimensions, so use pandas.
    import pandas as pd

    df = pd.read_excel(io.BytesIO(_fetch_bytes(URLS["market-probability-tracker"])), sheet_name="DATA")
    needed = {"date", "reference_start", "target_range", "field", "value"}
    if not needed.issubset(df.columns):
        raise AssertionError(f"market-probability-tracker DATA header changed: {list(df.columns)}")
    df = df.where(pd.notna(df), None)
    out = []
    for rec in df.to_dict("records"):
        d = _iso(rec["date"])
        if not d:
            continue
        out.append(
            {
                "date": d,
                "reference_start": _iso(rec["reference_start"]),
                "target_range": str(rec["target_range"]).strip() if rec["target_range"] is not None else None,
                "field": str(rec["field"]).strip() if rec["field"] is not None else None,
                "value": _num(rec["value"]),
            }
        )
    return out


def _h_cre_market_index(_asset):
    text = _fetch_text(URLS["commercial-real-estate-market-index"])
    reader = csv.DictReader(io.StringIO(text))
    out = []
    for row in reader:
        d = _iso(row.get("DT"))
        if not d:
            continue
        out.append(
            {
                "geography": (row.get("Geography.Name") or "").strip() or None,
                "cbsa_code": (row.get("CBSA.Code") or "").strip() or None,
                "asset_type": (row.get("Asset_Type") or "").strip() or None,
                "date": d,
                "variable": (row.get("variable") or "").strip() or None,
                "value": _num(row.get("value")),
            }
        )
    return out


def _h_gdp_recession(_asset):
    # Legacy .xls hosted on econbrowser (the product page links it). xlrd reads it.
    content = _fetch_bytes(URLS["gdp-based-recession-indicator-index"])
    wb = xlrd.open_workbook(file_contents=content)
    sh = wb.sheet_by_name("summary")
    out = []
    for i in range(1, sh.nrows):
        quarter = sh.cell_value(i, 1)
        d = _quarter_iso(quarter)
        if not d:
            continue
        out.append(
            {
                "date": d,
                "period": str(quarter).strip(),
                "recession_index": _num(sh.cell_value(i, 2)),
                "our_dates": _num(sh.cell_value(i, 4)),
                "nber_dates": _num(sh.cell_value(i, 5)),
            }
        )
    return out


def _latest_china_zip_url() -> str:
    html = _fetch_text(CHINA_PAGE)
    best = None
    for href in re.findall(r'href="([^"]+\.zip)"', html, flags=re.IGNORECASE):
        m = re.search(r"(20\d{2})[-_]?(\d{2})", href)
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        full = href if href.startswith("http") else "https://www.atlantafed.org" + href
        if best is None or key > best[0]:
            best = (key, full)
    if best is None:
        raise AssertionError("no dated China macroeconomy ZIP release found on page")
    return best[1]


def _china_member_xlsx(zip_bytes: bytes, suffix: str) -> bytes:
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    for name in z.namelist():
        if name.startswith("__MACOSX"):
            continue
        if name.endswith(suffix):
            return z.read(name)
    raise AssertionError(f"China ZIP missing member ending {suffix}: {z.namelist()}")


def _h_china_gdp_consumption(_asset):
    zip_bytes = _fetch_bytes(_latest_china_zip_url())
    content = _china_member_xlsx(zip_bytes, "_hz_quarterly.xlsx")
    rows = _ws_rows(content, "QuarterlyData")
    return _melt_decimal(rows, "Q")


def _h_china_macroeconomy(_asset):
    zip_bytes = _fetch_bytes(_latest_china_zip_url())
    content = _china_member_xlsx(zip_bytes, "_hz_monthly.xlsx")
    rows = _ws_rows(content, "MonthlyData")
    return _melt_decimal(rows, "M")


def _melt_decimal(rows, freq):
    if not rows:
        return []
    header = rows[0]
    out = []
    for r in rows[1:]:
        if not r or r[0] is None:
            continue
        try:
            dec = float(r[0])
        except (TypeError, ValueError):
            continue
        d = _decimal_year_iso(dec, freq)
        for j in range(1, len(header)):
            name = header[j]
            if name is None or not str(name).strip():
                continue
            val = _num(r[j]) if j < len(r) else None
            if val is None:
                continue
            out.append({"date": d, "series": str(name).strip(), "value": val})
    return out


HANDLERS = {
    "china-gdp-consumption": _h_china_gdp_consumption,
    "china-macroeconomy": _h_china_macroeconomy,
    "commercial-real-estate-market-index": _h_cre_market_index,
    "deflation-probabilities": _h_deflation_probabilities,
    "gdp-based-recession-indicator-index": _h_gdp_recession,
    "gdpnow": _h_gdpnow,
    "home-ownership-affordability-monitor": _h_hoam,
    "labor-force-participation-dynamics": _h_lfpd,
    "market-probability-tracker": _h_market_probability_tracker,
    "sticky-price-cpi": _h_sticky_price_cpi,
    "taylor-rule": _h_taylor_rule,
    "underlying-inflation-dashboard": _h_underlying_inflation,
    "wage-growth-tracker": _h_wage_growth_tracker,
    "wu-xia-shadow-federal-funds-rate": _h_wu_xia,
}


def fetch_one(node_id: str) -> None:
    """Dispatch by entity, parse the source file, and write tidy NDJSON raw."""
    entity = node_id[len(PREFIX):]
    rows = HANDLERS[entity](node_id)
    if not rows:
        raise AssertionError(f"{node_id}: parser produced 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per subset                          #
# --------------------------------------------------------------------------- #
# Long (date, series, value) entities share one cast.
_LONG_SERIES = {
    "china-gdp-consumption",
    "china-macroeconomy",
    "sticky-price-cpi",
    "taylor-rule",
    "wage-growth-tracker",
    "wu-xia-shadow-federal-funds-rate",
}


def _sql_for(entity: str, view: str) -> str:
    if entity in _LONG_SERIES:
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   series,
                   CAST(value AS DOUBLE) AS value
            FROM "{view}"
            WHERE value IS NOT NULL AND date IS NOT NULL
        '''
    if entity == "underlying-inflation-dashboard":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   measure,
                   CAST(value AS DOUBLE) AS value
            FROM "{view}"
            WHERE value IS NOT NULL AND date IS NOT NULL
        '''
    if entity == "deflation-probabilities":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   horizon,
                   CAST(lower_bound AS DOUBLE) AS lower_bound,
                   CAST(probability AS DOUBLE) AS probability
            FROM "{view}"
            WHERE date IS NOT NULL AND probability IS NOT NULL
        '''
    if entity == "gdpnow":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   CAST(forecast_quarter AS DATE) AS forecast_quarter,
                   CAST(gdp_forecast AS DOUBLE) AS gdp_forecast,
                   CAST(pce AS DOUBLE) AS pce,
                   CAST(nonresidential_fixed_investment AS DOUBLE) AS nonresidential_fixed_investment,
                   CAST(residential_investment AS DOUBLE) AS residential_investment,
                   CAST(change_in_inventories AS DOUBLE) AS change_in_inventories,
                   CAST(net_exports AS DOUBLE) AS net_exports,
                   CAST(government AS DOUBLE) AS government,
                   CAST(change_in_gdp_forecast AS DOUBLE) AS change_in_gdp_forecast,
                   data_releases
            FROM "{view}"
            WHERE date IS NOT NULL
        '''
    if entity == "home-ownership-affordability-monitor":
        return f'''
            SELECT cbsa_name,
                   cbsa_code,
                   CAST(date AS DATE) AS date,
                   CAST(affordability AS DOUBLE) AS affordability,
                   CAST(housing_cost_share_of_income AS DOUBLE) AS housing_cost_share_of_income
            FROM "{view}"
            WHERE date IS NOT NULL AND affordability IS NOT NULL
        '''
    if entity == "labor-force-participation-dynamics":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   age,
                   race_ethnicity,
                   education,
                   gender,
                   component,
                   CAST(value AS DOUBLE) AS value
            FROM "{view}"
            WHERE date IS NOT NULL AND value IS NOT NULL
        '''
    if entity == "market-probability-tracker":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   CAST(reference_start AS DATE) AS reference_start,
                   target_range,
                   field,
                   CAST(value AS DOUBLE) AS value
            FROM "{view}"
            WHERE date IS NOT NULL AND value IS NOT NULL
        '''
    if entity == "commercial-real-estate-market-index":
        return f'''
            SELECT geography,
                   cbsa_code,
                   asset_type,
                   CAST(date AS DATE) AS date,
                   variable,
                   CAST(value AS DOUBLE) AS value
            FROM "{view}"
            WHERE date IS NOT NULL AND value IS NOT NULL
        '''
    if entity == "gdp-based-recession-indicator-index":
        return f'''
            SELECT CAST(date AS DATE) AS date,
                   period,
                   CAST(recession_index AS DOUBLE) AS recession_index,
                   CAST(our_dates AS DOUBLE) AS our_dates,
                   CAST(nber_dates AS DOUBLE) AS nber_dates
            FROM "{view}"
            WHERE date IS NOT NULL AND recession_index IS NOT NULL
        '''
    raise KeyError(entity)


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_sql_for(spec.id[len(PREFIX):], spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
