"""Universal FRBSF indicator parser — wide-to-long melt. Tested in dev across all 22."""
import io, re
import pandas as pd
import numpy as np

META_SHEET = re.compile(r"(readme|methodolog|description|contents|notes|about|^info|cover|citation|legend|sources?)$", re.I)
DATE_HDR = re.compile(r"^(date|period|month|week|day|time|observation_date|quarter|year)$", re.I)

def _find_header_row(raw: pd.DataFrame, scan=12):
    """Return index of the header row: first row (within scan) whose first ~4 cells
    contain a 'date'-like label. Fallback 0."""
    for i in range(min(scan, len(raw))):
        cells = [str(c).strip() for c in raw.iloc[i, :4].tolist()]
        if any(DATE_HDR.match(c) for c in cells if c and c != "nan"):
            return i
    return 0

def _parse_period(series: pd.Series):
    """Return (date_series[date|NaT], ok_fraction). Handles real dates, ISO strings,
    'YYYY:Qn'/'YYYYQn' quarters, bare 'YYYY' years, 'YYYYmMM' months."""
    s = series.astype("string").str.strip()
    # try straight datetime first
    dt = pd.to_datetime(series, errors="coerce")
    out = dt.copy()
    miss = out.isna() & s.notna()
    if miss.any():
        for idx in np.where(miss.to_numpy())[0]:
            v = s.iloc[idx]
            if v is pd.NA or v is None: continue
            m = re.match(r"^(\d{4})[:\-]?[Qq]([1-4])$", v)
            if m:
                yr, q = int(m.group(1)), int(m.group(2)); out.iloc[idx] = pd.Timestamp(yr, (q-1)*3+1, 1); continue
            m = re.match(r"^(\d{4})[:\-]?[Mm]?(\d{1,2})$", v)
            if m and 1 <= int(m.group(2)) <= 12 and len(v) > 4:
                out.iloc[idx] = pd.Timestamp(int(m.group(1)), int(m.group(2)), 1); continue
            m = re.match(r"^(\d{4})(\.0)?$", v)
            if m:
                out.iloc[idx] = pd.Timestamp(int(m.group(1)), 1, 1); continue
    ok = out.notna().sum() / max(1, s.notna().sum())
    return out, ok

def parse_workbook(content: bytes, file_stem: str):
    """Yield long rows: dict(sheet, period, date, dimension, series, value)."""
    xl = pd.ExcelFile(io.BytesIO(content))
    rows = []
    for sh in xl.sheet_names:
        if META_SHEET.search(sh.strip()):
            continue
        raw = xl.parse(sh, header=None)
        if raw.empty or raw.shape[1] < 2:
            continue
        hr = _find_header_row(raw)
        header = [str(c).strip() for c in raw.iloc[hr].tolist()]
        body = raw.iloc[hr+1:].reset_index(drop=True)
        body.columns = range(body.shape[1])
        # drop fully-empty trailing cols/rows
        period_raw = body[0].astype("string").str.strip()
        keep = period_raw.notna() & (period_raw != "") & (period_raw.str.lower() != "nan")
        body = body[keep.to_numpy()].reset_index(drop=True)
        if body.empty:
            continue
        period_raw = body[0].astype("string").str.strip()
        date_parsed, ok = _parse_period(body[0])
        if ok < 0.5:  # first column isn't a time axis -> not a data sheet we understand
            continue
        sheet_tag = sh.strip() if len(xl.sheet_names) == 1 else f"{file_stem}:{sh.strip()}"
        n = len(body)
        is_panel = period_raw.duplicated(keep=False).sum() > 0.3 * n  # many repeated periods -> panel
        # classify other columns
        value_cols, dim_cols = [], []
        for ci in range(1, body.shape[1]):
            name = header[ci] if ci < len(header) else f"col{ci}"
            if not name or name.lower() in ("nan", "none", ""):
                name = f"col{ci}"
            col = body[ci]
            num = pd.to_numeric(col, errors="coerce")
            numfrac = num.notna().sum() / max(1, col.notna().sum())
            if numfrac >= 0.6:
                value_cols.append((ci, name, num))
            else:
                dim_cols.append((ci, name, col.astype("string")))
        # build dimension string (only meaningful for panels; drop notes/text in wide)
        if is_panel and dim_cols:
            dim_series = dim_cols[0][2]  # first text col is the dimension (e.g. state)
        else:
            dim_series = pd.Series([pd.NA]*n, dtype="string")
        for ci, name, num in value_cols:
            for i in range(n):
                v = num.iloc[i]
                if pd.isna(v):
                    continue
                d = date_parsed.iloc[i]
                rows.append({
                    "sheet": sheet_tag,
                    "period": period_raw.iloc[i] if period_raw.iloc[i] is not pd.NA else None,
                    "date": None if pd.isna(d) else d.date(),
                    "dimension": None if dim_series.iloc[i] is pd.NA else str(dim_series.iloc[i]),
                    "series": name,
                    "value": float(v),
                })
    return rows
