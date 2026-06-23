"""Universal FRBSF indicator parser — wide-to-long melt. Tested across all 22 indicators."""
import io, re
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

META_SHEET = re.compile(r"(readme|methodolog|description|contents?|notes|about|^info|cover|citation|legend|sources?|disclaimer)", re.I)
DATE_HDR = re.compile(r"(date|period|month|week|quarter|release|observation)", re.I)

def _parse_period_strings(str_series: pd.Series):
    """Parse a string Series into dates. Operates ONLY on string form so plain
    integers are never misread as nanosecond epochs. Handles ISO datetimes,
    'YYYY:Qn'/'YYYYQn', 'YYYYmMM', bare 'YYYY'. Returns (date Series, ok_frac)."""
    s = str_series
    out = pd.to_datetime(s, errors="coerce", format="mixed")
    miss = out.isna() & s.notna() & (s.str.strip() != "")
    for idx in np.where(miss.to_numpy())[0]:
        v = str(s.iloc[idx]).strip()
        m = re.match(r"^(\d{4})[:\-]?[Qq]([1-4])$", v)
        if m:
            out.iloc[idx] = pd.Timestamp(int(m.group(1)), (int(m.group(2))-1)*3+1, 1); continue
        m = re.match(r"^(\d{4})[:\-]?[Mm](\d{1,2})$", v)
        if m and 1 <= int(m.group(2)) <= 12:
            out.iloc[idx] = pd.Timestamp(int(m.group(1)), int(m.group(2)), 1); continue
        m = re.match(r"^(19|20)\d{2}$", v)        # bare 4-digit year
        if m:
            out.iloc[idx] = pd.Timestamp(int(v), 1, 1); continue
    nonblank = (s.notna() & (s.str.strip() != "")).sum()
    ok = out.notna().sum() / max(1, nonblank)
    return out, ok

def _as_str(col: pd.Series) -> pd.Series:
    return col.astype("string").str.strip()

def parse_workbook(content: bytes, file_stem: str):
    """Yield long rows: dict(sheet, period, date, dimension, series, value)."""
    xl = pd.ExcelFile(io.BytesIO(content))
    rows = []
    multi = len(xl.sheet_names) > 1
    for sh in xl.sheet_names:
        if META_SHEET.search(sh.strip()):
            continue
        raw = xl.parse(sh, header=None)
        if raw.empty or raw.shape[1] < 2:
            continue
        # Detect header row: first of the first ~15 rows whose cells include a
        # date-ish name, else the first row that has >=2 non-null cells.
        hr = None
        for i in range(min(15, len(raw))):
            cells = [str(c).strip() for c in raw.iloc[i].tolist()]
            if any(DATE_HDR.search(c) for c in cells if c and c.lower() != "nan"):
                hr = i; break
        if hr is None:
            for i in range(min(15, len(raw))):
                if raw.iloc[i].notna().sum() >= 2:
                    hr = i; break
        if hr is None:
            continue
        header = [str(c).strip() for c in raw.iloc[hr].tolist()]
        body = raw.iloc[hr+1:].reset_index(drop=True)
        body.columns = range(body.shape[1])
        if body.empty:
            continue
        # Choose the time-axis column: the column with the best date-parse fraction,
        # giving a strong bonus to date-ish header names. Require >= 0.6 to accept.
        best = None  # (score, ci, parsed_dates)
        for ci in range(min(body.shape[1], 8)):
            parsed, ok = _parse_period_strings(_as_str(body[ci]))
            name = header[ci] if ci < len(header) else ""
            score = ok + (0.5 if name and DATE_HDR.search(name) else 0.0)
            if ok >= 0.6 and (best is None or score > best[0]):
                best = (score, ci, parsed)
        if best is None:
            continue
        _, dci, date_parsed = best
        period_raw = _as_str(body[dci])
        keep = period_raw.notna() & (period_raw != "") & (period_raw.str.lower() != "nan")
        body = body[keep.to_numpy()].reset_index(drop=True)
        period_raw = period_raw[keep.to_numpy()].reset_index(drop=True)
        date_parsed = date_parsed[keep.to_numpy()].reset_index(drop=True)
        n = len(body)
        if n == 0:
            continue
        sheet_tag = sh.strip() if not multi else f"{file_stem}:{sh.strip()}"
        is_panel = period_raw.duplicated(keep=False).sum() > 0.3 * n
        value_cols, dim_cols = [], []
        for ci in range(body.shape[1]):
            if ci == dci:
                continue
            name = header[ci] if ci < len(header) else ""
            if not name or name.lower() in ("nan", "none", ""):
                continue  # drop unnamed/index columns
            col = body[ci]
            num = pd.to_numeric(col.astype("string").str.replace(",", "", regex=False), errors="coerce")
            numfrac = num.notna().sum() / max(1, col.notna().sum())
            if numfrac >= 0.6:
                value_cols.append((name, num))
            else:
                dim_cols.append((name, _as_str(col)))
        # dimension: concat all text columns (panels only); ignored in wide mode
        if is_panel and dim_cols:
            dim_vals = []
            for i in range(n):
                parts = [str(dc[1].iloc[i]) for dc in dim_cols if dc[1].iloc[i] is not pd.NA]
                dim_vals.append(" | ".join(parts) if parts else None)
        else:
            dim_vals = [None]*n
        for name, num in value_cols:
            arr = num.to_numpy()
            for i in range(n):
                v = arr[i]
                if v is None or (isinstance(v, float) and np.isnan(v)):
                    continue
                d = date_parsed.iloc[i]
                rows.append({
                    "sheet": sheet_tag,
                    "period": None if period_raw.iloc[i] is pd.NA else str(period_raw.iloc[i]),
                    "date": None if pd.isna(d) else d.date(),
                    "dimension": dim_vals[i],
                    "series": name,
                    "value": float(v),
                })
    return rows
