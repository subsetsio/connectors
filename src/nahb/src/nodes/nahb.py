"""NAHB Housing Economics connector.

NAHB publishes a small set of survey-based indices as Excel "history" workbooks
(one file per index table) under period-versioned /-/media/ URLs. There is no API
or catalog endpoint. Each workbook holds the FULL time series back to inception,
so a stateless full re-pull of the single latest-release file per table is the
correct shape (files are tens of KB; revisions are picked up for free).

The media URLs embed the release period and are NOT persistent (HMI monthly,
RMI/CHI/HBGI/MMS quarterly). We therefore resolve the current file each run by
fetching the human index page and matching the <a href> to the table's file
token, rather than constructing a date-based URL (which would 404 on release lag).

Each workbook has its own bespoke Excel layout (stacked year/month blocks,
multi-row nested headers, several sub-tables per sheet). Because a SQL transform
can only read parquet/ndjson/csv, the fetch fn parses the workbook into a tidy
long-format record stream and saves ndjson; the transform is a thin cast/select.
"""

import io
import math
import re

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

HOST = "https://www.nahb.org"

# Index landing pages we scrape to resolve the current file URL.
LANDING_HMI = f"{HOST}/news-and-economics/housing-economics/indices/housing-market-index"
LANDING_RMI = f"{HOST}/news-and-economics/housing-economics/indices/remodeling-market-index"
LANDING_CHI = f"{HOST}/news-and-economics/housing-economics/indices/cost-of-housing-index"
LANDING_HBGI = f"{HOST}/news-and-economics/housing-economics/indices/home-building-geography-index"
LANDING_MMS = f"{HOST}/news-and-economics/housing-economics/indices/multifamily-market-survey"

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
_QSTART = {"q1": "01-01", "q2": "04-01", "q3": "07-01", "q4": "10-01"}
_ORD = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4}


# --------------------------------------------------------------------------- #
# cell helpers
# --------------------------------------------------------------------------- #
def _month(v):
    if not (v is not None and isinstance(v, str)):
        return None
    return _MONTHS.get(v.strip().lower().rstrip(".")[:3])


def _is_year(v):
    try:
        if isinstance(v, str):
            if not v.strip().replace(".0", "").isdigit():
                return None
        n = int(float(v))
    except (TypeError, ValueError):
        return None
    return n if 1985 <= n <= 2100 else None


def _num(v):
    if v is None:
        return None
    try:
        if isinstance(v, str) and not v.strip():
            return None
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


def _text(v):
    return v.strip() if (v is not None and isinstance(v, str)) else ""


def _qdate(year, q):
    return f"{year}-{_QSTART[q.lower()]}"


def _quarter_cols(df, row):
    """col -> (year, 'Qn') for a quarter-header row, year forward-filled from the row above."""
    colperiod, last = {}, None
    for c in range(df.shape[1]):
        y = _is_year(df.iat[row - 1, c])
        if y:
            last = y
        q = str(df.iat[row, c]).strip()
        if q.lower() in ("q1", "q2", "q3", "q4") and last:
            colperiod[c] = (last, q)
    return colperiod


def _is_quarter_header(df, row):
    return sum(
        1 for c in range(df.shape[1])
        if str(df.iat[row, c]).strip().lower() in ("q1", "q2", "q3", "q4")
    ) >= 4


# --------------------------------------------------------------------------- #
# per-table parsers  (each returns list[dict] in tidy long format)
# --------------------------------------------------------------------------- #
def parse_hmi_national(df):
    """Table 2: year per row in col0, 12 monthly HMI values in cols 1..12."""
    out = []
    for i in range(len(df)):
        y = _is_year(df.iat[i, 0])
        if y is None:
            continue
        for m in range(1, 13):
            if m >= df.shape[1]:
                break
            v = _num(df.iat[i, m])
            if v is not None:
                out.append({"date": f"{y}-{m:02d}-01", "hmi": v})
    return out


def parse_hmi_components(df):
    """Table 3: three stacked blocks (present sales / next 6 months / traffic),
    each [label][year-header][12 month rows]."""
    out, component, years = [], None, {}
    for i in range(len(df)):
        c0 = df.iat[i, 0]
        m = _month(c0)
        yrcols = {c: _is_year(df.iat[i, c]) for c in range(1, df.shape[1]) if _is_year(df.iat[i, c])}
        if yrcols and (pd.isna(c0) if not isinstance(c0, str) else False):
            years = yrcols
            continue
        if m is None and isinstance(c0, str) and c0.strip():
            lab = c0.lower()
            if "present" in lab:
                component = "present_sales"
            elif "next six" in lab:
                component = "future_sales"
            elif "traffic" in lab:
                component = "traffic"
            continue
        if m is not None and component and years:
            for c, y in years.items():
                v = _num(df.iat[i, c])
                if v is not None:
                    out.append({"date": f"{y}-{m:02d}-01", "component": component, "value": v})
    return out


def _parse_hmi_regional(df, value_key):
    """Tables 4 & 5: year-blocks of [year-row][month-row][4 region rows]."""
    out, colyear, colmonth = [], {}, {}
    regions = {"northeast", "midwest", "south", "west"}
    for i in range(len(df)):
        c0 = df.iat[i, 0]
        c0na = pd.isna(c0) if not isinstance(c0, str) else not c0.strip()
        yrcols = {c: _is_year(df.iat[i, c]) for c in range(1, df.shape[1]) if _is_year(df.iat[i, c])}
        monthcols = {c: _month(df.iat[i, c]) for c in range(1, df.shape[1]) if _month(df.iat[i, c])}
        if c0na and yrcols and not monthcols:
            colyear, last = {}, None
            for c in range(1, df.shape[1]):
                if c in yrcols:
                    last = yrcols[c]
                if last is not None:
                    colyear[c] = last
            continue
        if c0na and monthcols:
            colmonth = monthcols
            continue
        reg = _text(c0).lower()
        if reg in regions and colmonth and colyear:
            for c, m in colmonth.items():
                y = colyear.get(c)
                v = _num(df.iat[i, c])
                if y is not None and v is not None:
                    out.append({"date": f"{y}-{m:02d}-01", "region": _text(c0), value_key: v})
    return out


def parse_hmi_regional(df):
    return _parse_hmi_regional(df, "hmi")


def parse_hmi_regional_3mo(df):
    return _parse_hmi_regional(df, "hmi_3mo_ma")


def parse_rmi_national(df):
    """Table 1: single quarter grid; row labels in the column left of the first quarter."""
    out, colperiod, labelcol = [], {}, None
    for i in range(len(df)):
        if _is_quarter_header(df, i):
            colperiod = _quarter_cols(df, i)
            labelcol = (min(colperiod) - 1) if colperiod else None
            continue
        if not colperiod or labelcol is None or labelcol < 0:
            continue
        label = _text(df.iat[i, labelcol])
        if not label:
            continue
        for c, (y, q) in colperiod.items():
            v = _num(df.iat[i, c])
            if v is not None:
                out.append({"period": f"{y}-{q.upper()}", "date": _qdate(y, q),
                            "indicator": label, "value": v})
    return out


_RMI_REG_MAP = {
    3: ("National", "RMI"), 4: ("National", "Current Market Conditions"),
    5: ("National", "Future Market Indicators"),
    6: ("Northeast", "RMI"), 7: ("Northeast", "Current Market Conditions"),
    8: ("Northeast", "Future Market Indicators"),
    9: ("Midwest", "RMI"), 10: ("Midwest", "Current Market Conditions"),
    11: ("Midwest", "Future Market Indicators"),
    12: ("South", "RMI"), 13: ("South", "Current Market Conditions"),
    14: ("South", "Future Market Indicators"),
    15: ("West", "RMI"), 16: ("West", "Current Market Conditions"),
    17: ("West", "Future Market Indicators"),
}


def parse_rmi_regional(df):
    """Table 2: period text ('1st Quarter 2020') in col2, fixed region/measure columns."""
    out = []
    for i in range(len(df)):
        p = df.iat[i, 2]
        if not (isinstance(p, str) and p.strip()):
            continue
        mt = re.match(r"(1st|2nd|3rd|4th)\s+Quarter\s+(\d{4})", p.strip(), re.I)
        if not mt:
            continue
        q = _ORD[mt.group(1).lower()]
        y = int(mt.group(2))
        for c, (region, measure) in _RMI_REG_MAP.items():
            if c >= df.shape[1]:
                continue
            v = _num(df.iat[i, c])
            if v is not None:
                out.append({"period": f"{y}-Q{q}", "date": _qdate(y, f"q{q}"),
                            "region": region, "measure": measure, "value": v})
    return out


def parse_chi(df):
    """CHI history: header row 0 (Name, msa_fip, flag, Q1_23..Q1_26); one row per (geography, metric flag)."""
    out = {}
    qcols = {}
    for c in range(3, df.shape[1]):
        mt = re.match(r"q([1-4])_(\d{2})$", str(df.iat[0, c]).strip().lower())
        if mt:
            qcols[c] = (2000 + int(mt.group(2)), int(mt.group(1)))
    out = []
    for i in range(1, len(df)):
        fip = _num(df.iat[i, 1])
        flag = _num(df.iat[i, 2])
        if fip is None or flag is None:
            continue
        name = _text(df.iat[i, 0]) or None
        for c, (yy, q) in qcols.items():
            v = _num(df.iat[i, c])
            if v is None:
                continue
            out.append({"period": f"{yy}-Q{q}", "date": _qdate(yy, f"q{q}"),
                        "msa_fip": int(fip), "flag": int(flag), "name": name, "value": v})
    return out


def parse_hbgi(df):
    """HBGI 'NAHB' sheet: sections (growth rate / market share) x (single-family / multifamily),
    each a quarter grid over 7 geography rows."""
    out, metric, segment, colperiod = [], None, None, {}
    for i in range(len(df)):
        s = _text(df.iat[i, 0])
        if "Growth Rate" in s:
            metric = "growth_rate"
        elif "Market Share" in s:
            metric = "market_share"
        if _is_quarter_header(df, i):
            if s in ("Single-Family", "Multifamily"):
                segment = s
            colperiod = _quarter_cols(df, i)
            continue
        if colperiod and s and ("Metro" in s or "County" in s):
            for c, (y, q) in colperiod.items():
                v = _num(df.iat[i, c])
                if v is not None:
                    out.append({"period": f"{y}-{q.upper()}", "date": _qdate(y, q),
                                "metric": metric, "segment": segment, "geography": s, "value": v})
    return out


def _mms_title(s):
    if "Production Index" in s:
        return "Multifamily Production Index"
    if "Occupancy Index" in s:
        return "Multifamily Occupancy Index"
    if "Market Conditions" in s:
        return "Change in Overall Market Conditions"
    return None


def parse_mms(df):
    """MMS Table 1: three stacked quarter grids (production / occupancy / market-conditions)."""
    out, index_type, colperiod = [], None, {}
    for i in range(len(df)):
        s = _text(df.iat[i, 0])
        row_has_num = any(_num(df.iat[i, c]) is not None for c in range(1, df.shape[1]))
        title = _mms_title(s)
        if title and not row_has_num:
            index_type = title
        if _is_quarter_header(df, i):
            colperiod = _quarter_cols(df, i)
            continue
        if colperiod and s:
            for c, (y, q) in colperiod.items():
                v = _num(df.iat[i, c])
                if v is not None:
                    out.append({"period": f"{y}-{q.upper()}", "date": _qdate(y, q),
                                "index_type": index_type, "component": s, "value": v})
    return out


# --------------------------------------------------------------------------- #
# fetch
# --------------------------------------------------------------------------- #
# entity_id -> (landing page, file-name token, sheet, parser)
CONFIG = {
    "hmi-national-history": (LANDING_HMI, "t2-national-hmi-history", 0, parse_hmi_national),
    "hmi-components-history": (LANDING_HMI, "t3-national-hmi-components-history", 0, parse_hmi_components),
    "hmi-regional-history": (LANDING_HMI, "t4-regional-hmi-history", 0, parse_hmi_regional),
    "hmi-regional-3mo-moving-average": (LANDING_HMI, "t5-regional-hmi-history", 0, parse_hmi_regional_3mo),
    "rmi-national-history": (LANDING_RMI, "rmi-table1", 0, parse_rmi_national),
    "rmi-regional-history": (LANDING_RMI, "rmi-table2", 0, parse_rmi_regional),
    "chi-history": (LANDING_CHI, "chi-history", 0, parse_chi),
    "hbgi-full-findings": (LANDING_HBGI, "hbgi-full-findings", "NAHB", parse_hbgi),
    "mms-survey": (LANDING_MMS, "table1-xlxs", 0, parse_mms),
}


@transient_retry()
def _http_get(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _resolve_url(landing, token):
    """Find the current Excel file URL on the landing page by matching the file token."""
    html = _http_get(landing).text
    cand = [
        h for h in re.findall(r'href="([^"]+)"', html)
        if token.lower() in h.lower() and "/-/media/" in h.lower() and ".xls" in h.lower()
    ]
    if not cand:
        raise AssertionError(f"no media link for token {token!r} on {landing}")
    h = cand[0]
    if h.startswith("//"):
        return "https:" + h
    if h.startswith("/"):
        return HOST + h
    return h


def _read_excel(content, sheet):
    engine = "xlrd" if content[:2] == b"\xd0\xcf" else "openpyxl"
    return pd.read_excel(io.BytesIO(content), sheet_name=sheet, engine=engine, header=None)


def fetch_one(node_id: str) -> None:
    entity = node_id[len("nahb-"):]
    landing, token, sheet, parser = CONFIG[entity]
    url = _resolve_url(landing, token)
    content = _http_get(url).content
    df = _read_excel(content, sheet)
    rows = parser(df)
    if not rows:
        raise AssertionError(f"{node_id}: parser produced 0 rows from {url}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"nahb-{eid}", fn=fetch_one, kind="download")
    for eid in CONFIG
]


# --------------------------------------------------------------------------- #
# transforms — one published Delta table per subset (thin cast/select)
# --------------------------------------------------------------------------- #
def _t(download_id, sql, *, key, temporal="date"):
    return SqlNodeSpec(
        id=f"{download_id}-transform", deps=[download_id], sql=sql,
        key=key, temporal=temporal,
    )


TRANSFORM_SPECS = [
    _t("nahb-hmi-national-history", '''
        SELECT CAST(date AS DATE) AS date, CAST(hmi AS DOUBLE) AS hmi
        FROM "nahb-hmi-national-history" WHERE hmi IS NOT NULL
    ''', key=("date",)),
    _t("nahb-hmi-components-history", '''
        SELECT DISTINCT CAST(date AS DATE) AS date, component,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-hmi-components-history" WHERE value IS NOT NULL
    ''', key=("date", "component")),
    _t("nahb-hmi-regional-history", '''
        SELECT DISTINCT CAST(date AS DATE) AS date, region,
               CAST(hmi AS DOUBLE) AS hmi
        FROM "nahb-hmi-regional-history" WHERE hmi IS NOT NULL
    ''', key=("date", "region")),
    _t("nahb-hmi-regional-3mo-moving-average", '''
        SELECT DISTINCT CAST(date AS DATE) AS date, region,
               CAST(hmi_3mo_ma AS DOUBLE) AS hmi_3mo_ma
        FROM "nahb-hmi-regional-3mo-moving-average" WHERE hmi_3mo_ma IS NOT NULL
    ''', key=("date", "region")),
    _t("nahb-rmi-national-history", '''
        SELECT period, CAST(date AS DATE) AS date, indicator,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-rmi-national-history" WHERE value IS NOT NULL
    ''', key=("date", "indicator")),
    _t("nahb-rmi-regional-history", '''
        SELECT period, CAST(date AS DATE) AS date, region, measure,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-rmi-regional-history" WHERE value IS NOT NULL
    ''', key=("date", "region", "measure")),
    _t("nahb-chi-history", '''
        SELECT period, CAST(date AS DATE) AS date,
               CAST(msa_fip AS INTEGER) AS msa_fip,
               CAST(flag AS INTEGER) AS flag, name,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-chi-history" WHERE value IS NOT NULL
    ''', key=("date", "msa_fip", "flag")),
    _t("nahb-hbgi-full-findings", '''
        SELECT period, CAST(date AS DATE) AS date, metric, segment, geography,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-hbgi-full-findings" WHERE value IS NOT NULL
    ''', key=("date", "metric", "segment", "geography")),
    _t("nahb-mms-survey", '''
        SELECT period, CAST(date AS DATE) AS date, index_type, component,
               CAST(value AS DOUBLE) AS value
        FROM "nahb-mms-survey" WHERE value IS NOT NULL
    ''', key=("date", "index_type", "component")),
]
