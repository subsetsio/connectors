"""Shared helpers for the Bank of Jamaica (jm-boj) connector.

BOJ publishes one Excel workbook per statistical dataset under /wp-content/
uploads/, linked from the /statistics/ leaf pages. There is no catalog API and
no machine-readable schema; the workbooks are hand-laid spreadsheets. They do,
however, share a standardized house style:

  * a metadata header block (Table Code / Category / Table Name / Data Range /
    Frequency / Units / Updated),
  * a clean data sheet (usually named exactly after the dataset code, sometimes
    split into code-prefixed sub-sheets like FS.CB.05.TOT / .DCD / .FCD or
    FS.MA.04 "Uses of Funds" / "Sources of Funds"),
  * a data region that is EITHER date-down-rows + series-across-columns
    (the common case) OR transposed: dates-across + metrics-down-rows
    (balance-of-payments / external-debt / reserve-template style).

`parse_workbook` melts whichever layout it finds into a uniform long table of
(date, subtable, series, value) plus workbook-level frequency / unit, so every
dataset publishes the same tidy shape and the differentiation lives in the
`series` (and `subtable`) values. This is a best-effort generic melt — it
prioritises never dropping data over perfectly clean labels.
"""

import io
import re
import datetime

import pandas as pd
import pyarrow as pa

from subsets_utils import get, transient_retry

BASE = "https://boj.org.jm"

# (sector, category) -> statistics leaf page that links the workbook.
LEAF = {
    ("FS", "CB"): "/statistics/financial-sector/commercial-banks/",
    ("FS", "BS"): "/statistics/financial-sector/building-societies-data/",
    ("FS", "MB"): "/statistics/financial-sector/merchant-banks-data/",
    ("FS", "CU"): "/statistics/financial-sector/credit-unions-data/",
    ("FS", "OFC"): "/statistics/financial-sector/other-financial-corporations/",
    ("FS", "MA"): "/statistics/financial-sector/monetary-authorities/",
    ("FS", "MCM"): "/statistics/financial-sector/money-capital-market/",
    ("FS", "DTI"): "/statistics/financial-sector/banking-system/",
    ("ES", "NIR"): "/statistics/external-sector/official-international-reserves/",
    ("ES", "BOP"): "/statistics/external-sector/balance-of-payments/",
    ("ES", "RMT"): "/statistics/external-sector/remittances/",
    ("ES", "FDI"): "/statistics/external-sector/foreign-direct-investments/",
    ("ES", "IIP"): "/statistics/external-sector/international-investment-position/",
    ("ES", "EXD"): "/statistics/external-sector/external-debt/",
    ("IR", "CB"): "/statistics/interest-rates/commercial-banks-interest-rates/",
    ("IR", "BS"): "/statistics/interest-rates/building-societies-interest-rates/",
    ("IR", "MB"): "/statistics/interest-rates/merchant-banks-interest-rates/",
    ("IR", "BOJ"): "/statistics/interest-rates/bank-of-jamaica-rates/",
    ("IR", "GOJ"): "/statistics/interest-rates/government-of-jamaica-rates/",
    ("IR", "PMM"): "/statistics/interest-rates/private-money-market-rates/",
    ("RS", "CPI"): "/statistics/real-sector/consumer-price-indices/",
    ("RS", "INF"): "/statistics/real-sector/inflation/",
    ("FX", "FCA"): "/statistics/foreign-exchange/",
    ("FX", "FLW"): "/statistics/foreign-exchange/",
    ("FX", "BFXITT"): "/statistics/foreign-exchange/",
}

_BLOCK_SHEETS = {
    "notes", "note", "chart", "charts", "graph", "graphs", "sheet1", "sheet2",
    "sheet3", "sheet4", "sheet5", "sheet6", "sheet7", "",
}

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
    "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Workbook schema: one long row per (date, subtable, series).
SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("subtable", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
    ("frequency", pa.string()),
    ("unit", pa.string()),
])


def _norm(s):
    return re.sub(r"[ _]", "", str(s)).strip().lower()


@transient_retry()
def http_get(url, **kwargs):
    kwargs.setdefault("timeout", (10.0, 120.0))
    resp = get(url, **kwargs)
    resp.raise_for_status()
    return resp


def leaf_for(code):
    sector, cat, _nn = code.split(".")
    return BASE + LEAF[(sector, cat)]


def resolve_workbook_url(code, page_html):
    """Find the .xls/.xlsx href on a leaf page whose basename matches the code.

    Tolerates the WordPress-sanitised trailing underscore (IR.PMM_.00) and the
    descriptive-suffix filenames (IR.CB.01-Commercial-Banks-...xls).
    """
    sector, cat, nn = code.split(".")
    rx = re.compile(rf"^{sector}\.{cat}_?\.{nn}([-.]|$)", re.I)
    for href in re.findall(r'href="([^"]*\.xlsx?)"', page_html, re.I):
        base = href.rsplit("/", 1)[-1]
        if rx.match(base):
            return (BASE + href) if href.startswith("/") else href
    raise RuntimeError(f"{code}: no matching workbook href found on leaf page")


# ---- cell coercion ---------------------------------------------------------

def _to_float(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        return None if pd.isna(f) else f
    if isinstance(v, str):
        s = v.strip().replace(",", "")
        if s in ("", "-", "--", "...", "..", "n/a", "na", "nil", "*", "**"):
            return None
        s = s.rstrip("*").strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None


def _to_date(v):
    if isinstance(v, (pd.Timestamp, datetime.datetime, datetime.date)):
        try:
            return pd.Timestamp(v).date()
        except (ValueError, OverflowError):
            return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        f = float(v)
        if not pd.isna(f) and f.is_integer() and 1900 <= f <= 2100:
            return datetime.date(int(f), 1, 1)
        return None
    if isinstance(v, str):
        s = v.strip()
        if re.fullmatch(r"(19|20)\d{2}", s):
            return datetime.date(int(s), 1, 1)
        m = re.fullmatch(r"([A-Za-z]{3,9})\.?[\s\-/]+((?:19|20)?\d{2})", s)
        if m:
            mo = _MONTHS.get(m.group(1)[:3].lower())
            if mo:
                y = int(m.group(2))
                if y < 100:
                    y += 2000 if y < 50 else 1900
                return datetime.date(y, mo, 1)
        m = re.match(r"((?:19|20)\d{2})[-/](\d{1,2})", s)
        if m:
            mo = int(m.group(2))
            if 1 <= mo <= 12:
                return datetime.date(int(m.group(1)), mo, 1)
    return None


def _year_only(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        if not pd.isna(f) and f.is_integer() and 1900 <= f <= 2100:
            return int(f)
    if isinstance(v, str) and re.fullmatch(r"(19|20)\d{2}", v.strip()):
        return int(v.strip())
    return None


def _month_only(v):
    if isinstance(v, str):
        m = re.fullmatch(r"([A-Za-z]{3,9})\.?", v.strip())
        if m:
            return _MONTHS.get(m.group(1)[:3].lower())
    return None


# ---- header / orientation --------------------------------------------------

_PERIOD_LABELS = {
    "date", "end of period", "period", "as at", "month", "month/year",
    "announcement date", "effective date", "year",
}


def _clean_label(s):
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    return re.sub(r"\s+", " ", str(s).replace("\n", " ")).strip()


def _melt_vertical(df, header_row, first_data, hierarchical):
    """dates down col0, series across columns."""
    ncols = df.shape[1]
    # Build series labels by joining header rows between header_row and data.
    labels = {}
    for c in range(1, ncols):
        parts = []
        for r in range(header_row, first_data):
            txt = _clean_label(df.iat[r, c])
            if txt and txt.lower() != "nan" and txt not in parts:
                parts.append(txt)
        labels[c] = " - ".join(parts) if parts else f"column_{c}"

    rows = []
    cur_year = None
    for r in range(first_data, len(df)):
        c0 = df.iat[r, 0]
        d = None
        if hierarchical:
            mo = _month_only(c0)
            if mo is not None and cur_year is not None:
                d = datetime.date(cur_year, mo, 1)
            else:
                y = _year_only(c0)
                if y is not None:
                    cur_year = y
                    continue
                d = _to_date(c0)
        else:
            d = _to_date(c0)
        if d is None:
            continue
        for c in range(1, ncols):
            val = _to_float(df.iat[r, c])
            if val is None:
                continue
            rows.append((d, labels[c], val))
    return rows


def _melt_horizontal(df, date_row):
    """transposed: dates across `date_row`, metric labels down col0."""
    ncols = df.shape[1]
    date_cols = {}
    for c in range(1, ncols):
        d = _to_date(df.iat[date_row, c])
        if d is not None:
            date_cols[c] = d
    rows = []
    for r in range(date_row + 1, len(df)):
        label = ""
        for lc in range(0, min(3, ncols)):
            t = _clean_label(df.iat[r, lc])
            if t and t.lower() != "nan":
                label = t
                break
        if not label:
            continue
        for c, d in date_cols.items():
            val = _to_float(df.iat[r, c])
            if val is None:
                continue
            rows.append((d, label, val))
    return rows


def _date_rows(df, hierarchical):
    """row indices in col0 that carry a usable date."""
    out = []
    cur_year = None
    for r in range(len(df)):
        c0 = df.iat[r, 0]
        if hierarchical:
            mo = _month_only(c0)
            if mo is not None and cur_year is not None:
                out.append(r)
                continue
            y = _year_only(c0)
            if y is not None:
                cur_year = y
                continue
            if _to_date(c0) is not None:
                out.append(r)
        elif _to_date(c0) is not None:
            out.append(r)
    return out


def _melt_sheet(df):
    if df.shape[0] < 2 or df.shape[1] < 2:
        return []
    df = df.reset_index(drop=True)

    has_month_only = any(_month_only(df.iat[r, 0]) is not None for r in range(len(df)))

    vrows = _date_rows(df, has_month_only)
    # horizontal score: row with the most date cells across columns
    best_hrow, best_hcount = None, 0
    for r in range(min(60, len(df))):
        cnt = sum(1 for c in range(1, df.shape[1]) if _to_date(df.iat[r, c]) is not None)
        if cnt > best_hcount:
            best_hrow, best_hcount = r, cnt

    use_vertical = len(vrows) >= 3 and len(vrows) >= best_hcount
    if use_vertical:
        first_data = vrows[0]
        # locate the header row: a labelled period row above the data, else the
        # nearest non-empty (cols>=1) row above the first data row.
        header_row = None
        for r in range(first_data - 1, -1, -1):
            if _clean_label(df.iat[r, 0]).lower() in _PERIOD_LABELS:
                header_row = r
                break
        if header_row is None:
            for r in range(first_data - 1, -1, -1):
                if any(_clean_label(df.iat[r, c]) for c in range(1, df.shape[1])):
                    header_row = r
                    break
        if header_row is None:
            header_row = max(0, first_data - 1)
        return _melt_vertical(df, header_row, first_data, has_month_only)

    if best_hcount >= 3:
        return _melt_horizontal(df, best_hrow)

    # last resort: vertical with whatever date rows exist
    if vrows:
        return _melt_vertical(df, max(0, vrows[0] - 1), vrows[0], has_month_only)
    return []


def _extract_meta(df):
    meta = {"frequency": None, "unit": None}
    pairs = [("frequency", "frequency:"), ("unit", "units:")]
    for r in range(min(16, len(df))):
        for c in range(min(2, df.shape[1])):
            cell = df.iat[r, c]
            if not isinstance(cell, str):
                continue
            s = cell.strip()
            low = s.lower()
            for key, lab in pairs:
                if low.startswith(lab):
                    val = s[len(lab):].strip()
                    if not val and c + 1 < df.shape[1]:
                        nxt = df.iat[r, c + 1]
                        val = str(nxt).strip() if pd.notna(nxt) else ""
                    if val and val.lower() != "nan":
                        meta[key] = val
    return meta


def _subtable_label(code, sheet_name):
    rem = re.sub(r"[ _]", "", sheet_name)
    pref = re.sub(r"[ _]", "", code)
    if rem.lower().startswith(pref.lower()):
        tail = sheet_name
        # strip the code prefix from the original (case-insensitive) name
        m = re.match(re.escape(code) + r"[ _.]*", sheet_name, re.I)
        if m:
            tail = sheet_name[m.end():]
        return _clean_label(tail)
    return ""


def parse_workbook(code, raw_bytes, is_xlsx):
    """Return a pyarrow.Table of long (date, subtable, series, value, ...) rows."""
    engine = "openpyxl" if is_xlsx else "xlrd"
    xls = pd.ExcelFile(io.BytesIO(raw_bytes), engine=engine)

    prefixed = [s for s in xls.sheet_names if _norm(s).startswith(_norm(code))]
    meta_df = None
    melted = []  # (subtable, [(date, series, value)])

    if prefixed:
        for sh in prefixed:
            df = pd.read_excel(xls, sheet_name=sh, header=None)
            if meta_df is None:
                meta_df = df
            rows = _melt_sheet(df)
            if rows:
                melted.append((_subtable_label(code, sh), rows))

    if not melted:
        # no usable code-prefixed sheet: melt the single richest data sheet.
        cands = [s for s in xls.sheet_names if _norm(s) not in _BLOCK_SHEETS]
        best, best_rows = None, []
        for sh in cands:
            df = pd.read_excel(xls, sheet_name=sh, header=None)
            rows = _melt_sheet(df)
            if len(rows) > len(best_rows):
                best, best_rows, best_df = sh, rows, df
        if best is not None and best_rows:
            meta_df = best_df
            melted.append(("", best_rows))

    meta = _extract_meta(meta_df) if meta_df is not None else {"frequency": None, "unit": None}

    # dedup on (subtable, date, series) keeping the last value seen.
    dedup = {}
    for sub, rows in melted:
        for d, series, val in rows:
            dedup[(sub, d, series)] = val

    dates, subs, sers, vals = [], [], [], []
    for (sub, d, series), val in dedup.items():
        dates.append(d)
        subs.append(sub)
        sers.append(series)
        vals.append(val)

    n = len(dates)
    return pa.table({
        "date": pa.array(dates, pa.date32()),
        "subtable": pa.array(subs, pa.string()),
        "series": pa.array(sers, pa.string()),
        "value": pa.array(vals, pa.float64()),
        "frequency": pa.array([meta["frequency"]] * n, pa.string()),
        "unit": pa.array([meta["unit"]] * n, pa.string()),
    }, schema=SCHEMA)
