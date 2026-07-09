"""Federal Reserve Bank of Dallas research data.

Stateless full re-pull connector. Each entity is a small Excel workbook (or a
handful of workbooks) served at a stable /research/ URL on dallasfed.org. There
is no catalog API and no incremental query, so every refresh re-fetches each
workbook in full and overwrites — the corpus is tiny (each product is a few KB
to ~500KB) so this is cheap, and revisions/late corrections are picked up for
free. The fetch fns parse the workbooks into tidy long-format parquet (the SQL
transforms can only read parquet/ndjson/csv, so all Excel reshaping happens
here); the transforms are thin cast-and-clean passes.

Gotcha: the site 403s default bot user-agents, so configure_http sets a normal
browser UA once per fetch fn. Media URLs accept both /~/media/ and /-/media/.
"""

import io
import re
import datetime as dt

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
)

BASE = "https://www.dallasfed.org"
_UA = "Mozilla/5.0 (compatible; subsets.io connector; +https://subsets.io)"

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


@transient_retry()
def _fetch_bytes(path: str) -> bytes:
    configure_http(headers={"User-Agent": _UA})
    resp = get(BASE + path, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _excel(path: str) -> pd.ExcelFile:
    return pd.ExcelFile(io.BytesIO(_fetch_bytes(path)))


def _to_float(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return None if (isinstance(v, float) and pd.isna(v)) else float(v)
    s = str(v).strip()
    if s == "" or s.lower() in {"n.a.", "n.a", "na", "nan", "#nan", "#n/a", "n/a", "-"}:
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def _to_date(v, monyy: bool = False):
    """Coerce a cell to a datetime.date. `monyy` parses 'Jun-04' style labels."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, pd.Timestamp):
        return v.date()
    s = str(v).strip()
    if not s:
        return None
    if monyy:
        ts = pd.to_datetime(s, format="%b-%y", errors="coerce")
    else:
        ts = pd.to_datetime(s, errors="coerce")
    return None if pd.isna(ts) else ts.date()


_QUARTER_RE = re.compile(r"(\d{4}).*?Q\s*([1-4])")


def _parse_quarter(v):
    """'2000: Q1' / '1975:Q1' -> first day of the quarter."""
    if v is None:
        return None
    m = _QUARTER_RE.search(str(v))
    if not m:
        return None
    year = int(m.group(1))
    q = int(m.group(2))
    return dt.date(year, (q - 1) * 3 + 1, 1)


# ===========================================================================
# Diffusion surveys: TMOS, TSSOS, TROS, BCS, DES
# ===========================================================================
# Each workbook is a date column + groups of columns per survey question. For a
# question with stem code X the columns are {X (net diffusion index), Xi
# (% increase), Xn (% no change), Xd (% decrease)} in some order. We melt every
# column and decode the component from the suffix via stem membership, keeping
# the source mnemonic as series_code (which preserves the f-prefix = future
# horizon distinction, e.g. 'prod' vs 'fprod').

_COMPONENT = {"i": "increase", "n": "no_change", "d": "decrease"}

# entity -> list of (url, basis); basis labels the workbook variant.
SURVEY_CONFIG = {
    "tmos": {
        "monyy": True,
        "books": [
            ("/~/media/Documents/research/surveys/tmos/documents/alldata.xls", "nsa"),
            ("/~/media/Documents/research/surveys/tmos/documents/alldata_sa.xls", "sa"),
        ],
    },
    "tssos": {
        "monyy": True,
        "books": [
            ("/~/media/Documents/research/surveys/tssos/documents/tssos_alldata.xls", "nsa"),
            ("/~/media/Documents/research/surveys/tssos/documents/tssos_alldata_sa.xls", "sa"),
        ],
    },
    "tros": {
        "monyy": True,
        "books": [
            ("/-/media/Documents/research/surveys/tssos/documents/tros_alldata.xls", "nsa"),
            ("/-/media/Documents/research/surveys/tssos/documents/tros_alldata_sa.xls", "sa"),
        ],
    },
    "bcs": {
        "monyy": False,
        "books": [
            ("/~/media/Documents/research/surveys/bcs/documents/BCS_All_Results.xls", "nsa"),
        ],
    },
    "des": {
        "monyy": False,
        "books": [
            ("/~/media/Documents/research/surveys/des/documents/all_data_qq.xlsx", "qoq"),
            ("/~/media/Documents/research/surveys/des/documents/all_data_yy.xlsx", "yoy"),
        ],
    },
}

DIFFUSION_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("segment", pa.string()),
    ("basis", pa.string()),
    ("series_code", pa.string()),
    ("component", pa.string()),
    ("value", pa.float64()),
])


def _parse_diffusion_sheet(df: pd.DataFrame, segment: str, basis: str, monyy: bool):
    header = [str(c).strip() if c is not None else "" for c in df.iloc[0].tolist()]
    colset = {c for c in header[1:] if c}
    rows = []
    for _, r in df.iloc[1:].iterrows():
        d = _to_date(r.iloc[0], monyy=monyy)
        if d is None:
            continue
        for ci in range(1, len(header)):
            code = header[ci]
            if not code:
                continue
            val = _to_float(r.iloc[ci])
            if val is None:
                continue
            last = code[-1].lower()
            if last in _COMPONENT and code[:-1] in colset:
                series_code, component = code[:-1], _COMPONENT[last]
            else:
                series_code, component = code, "net_index"
            rows.append({
                "date": d,
                "segment": segment,
                "basis": basis,
                "series_code": series_code,
                "component": component,
                "value": val,
            })
    return rows


def fetch_diffusion(node_id: str) -> None:
    entity = node_id[len("dallas-fed-"):]
    cfg = SURVEY_CONFIG[entity]
    rows = []
    for url, basis in cfg["books"]:
        xl = _excel(url)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, header=None)
            if df.empty or str(df.iloc[0, 0]).strip().lower() not in {"date"}:
                continue  # skip helper sheets (Sheet2/Sheet3) without a Date header
            segment = "overall" if len(xl.sheet_names) == 1 or sheet.lower().startswith(("all data", "alldata")) else sheet.strip()
            # DES splits firm types across sheets; surveys keep one data sheet.
            if entity == "des":
                segment = sheet.strip()
            rows.extend(_parse_diffusion_sheet(df, segment, basis, cfg["monyy"]))
    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 rows from survey workbooks")
    table = pa.Table.from_pylist(rows, schema=DIFFUSION_SCHEMA)
    save_raw_parquet(table, node_id)


# ===========================================================================
# Agricultural Survey: 6 topic workbooks combined
# ===========================================================================
AGSURVEY_FILES = {
    "land_values": "/-/media/Documents/research/surveys/AgSurvey/data/agvalue.xlsx",
    "cash_rents": "/-/media/Documents/research/surveys/AgSurvey/data/agrents.xlsx",
    "credit_conditions": "/-/media/Documents/research/surveys/AgSurvey/data/agcredit.xlsx",
    "loan_volume": "/-/media/Documents/research/surveys/AgSurvey/data/agvolume.xlsx",
    "lending": "/-/media/Documents/research/surveys/AgSurvey/data/aglending.xlsx",
    "interest_rates": "/-/media/Documents/research/surveys/AgSurvey/data/agrates.xlsx",
}

AGSURVEY_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("topic", pa.string()),
    ("sheet", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])


def _parse_agsurvey_sheet(df: pd.DataFrame, topic: str, sheet: str):
    # Locate the row whose first cell is "Date".
    hrow = None
    for i in range(min(20, len(df))):
        if str(df.iloc[i, 0]).strip().lower() == "date":
            hrow = i
            break
    if hrow is None:
        return []
    sub = [str(x).strip() if not pd.isna(x) else "" for x in df.iloc[hrow].tolist()]
    # Group labels live in the row above; forward-fill across each group span.
    groups = [""] * len(sub)
    if hrow > 0:
        grow = df.iloc[hrow - 1].tolist()
        last = ""
        for ci, g in enumerate(grow):
            if not (g is None or (isinstance(g, float) and pd.isna(g))) and str(g).strip():
                last = str(g).strip()
            groups[ci] = last
    rows = []
    for _, r in df.iloc[hrow + 1:].iterrows():
        d = _parse_quarter(r.iloc[0])
        if d is None:
            continue
        for ci in range(1, len(sub)):
            label = sub[ci]
            if not label or label.lower() == "nan":
                continue
            val = _to_float(r.iloc[ci])
            if val is None:
                continue
            series = f"{groups[ci]} | {label}" if groups[ci] else label
            rows.append({"date": d, "topic": topic, "sheet": sheet, "series": series, "value": val})
    return rows


def fetch_agsurvey(node_id: str) -> None:
    rows = []
    for topic, url in AGSURVEY_FILES.items():
        xl = _excel(url)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, header=None)
            rows.extend(_parse_agsurvey_sheet(df, topic, sheet.strip()))
    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 rows from AgSurvey workbooks")
    table = pa.Table.from_pylist(rows, schema=AGSURVEY_SCHEMA)
    save_raw_parquet(table, node_id)


# ===========================================================================
# Trimmed Mean PCE inflation rate
# ===========================================================================
PCE_URL = "/~/media/documents/research/pce/pcehist"  # xlsx despite no extension
PCE_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("horizon", pa.string()),
    ("value", pa.float64()),
])


def fetch_pce(node_id: str) -> None:
    xl = _excel(PCE_URL)
    df = xl.parse(xl.sheet_names[0], header=None)
    # Find the header row carrying the '1-month' / '6-month' / '12-month' labels.
    hrow = None
    for i in range(min(15, len(df))):
        cells = [str(x).strip().lower() for x in df.iloc[i].tolist()]
        if "1-month" in cells:
            hrow = i
            break
    if hrow is None:
        raise AssertionError(f"{node_id}: could not locate PCE rate header row")
    header = [str(x).strip() if not pd.isna(x) else "" for x in df.iloc[hrow].tolist()]
    rows = []
    for _, r in df.iloc[hrow + 1:].iterrows():
        d = _to_date(r.iloc[0])
        if d is None:
            continue
        for ci in range(1, len(header)):
            horizon = header[ci]
            if not horizon or "month" not in horizon.lower():
                continue
            val = _to_float(r.iloc[ci])
            if val is None:
                continue
            rows.append({"date": d, "horizon": horizon, "value": val})
    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 PCE rows")
    table = pa.Table.from_pylist(rows, schema=PCE_SCHEMA)
    save_raw_parquet(table, node_id)


# ===========================================================================
# Weekly Economic Index
# ===========================================================================
WEI_URL = "/-/media/documents/research/wei/weekly-economic-index.xlsx"
WEI_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("wei", pa.float64()),
])


def fetch_wei(node_id: str) -> None:
    xl = _excel(WEI_URL)
    sheet = "2008-current" if "2008-current" in xl.sheet_names else xl.sheet_names[0]
    df = xl.parse(sheet, header=None)
    # Header row: first cell 'Date', second 'WEI'.
    hrow = None
    for i in range(min(10, len(df))):
        if str(df.iloc[i, 0]).strip().lower() == "date":
            hrow = i
            break
    if hrow is None:
        raise AssertionError(f"{node_id}: could not locate WEI header row")
    rows = []
    for _, r in df.iloc[hrow + 1:].iterrows():
        d = _to_date(r.iloc[0])
        val = _to_float(r.iloc[1])
        if d is None or val is None:
            continue
        rows.append({"date": d, "wei": val})
    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 WEI rows")
    table = pa.Table.from_pylist(rows, schema=WEI_SCHEMA)
    save_raw_parquet(table, node_id)


# ===========================================================================
# International House Price Database
# ===========================================================================
HOUSEPRICE_PAGE = "/research/international/houseprice"
HOUSEPRICE_DIR = "/-/media/Documents/research/international/houseprice/"
HOUSEPRICE_METRICS = {
    "HPI": "house_price_index",
    "RHPI": "real_house_price_index",
    "PDI": "personal_disposable_income",
    "RPDI": "real_personal_disposable_income",
}
HOUSEPRICE_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("metric", pa.string()),
    ("country", pa.string()),
    ("value", pa.float64()),
])


def _latest_houseprice_file() -> str:
    page = _fetch_bytes(HOUSEPRICE_PAGE).decode("utf-8", errors="replace")
    versions = re.findall(r"houseprice/hp(\d{4})\.xlsx", page, flags=re.IGNORECASE)
    if not versions:
        raise AssertionError("houseprice: no hpXXXX.xlsx release found on product page")
    latest = max(versions)  # YYMM string sorts chronologically
    return f"{HOUSEPRICE_DIR}hp{latest}.xlsx"


def fetch_houseprice(node_id: str) -> None:
    xl = _excel(_latest_houseprice_file())
    rows = []
    for sheet, metric in HOUSEPRICE_METRICS.items():
        if sheet not in xl.sheet_names:
            continue
        df = xl.parse(sheet, header=None)
        countries = [str(x).strip() if not pd.isna(x) else "" for x in df.iloc[0].tolist()]
        for _, r in df.iloc[2:].iterrows():
            d = _parse_quarter(r.iloc[0])
            if d is None:
                continue
            for ci in range(1, len(countries)):
                country = countries[ci]
                if not country or country.lower() == "nan":
                    continue
                val = _to_float(r.iloc[ci])
                if val is None:
                    continue
                rows.append({"date": d, "metric": metric, "country": country, "value": val})
    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 house-price rows")
    table = pa.Table.from_pylist(rows, schema=HOUSEPRICE_SCHEMA)
    save_raw_parquet(table, node_id)


# ===========================================================================
# DOWNLOAD_SPECS — one per entity-union entry
# ===========================================================================
DOWNLOAD_SPECS = [
    NodeSpec(id="dallas-fed-tmos", fn=fetch_diffusion, kind="download"),
    NodeSpec(id="dallas-fed-tssos", fn=fetch_diffusion, kind="download"),
    NodeSpec(id="dallas-fed-tros", fn=fetch_diffusion, kind="download"),
    NodeSpec(id="dallas-fed-bcs", fn=fetch_diffusion, kind="download"),
    NodeSpec(id="dallas-fed-des", fn=fetch_diffusion, kind="download"),
    NodeSpec(id="dallas-fed-agsurvey", fn=fetch_agsurvey, kind="download"),
    NodeSpec(id="dallas-fed-pce", fn=fetch_pce, kind="download"),
    NodeSpec(id="dallas-fed-wei", fn=fetch_wei, kind="download"),
    NodeSpec(id="dallas-fed-houseprice", fn=fetch_houseprice, kind="download"),
]
