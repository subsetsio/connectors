"""Federal Reserve Bank of San Francisco — research data indicators.

The SF Fed Economic Research department publishes a curated set of research data
indicators on its Data and Indicators index page. Each indicator is one Excel
workbook at a stable https://www.frbsf.org/wp-content/uploads/<name>.xlsx URL
(filenames are persistent across releases). There is no API and no bulk archive
— one file per indicator, fetched whole each refresh (stateless full re-pull;
the files are small, a few KB to ~600KB).

Each workbook holds one or more *data sheets* (plus free-text readme/methodology
sheets we skip). A data sheet is shaped as one index/date column followed by one
or more value columns, occasionally with a title/notes row above the header.
Schemas differ wildly across the 22 indicators and several workbooks carry
multiple distinct data sheets (weekly+monthly, quarterly+annual, per-region),
so the only faithful single-table representation per indicator is a generic
LONG melt: one row per (sheet, original-row, column). `row_idx` preserves the
original wide row, so the source layout is reconstructable losslessly by
pivoting on (sheet, row_idx). The transform is a thin parse-and-filter pass.
"""

import io
import math
import re
from datetime import date, datetime

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# entity slug -> canonical workbook URL (bare, no cache-busting query string).
# Verified live (HTTP 200, xlsx content-type) during implement probing.
FILE_URL = {
    "china-cyclical-activity-tracker": "https://www.frbsf.org/wp-content/uploads/ccat_data.xlsx",
    "cpi-inflation-contributions-from-goods-and-services": "https://www.frbsf.org/wp-content/uploads/cpi-contributors-data.xlsx",
    "cyclical-and-acyclical-core-pce-inflation": "https://www.frbsf.org/wp-content/uploads/cyclical-acyclical-core-pce-data.xlsx",
    "daily-news-sentiment-index": "https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx",
    "interest-rate-probability-distributions": "https://www.frbsf.org/wp-content/uploads/interest-rate-probability-distributions-data.xlsx",
    "labor-market-stress-indicator": "https://www.frbsf.org/wp-content/uploads/labor-market-stress-indicator-data.xlsx",
    "market-based-monetary-policy-uncertainty": "https://www.frbsf.org/wp-content/uploads/market-based-monetary-policy-uncertainty-data.xlsx",
    "monetary-policy-surprises": "https://www.frbsf.org/wp-content/uploads/monetary-policy-surprises-data.xlsx",
    "pandemic-era-excess-savings": "https://www.frbsf.org/wp-content/uploads/excess_savings_data.xlsx",
    "pce-inflation-contributions-from-goods-and-services": "https://www.frbsf.org/wp-content/uploads/pce-contributions-data.xlsx",
    "pce-personal-consumption-expenditure-price-index-pcepi": "https://www.frbsf.org/wp-content/uploads/pce-releases.xlsx",
    "proxy-funds-rate": "https://www.frbsf.org/wp-content/uploads/proxy-funds-rate-data.xlsx",
    "regional-indicators-for-labor-markets-and-prices": "https://www.frbsf.org/wp-content/uploads/regional-indicators-data.xlsx",
    "revisions-to-payroll-employment-gains": "https://www.frbsf.org/wp-content/uploads/revisions-to-payroll-employment-data.xlsx",
    "supply-and-demand-driven-pce-inflation": "https://www.frbsf.org/wp-content/uploads/supply-demand-pce-inflation.xlsx",
    "total-factor-productivity-tfp": "https://www.frbsf.org/wp-content/uploads/quarterly_tfp.xlsx",
    "treasury-yield-premiums": "https://www.frbsf.org/wp-content/uploads/FRBSF_Term_Web_Chart_Data.xlsx",
    "treasury-yield-skewness": "https://www.frbsf.org/wp-content/uploads/treasury-yield-skewness-data.xlsx",
    "twelfth-district-business-sentiment": "https://www.frbsf.org/wp-content/uploads/twelfth-district-business-sentiment-data.xlsx",
    "us-monetary-policy-event-study-database": "https://www.frbsf.org/wp-content/uploads/USMPD.xlsx",
    "weather-adjusted-employment-change": "https://www.frbsf.org/wp-content/uploads/weather-adjustment-time-series.xlsx",
    "zero-lower-bound-probabilities-at-different-time-horizons": "https://www.frbsf.org/wp-content/uploads/zero-lower-bound-probabilities-data.xlsx",
}

# Sheet names that are pure documentation, not data — skipped fast (the header
# detector would skip them anyway; this avoids parsing prose).
_DOC_SHEET_RE = re.compile(
    r"^(read\s*me|methodology|description|documentation|contents|notes?)\b", re.IGNORECASE
)

SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("row_idx", pa.int64()),       # 0-based row position within the sheet's data block
    ("period", pa.string()),       # raw label of the index (first) column
    ("period_date", pa.date32()),  # best-effort parse of period; null when not a date
    ("series", pa.string()),       # column header
    ("value", pa.float64()),       # numeric cell; null for text cells
    ("value_text", pa.string()),   # raw text cell; null for numeric cells
])


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _isblank(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.strip().lower() in ("", "nan"):
        return True
    return False


def _is_numeric(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return not (isinstance(v, float) and math.isnan(v))
    if isinstance(v, str):
        s = v.strip().replace(",", "")
        if s in ("", ".", "`"):
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False
    return False


_Q_RE = re.compile(r"^(\d{4})[\s:_-]*[qQ]([1-4])$")
_M_RE = re.compile(r"^(\d{4})[\s:_-]*[mM]([0-9]{1,2})$")
_MON_RE = re.compile(r"^([A-Za-z]{3,9})\.?\s+(\d{4})$")
_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def _parse_period_date(s: str):
    """Best-effort map of an index label to a calendar date. None when not datelike."""
    s = s.strip()
    if not s:
        return None
    # ISO date / datetime
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = _Q_RE.match(s)
    if m:
        return date(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)
    m = _M_RE.match(s)
    if m:
        mo = int(m.group(2))
        if 1 <= mo <= 12:
            return date(int(m.group(1)), mo, 1)
        return None
    m = _MON_RE.match(s)
    if m:
        mo = _MONTHS.get(m.group(1)[:3].lower())
        if mo:
            return date(int(m.group(2)), mo, 1)
        return None
    if re.fullmatch(r"\d{4}", s):  # bare year
        return date(int(s), 1, 1)
    return None


def _to_iso(v) -> str:
    if isinstance(v, (datetime, pd.Timestamp)):
        return v.date().isoformat() if hasattr(v, "date") else str(v)
    if isinstance(v, date):
        return v.isoformat()
    return str(v)


def _norm_cell(v):
    """Return (value_num, value_text) for a data cell."""
    if _isblank(v):
        return (None, None)
    if isinstance(v, bool):
        return (None, str(v))
    if isinstance(v, (int, float)):
        return (float(v), None)
    if isinstance(v, (datetime, date, pd.Timestamp)):
        return (None, _to_iso(v))
    s = str(v).strip()
    if s in ("", ".", "`") or s.lower() == "nan":
        return (None, None)
    try:
        return (float(s.replace(",", "")), None)
    except ValueError:
        return (None, s)


def _find_header(df: pd.DataFrame):
    """Index of the header row within the first 8 rows, or None if no data table."""
    n = min(8, len(df))
    for h in range(n):
        row = df.iloc[h].tolist()
        nonnull = [c for c in row if not _isblank(c)]
        if len(nonnull) < 2:
            continue
        textish = sum(1 for c in nonnull if isinstance(c, str))
        if textish < max(2, (len(nonnull) + 1) // 2):
            continue
        # Confirm a numeric appears below the header in a non-index column.
        for d in range(h + 1, min(h + 8, len(df))):
            drow = df.iloc[d].tolist()[1:]
            if any(_is_numeric(c) for c in drow):
                return h
        return None
    return None


def _dedup_headers(headers):
    out, seen = [], {}
    for j, hdr in enumerate(headers):
        name = "" if _isblank(hdr) else str(hdr).strip()
        if not name:
            name = f"column_{j}"
        if name in seen:
            seen[name] += 1
            name = f"{name} ({seen[name]})"
        else:
            seen[name] = 1
        out.append(name)
    return out


def _melt_workbook(content: bytes) -> dict:
    """Parse an xlsx into the long columnar dict matching SCHEMA."""
    cols = {k: [] for k in
            ("sheet", "row_idx", "period", "period_date", "series", "value", "value_text")}
    xls = pd.ExcelFile(io.BytesIO(content), engine="openpyxl")
    for sn in xls.sheet_names:
        if _DOC_SHEET_RE.match(sn.strip()):
            continue
        df = pd.read_excel(xls, sheet_name=sn, header=None, dtype=object)
        if df.empty:
            continue
        h = _find_header(df)
        if h is None:
            continue
        headers = _dedup_headers(df.iloc[h].tolist())
        if len(headers) < 2:
            continue
        ri = 0
        for _, raw in df.iloc[h + 1:].iterrows():
            cells = raw.tolist()
            if _isblank(cells[0]):
                continue
            period = _to_iso(cells[0]) if isinstance(cells[0], (datetime, date, pd.Timestamp)) else str(cells[0]).strip()
            if not period:
                continue
            pdate = _parse_period_date(period)
            emitted = False
            for j in range(1, len(headers)):
                cell = cells[j] if j < len(cells) else None
                vnum, vtext = _norm_cell(cell)
                if vnum is None and vtext is None:
                    continue
                cols["sheet"].append(sn)
                cols["row_idx"].append(ri)
                cols["period"].append(period)
                cols["period_date"].append(pdate)
                cols["series"].append(headers[j])
                cols["value"].append(vnum)
                cols["value_text"].append(vtext)
                emitted = True
            if emitted:
                ri += 1
    return cols


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len("sf-fed-"):]
    url = FILE_URL[slug]
    content = _download(url)
    cols = _melt_workbook(content)
    if not cols["series"]:
        raise AssertionError(f"{node_id}: no data rows parsed from {url}")
    table = pa.table(cols, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"sf-fed-{eid}", fn=fetch_one, kind="download")
    for eid in FILE_URL
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                sheet,
                row_idx,
                period,
                CAST(period_date AS DATE) AS date,
                series,
                value,
                value_text
            FROM "{s.id}"
            WHERE value IS NOT NULL OR value_text IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
