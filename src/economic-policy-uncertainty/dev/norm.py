"""Universal normalizer for policyuncertainty.com files -> long (date, series, value, frequency).

The source is ~55 heterogeneous Excel/CSV files: Year/Month component columns,
single date columns in many formats (ISO, 1993m1, 2003M01, dd/mm/yyyy, 199501),
annual and quarterly data, multi-sheet workbooks, leading citation/preamble rows,
NaN-named header rows, and already-long layouts with a categorical dimension.

Strategy: locate the header row (by date-ish token, else by the first row that
holds a real date + a number), build a date from whatever the file provides,
then melt the numeric columns to long form. Already-long files (a date that
repeats) keep their string dimension columns folded into the series label.
"""
import csv
import io
import math
import re
import datetime as _dt

import pandas as pd

# whole-cell header tokens (plus startswith 'date' and 'time'/'quarter')
HEADER_TOKENS = {"year", "month", "day", "date", "time", "quarter"}
# names that are date-components, never value series
DATE_NAME_EXCLUDE = {
    "year", "month", "day", "quarter", "cmonth", "datem", "date", "time",
    "period", "monthly", "yearmonth", "ym", "semester", "week",
}
_YYYYMM_RE = re.compile(r"^(\d{4})m(\d{1,2})$", re.I)
_YYYYMM6_RE = re.compile(r"^\d{6}$")


def _coerce_date(x):
    """Scalar -> pd.Timestamp or None, across every date format the source uses."""
    if x is None:
        return None
    if isinstance(x, (pd.Timestamp, _dt.datetime, _dt.date)):
        try:
            if pd.isna(x):
                return None
        except (TypeError, ValueError):
            pass
        return pd.Timestamp(x)
    if isinstance(x, float) and math.isnan(x):
        return None
    s = str(x).strip()
    if not s or s.lower() in ("nan", "nat", "none"):
        return None
    m = _YYYYMM_RE.match(s)
    if m:
        mo = int(m.group(2))
        if 1 <= mo <= 12:
            return pd.Timestamp(int(m.group(1)), mo, 1)
    if _YYYYMM6_RE.match(s):
        y, mo = int(s[:4]), int(s[4:6])
        if 1850 <= y <= 2100 and 1 <= mo <= 12:
            return pd.Timestamp(y, mo, 1)
    ts = pd.to_datetime(s, errors="coerce")
    if pd.isna(ts):
        ts = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if pd.isna(ts) or ts.year < 1850 or ts.year > 2100:
        return None
    return ts


def _coerce_float(x):
    if x is None:
        return None
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return None if (isinstance(x, float) and math.isnan(x)) else float(x)
    s = str(x).strip().replace(",", "")
    if not s or s.lower() in ("nan", "nat", "none"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date_series(s: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(s):
        return pd.to_datetime(s, errors="coerce")
    return pd.to_datetime(s.map(_coerce_date), errors="coerce")


def _read_sheets(content: bytes, filename: str):
    low = filename.lower()
    if low.endswith(".csv"):
        text = content.decode("utf-8", "replace")
        # sniff delimiter: some files are ';'-delimited with decimal commas
        sample = [l for l in text.splitlines() if l.strip()][:5]
        semic = sum(l.count(";") for l in sample)
        comma = sum(l.count(",") for l in sample)
        if semic > comma and semic > 0:
            delim, decimal_comma = ";", True
        else:
            delim, decimal_comma = ",", False
        rows = list(csv.reader(io.StringIO(text), delimiter=delim))
        if not rows:
            return [("csv", pd.DataFrame())]
        if decimal_comma:
            rows = [[(c.replace(",", ".") if isinstance(c, str) else c) for c in r] for r in rows]
        maxc = max(len(r) for r in rows)
        rows = [r + [None] * (maxc - len(r)) for r in rows]
        return [("csv", pd.DataFrame(rows))]
    engine = "xlrd" if low.endswith(".xls") else "openpyxl"
    xl = pd.ExcelFile(io.BytesIO(content), engine=engine)
    return [(sh, xl.parse(sh, header=None)) for sh in xl.sheet_names]


def _header_cell_match(cell) -> bool:
    s = str(cell).strip().lower()
    return s in HEADER_TOKENS or s.startswith("date")


def _locate_header(raw: pd.DataFrame):
    n = min(len(raw), 30)
    for i in range(n):
        if any(_header_cell_match(c) for c in raw.iloc[i].tolist()):
            return i, i + 1
    # value-based fallback: first row carrying a real date AND a number
    for r in range(n):
        row = raw.iloc[r].tolist()
        nd = sum(1 for x in row if _coerce_date(x) is not None)
        nn = sum(1 for x in row if _coerce_float(x) is not None)
        if nd >= 1 and nn >= 1:
            return (r - 1 if r >= 1 else None), r
    return None, None


def _mk_header(row, ncols):
    names, seen = [], {}
    for i in range(ncols):
        v = row[i] if i < len(row) else None
        s = "" if v is None else str(v).strip()
        if not s or s.lower() in ("nan", "nat"):
            s = f"col{i}"
        if s in seen:
            seen[s] += 1
            s = f"{s}.{seen[s]}"
        else:
            seen[s] = 0
        names.append(s)
    return names


def _first(cols, lc, name):
    return next((c for c in cols if lc[c] == name), None)


def _build_date(data, lc, cols):
    """Return (date_series, {used_cols}, frequency) or None."""
    yc, mc, dc, qc = (_first(cols, lc, k) for k in ("year", "month", "day", "quarter"))
    if yc is not None:
        y = pd.to_numeric(data[yc], errors="coerce")
        yv = y.dropna()
        if len(yv) and yv.between(1850, 2100).mean() >= 0.8:
            used = {yc}
            m = pd.to_numeric(data[mc], errors="coerce") if mc is not None else None
            if m is not None and m.dropna().between(1, 12).mean() < 0.8:
                m = None
            if m is not None:
                used.add(mc)
                if dc is not None:
                    d = pd.to_numeric(data[dc], errors="coerce")
                    if d.dropna().between(1, 31).mean() >= 0.8:
                        used.add(dc)
                        return (pd.to_datetime(dict(year=y, month=m, day=d), errors="coerce"),
                                used, "daily")
                return (pd.to_datetime(dict(year=y, month=m, day=1), errors="coerce"),
                        used, "monthly")
            if qc is not None:
                q = pd.to_numeric(data[qc], errors="coerce")
                if q.dropna().between(1, 4).mean() >= 0.8:
                    used.add(qc)
                    return (pd.to_datetime(dict(year=y, month=(q - 1) * 3 + 1, day=1),
                                           errors="coerce"), used, "quarterly")
            # year only -> annual, only when year is (near) unique
            if len(yv) and yv.duplicated().mean() < 0.05:
                return (pd.to_datetime(dict(year=y, month=1, day=1), errors="coerce"),
                        used, "annual")
    # single date-bearing column
    order = []
    for c in cols:
        n = lc[c]
        if "date" in n or n in DATE_NAME_EXCLUDE or n.startswith("date"):
            order.append(c)
    if cols and cols[0] not in order:
        order.append(cols[0])
    for c in order:
        parsed = _parse_date_series(data[c])
        present = data[c].notna().sum()
        # fraction over non-null cells (a glued side-table can inflate row count)
        if present < 10 or (parsed.notna().sum() / present) < 0.8:
            continue
        yrs = parsed.dropna().dt.year
        if len(yrs) == 0 or yrs.between(1850, 2100).mean() < 0.9:
            continue
        is_daily = bool((parsed.dropna().dt.day != 1).any())
        return parsed, {c}, ("daily" if is_daily else "monthly")
    return None


def _norm_sheet(raw: pd.DataFrame):
    if raw is None or raw.empty:
        return None
    header_row, data_start = _locate_header(raw)
    if data_start is None:
        return None
    ncols = raw.shape[1]
    if header_row is None:
        names = [f"col{i}" for i in range(ncols)]
    else:
        names = _mk_header(raw.iloc[header_row].tolist(), ncols)
    data = raw.iloc[data_start:].copy()
    data.columns = names
    cols = list(data.columns)
    lc = {c: str(c).strip().lower() for c in cols}

    built = _build_date(data, lc, cols)
    if built is None:
        return None
    date, date_used, freq = built

    # Drop glued side-tables: truncate at the first blank-header ('colN') column
    # that follows the date column(s). Keeps the date+value block, sheds vocab/
    # note tables pasted to the right under empty headers.
    blanks = [i for i, c in enumerate(cols) if re.fullmatch(r"col\d+", str(c))]
    date_idx = [cols.index(c) for c in date_used if c in cols]
    max_d = max(date_idx) if date_idx else -1
    trunc = next((b for b in blanks if b > max_d), None)
    keep = cols if trunc is None else cols[:trunc]

    cand = [c for c in keep if c not in date_used and lc[c] not in DATE_NAME_EXCLUDE]
    numeric, value_cols, string_cols = {}, [], []
    for c in cand:
        num = pd.to_numeric(data[c], errors="coerce")
        present = data[c].notna().sum()
        ratio = (num.notna().sum() / present) if present else 0.0
        numeric[c] = num
        (value_cols if ratio >= 0.5 else string_cols).append(c)
    if not value_cols:
        return None

    date_is_long = bool(date.dropna().duplicated().any())
    dim_cols = string_cols if (date_is_long and string_cols) else []
    if dim_cols:
        prefix = data[dim_cols].astype(str).apply(
            lambda r: " | ".join(x for x in r if x and x.lower() != "nan"), axis=1
        )
    else:
        prefix = None

    frames = []
    for c in value_cols:
        if dim_cols:
            series = prefix.map(lambda p, c=c: f"{p} | {c}" if p else str(c))
        else:
            series = pd.Series(str(c), index=data.index)
        frames.append(pd.DataFrame({"date": date, "series": series, "value": numeric[c]}))
    out = pd.concat(frames, ignore_index=True).dropna(subset=["date", "value"])
    if out.empty:
        return None
    out["frequency"] = freq
    return out


def normalize(content: bytes, filename: str) -> pd.DataFrame:
    sheets = _read_sheets(content, filename)
    parsed = []
    for name, raw in sheets:
        try:
            res = _norm_sheet(raw)
        except Exception as e:
            raise RuntimeError(f"sheet {name!r}: {type(e).__name__}: {e}")
        if res is not None and len(res):
            parsed.append((name, res))
    if not parsed:
        raise ValueError(f"{filename}: no parseable (date, value) data found")
    multi = len(parsed) > 1
    out = []
    for name, df in parsed:
        if multi:
            df = df.copy()
            df["series"] = f"{str(name).strip()} | " + df["series"].astype(str)
        out.append(df)
    final = pd.concat(out, ignore_index=True)
    final["date"] = pd.to_datetime(final["date"]).dt.date
    final["series"] = final["series"].astype(str)
    final["value"] = pd.to_numeric(final["value"], errors="coerce").astype(float)
    final = final.dropna(subset=["value"])
    return final[["date", "series", "value", "frequency"]]
