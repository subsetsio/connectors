"""Shared parsing for the Economic Policy Uncertainty (policyuncertainty.com) connector.

The source is ~55 heterogeneous Baker-Bloom-Davis data files (xlsx/xls/csv) served
under https://www.policyuncertainty.com/media/. Each file is its own time-series
table with an idiosyncratic layout: header offset by title/citation rows, dates as
separate Year/Month(/Day) columns, Year/Quarter, a single Date column, or period
strings like ``1998m1`` / ``2003M01``; wide (many index columns) or long (a country
key column); plus stray note/citation/glossary columns and notes sheets.

``parse_index_file`` normalises any of them to a uniform long shape
``[date DATE, series STRING, value DOUBLE]`` so every transform can be the same thin
cast-and-select SQL. Heavy, file-specific logic lives here (Python), never in SQL.
"""
import datetime as _dt
import re

import pandas as pd

DATE_TOKENS = {
    "year", "month", "day", "date", "datem", "quarter", "qtr", "time",
    "period", "observation_date", "yyyymm", "yearmonth",
}
_PERIOD_M = re.compile(r"^\s*(\d{4})[mM](\d{1,2})\s*$")
_PERIOD_Q = re.compile(r"^\s*(\d{4})[qQ](\d)\s*$")
_ISO = re.compile(r"^\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})")
_YM = re.compile(r"^\s*(\d{4})[-/](\d{1,2})\s*$")
_SLASH = re.compile(r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$")
_YEAR = re.compile(r"^\s*(\d{4})\s*$")
_THOUS = re.compile(r"^-?\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
_EUDEC = re.compile(r"^-?\d+,\d+$")


def _norm(x):
    if x is None:
        return ""
    s = str(x).strip()
    return "" if s == "" or s.lower() == "nan" else s.lower()


def _orig(x):
    if x is None:
        return ""
    s = str(x).strip()
    return "" if s.lower() == "nan" else s


def to_float(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        try:
            f = float(x)
            return None if f != f else f
        except (ValueError, OverflowError):
            return None
    s = str(x).strip().replace("−", "-").replace("%", "").strip()
    if s == "" or s.lower() == "nan":
        return None
    if _THOUS.match(s):
        s = s.replace(",", "")
    elif _EUDEC.match(s):
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _parse_scalar_date(v):
    if v is None:
        return None
    if isinstance(v, (pd.Timestamp, _dt.datetime, _dt.date)):
        try:
            return pd.Timestamp(v).date()
        except (ValueError, OverflowError):
            return None
    s = str(v).strip()
    if s == "" or s.lower() == "nan":
        return None
    m = _PERIOD_M.match(s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        return _dt.date(y, mo, 1) if 1 <= mo <= 12 else None
    m = _PERIOD_Q.match(s)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        return _dt.date(y, (q - 1) * 3 + 1, 1) if 1 <= q <= 4 else None
    m = _ISO.match(s)
    if m:
        try:
            return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = _YM.match(s)
    if m:
        mo = int(m.group(2))
        return _dt.date(int(m.group(1)), mo, 1) if 1 <= mo <= 12 else None
    m = _YEAR.match(s)
    if m:
        y = int(m.group(1))
        return _dt.date(y, 1, 1) if 1850 <= y <= 2100 else None
    return None  # slash dates handled at column level (ambiguous order)


def _is_datelike(v):
    return not isinstance(v, (int, float)) and _parse_scalar_date(v) is not None


def _col_datelike_frac(body, ci, limit=40):
    vals = [v for v in body[ci].tolist() if _norm(v) != ""][:limit]
    if not vals:
        return 0.0
    n = sum(1 for v in vals if _parse_scalar_date(v) is not None or _SLASH.match(str(v).strip()))
    return n / len(vals)


def _parse_date_column(values):
    """Parse a whole date column, resolving D/M/Y vs M/D/Y ambiguity from the
    column as a whole (US-origin site → default month-first when unresolved)."""
    parts = []
    for v in values:
        s = str(v).strip() if v is not None else ""
        m = _SLASH.match(s)
        if m:
            parts.append((int(m.group(1)), int(m.group(2))))
    order = "mdy"
    if parts:
        a_max = max(a for a, _ in parts)
        b_max = max(b for _, b in parts)
        if a_max > 12 and b_max <= 12:
            order = "dmy"
        elif b_max > 12 and a_max <= 12:
            order = "mdy"
        else:
            a_const1 = all(a == 1 for a, _ in parts)
            b_const1 = all(b == 1 for _, b in parts)
            order = "dmy" if (a_const1 and not b_const1) else "mdy"

    out = []
    for v in values:
        s = str(v).strip() if v is not None else ""
        m = _SLASH.match(s)
        if m:
            a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            mo, d = (b, a) if order == "dmy" else (a, b)
            try:
                out.append(_dt.date(y, mo, d) if 1 <= mo <= 12 and 1 <= d <= 31 else None)
            except ValueError:
                out.append(None)
        else:
            out.append(_parse_scalar_date(v))
    return pd.Series(out)


def _find_header(raw):
    n = min(len(raw), 25)
    for r in range(n):
        cells = [_norm(c) for c in raw.iloc[r].tolist()]
        if sum(1 for c in cells if c) < 2:
            continue
        if any(c in DATE_TOKENS or c.startswith("date") for c in cells):
            return r
    for r in range(1, n):
        if any(_is_datelike(v) or _SLASH.match(str(v).strip()) for v in raw.iloc[r].tolist()):
            return r - 1
    return None


def _roles(headers):
    roles = {}
    for ci, h in enumerate(headers):
        if not h:
            continue
        if h in ("date", "datem", "observation_date", "time", "period",
                 "yyyymm", "yearmonth") or h.startswith("date"):
            roles[ci] = "date"
        elif h == "year":
            roles[ci] = "year"
        elif h == "month":
            roles[ci] = "month"
        elif h == "day":
            roles[ci] = "day"
        elif h in ("quarter", "qtr"):
            roles[ci] = "quarter"
    return roles


def _build_dates(body, roles):
    ycols = [c for c, r in roles.items() if r == "year"]
    if ycols:
        y = pd.to_numeric(body[ycols[0]], errors="coerce")
        qcols = [c for c, r in roles.items() if r == "quarter"]
        mcols = [c for c, r in roles.items() if r == "month"]
        dcols = [c for c, r in roles.items() if r == "day"]
        if qcols:
            q = pd.to_numeric(body[qcols[0]], errors="coerce")
            m = (q - 1) * 3 + 1
        elif mcols:
            m = pd.to_numeric(body[mcols[0]], errors="coerce")
            nn = m.dropna()
            if len(nn) and nn.median() > 12:  # packed YYYYMM in the "month" column
                y, m = (m // 100), (m % 100)
        else:
            m = pd.Series([1] * len(body))
        d = pd.to_numeric(body[dcols[0]], errors="coerce") if dcols else pd.Series([1] * len(body))
        used = set(ycols) | set(qcols) | set(mcols) | set(dcols)
        out = []
        for yy, mm, dd in zip(y, m, d):
            try:
                out.append(_dt.date(
                    int(yy),
                    int(mm) if pd.notna(mm) and 1 <= int(mm) <= 12 else 1,
                    int(dd) if pd.notna(dd) and 1 <= int(dd) <= 31 else 1,
                ))
            except (ValueError, TypeError):
                out.append(None)
        return pd.Series(out), used

    date_ci = next((c for c, r in roles.items() if r == "date"), None)
    if date_ci is None:
        date_ci = next((c for c in roles if _col_datelike_frac(body, c) >= 0.6), None)
    if date_ci is None:
        date_ci = next((c for c in range(body.shape[1]) if _col_datelike_frac(body, c) >= 0.6), None)
    if date_ci is None:
        return None, set()
    return _parse_date_column(body[date_ci].tolist()), {date_ci}


def _parse_sheet(raw):
    hr = _find_header(raw)
    if hr is None:
        return []
    headers_lc = [_norm(c) for c in raw.iloc[hr].tolist()]
    headers_orig = [_orig(c) for c in raw.iloc[hr].tolist()]
    body = raw.iloc[hr + 1:].reset_index(drop=True)
    body.columns = range(body.shape[1])

    dates, datecols = _build_dates(body, _roles(headers_lc))
    if dates is None:
        return []

    n = len(body)
    measures, dims = [], []
    for ci in range(body.shape[1]):
        if ci in datecols or not headers_orig[ci]:
            continue
        nonnull = [v for v in body[ci].tolist() if _norm(v) != ""]
        if not nonnull:
            continue
        nnum = sum(1 for v in nonnull if to_float(v) is not None)
        if nnum >= 0.6 * len(nonnull):
            measures.append(ci)
        else:  # categorical key only if present on ~every row and genuinely multi-valued
            distinct = len(set(str(v).strip() for v in nonnull))
            if len(nonnull) >= 0.9 * n and 2 <= distinct <= 0.5 * len(nonnull):
                dims.append(ci)
    if not measures:
        return []

    multi_measure = len(measures) > 1
    dvals = dates.tolist()
    rows = []
    for i in range(n):
        dt = dvals[i] if i < len(dvals) else None
        if dt is None or isinstance(dt, float):
            continue
        dimvals = [str(body[ci].iloc[i]).strip() for ci in dims if _norm(body[ci].iloc[i]) != ""]
        for mi in measures:
            v = to_float(body[mi].iloc[i])
            if v is None:
                continue
            parts = list(dimvals)
            if multi_measure or not dimvals:
                parts.append(headers_orig[mi])
            series = " | ".join(p for p in parts if p)
            if series:
                rows.append((dt, series, v))
    return rows


def parse_index_file(content: bytes, filename: str):
    """Normalise one policyuncertainty.com data file (raw bytes) to a list of
    ``(date: datetime.date, series: str, value: float)`` tuples."""
    import io

    fn = filename.lower()
    if fn.endswith(".csv"):
        text = content.decode("utf-8", "replace")
        first = text.split("\n", 1)[0]
        sep = ";" if first.count(";") > first.count(",") else ","
        raw = pd.read_csv(io.StringIO(text), header=None, dtype=object, sep=sep,
                          keep_default_na=True, na_values=[""], on_bad_lines="skip")
        sheets = [raw]
    else:
        xl = pd.ExcelFile(io.BytesIO(content))
        sheets = [pd.read_excel(xl, sheet_name=s, header=None, dtype=object)
                  for s in xl.sheet_names]
        labels = list(xl.sheet_names)

    per = []
    for idx, raw in enumerate(sheets):
        try:
            r = _parse_sheet(raw)
        except Exception:
            r = []
        if r:
            label = "" if fn.endswith(".csv") else labels[idx]
            per.append((label, r))

    multi = len(per) > 1
    merged = {}
    for label, r in per:
        for d, s, v in r:
            key = (d, f"{label} :: {s}" if multi and label else s)
            merged[key] = v  # last write wins → de-dupes overlapping rows
    return [(d, s, v) for (d, s), v in merged.items()]
