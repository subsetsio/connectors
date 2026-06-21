"""Generic parser for Central Bank of Malta statistical Excel tables.

CBM tables are human-oriented matrices: title rows, a multi-row column-header
band, a left "stub" of row identifiers (a Period/year column and/or category
text), and a block of numeric value columns. We melt each sheet to long format:
(sheet, section_label, row_label, series, value).

Heuristics:
- A row is a DATA row if it has >= 2 numerically-parseable cells.
- Header band = rows above the first data row.
- VALUE columns = columns that have a RAW (pre-fill) header label AND are mostly
  numeric in the data region. The Period/year column is numeric but header-less
  -> it falls into the STUB, becoming the row label.
- Column header path = header-band cells, horizontally forward-filled (to spread
  merged parent headers), joined top->bottom.
- A row whose stub has text but zero value cells is a SECTION row (e.g. a bare
  year "2008" above month rows); its label becomes section_label context for the
  following rows.
"""
import re
import math

_NUM_RE = re.compile(r"^-?\d{1,3}(?:,\d{3})*(?:\.\d+)?$|^-?\d+(?:\.\d+)?$")

_MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
_PERIOD_PATTERNS = [
    re.compile(r"\b(?:19|20)\d{2}\b"),                 # a year
    re.compile(r"\bq[1-4]\b", re.I),                   # quarter
]


def _is_period_like(x):
    if x is None:
        return False
    if isinstance(x, (int, float)):
        if isinstance(x, float) and math.isnan(x):
            return False
        v = float(x)
        return v == int(v) and 1900 <= v <= 2099       # a bare year
    s = str(x).strip().lower()
    if not s:
        return False
    if s[:3] in _MONTHS:
        return True
    return any(p.search(s) for p in _PERIOD_PATTERNS)


def _to_num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        if isinstance(x, float) and math.isnan(x):
            return None
        return float(x)
    s = str(x).strip()
    if s in ("", "-", "–", "—", "n/a", "N/A", "na", "NA", ":", "...", "."):
        return None
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    s = s.rstrip("%").strip()
    # strip trailing footnote markers like '809.1 1' are separate cells, leave alone
    s2 = s.replace(",", "")
    try:
        v = float(s2)
    except ValueError:
        return None
    return -v if neg else v


def _is_blank(x):
    if x is None:
        return True
    if isinstance(x, float) and math.isnan(x):
        return True
    return str(x).strip() == ""


def _clean_text(x):
    if _is_blank(x):
        return None
    s = str(x).strip()
    # collapse whitespace/newlines
    s = re.sub(r"\s+", " ", s)
    return s or None


def _fmt_label(x):
    """Format a stub cell for use as a label: integer-valued floats -> '1995'."""
    if isinstance(x, float) and not math.isnan(x) and x == int(x):
        return str(int(x))
    return _clean_text(x)


def parse_sheet(rows, sheet_name):
    """rows: list[list] grid (header=None). Returns list[dict]."""
    if not rows:
        return []
    ncols = max((len(r) for r in rows), default=0)
    grid = [list(r) + [None] * (ncols - len(r)) for r in rows]
    nrows = len(grid)

    # Orientation: periods may run DOWN a column (tall, the default) or ACROSS a
    # row (wide). Our melt assumes tall — transpose wide tables so periods become
    # the row stub. Decide by where period-like tokens cluster densest.
    best_col = max((sum(1 for r in range(nrows) if _is_period_like(grid[r][c])) for c in range(ncols)), default=0)
    best_row = max((sum(1 for c in range(ncols) if _is_period_like(grid[r][c])) for r in range(nrows)), default=0)
    if best_row > best_col and best_row >= 3:
        grid = [list(col) for col in zip(*grid)]
        nrows, ncols = ncols, nrows

    numgrid = [[_to_num(grid[r][c]) for c in range(ncols)] for r in range(nrows)]

    # data rows: >=2 numeric cells
    data_rows = [r for r in range(nrows) if sum(1 for c in range(ncols) if numgrid[r][c] is not None) >= 2]
    if not data_rows:
        return []
    first_data = min(data_rows)
    last_data = max(data_rows)
    header_rows = list(range(0, first_data))
    body_rows = list(range(first_data, last_data + 1))

    # raw header presence per column (text in any header row)
    raw_header = {}
    for c in range(ncols):
        labels = [_clean_text(grid[r][c]) for r in header_rows]
        raw_header[c] = [l for l in labels if l]

    # numeric fraction per column over body
    col_numfrac = {}
    for c in range(ncols):
        cnt = sum(1 for r in body_rows if numgrid[r][c] is not None)
        col_numfrac[c] = cnt / max(len(body_rows), 1)

    # value columns: have a raw header AND are mostly numeric
    value_cols = [c for c in range(ncols) if raw_header[c] and col_numfrac[c] >= 0.3]
    if not value_cols:
        # fallback: any column mostly numeric (no header band at all)
        value_cols = [c for c in range(ncols) if col_numfrac[c] >= 0.5]
    if not value_cols:
        return []
    first_val = min(value_cols)
    # stub columns: everything left of the first value column
    stub_cols = [c for c in range(ncols) if c < first_val]

    # build horizontally-ffilled header rows for label paths
    ff = []
    for r in header_rows:
        row = []
        last = None
        for c in range(ncols):
            t = _clean_text(grid[r][c])
            if t is not None:
                last = t
            row.append(last)
        ff.append(row)

    def series_for(c):
        parts = []
        for ri in range(len(header_rows)):
            t = ff[ri][c]
            if t and (not parts or parts[-1] != t):
                parts.append(t)
        return " | ".join(parts) if parts else f"col{c}"

    series_map = {c: series_for(c) for c in value_cols}

    out = []
    section_label = None
    for r in body_rows:
        stub_vals = [_fmt_label(grid[r][c]) for c in stub_cols]
        stub_vals = [s for s in stub_vals if s]
        row_label = " | ".join(stub_vals) if stub_vals else None
        has_value = any(numgrid[r][c] is not None for c in value_cols)
        if not has_value:
            # section / context row (e.g. a bare year above month rows)
            if row_label:
                section_label = row_label
            continue
        for c in value_cols:
            v = numgrid[r][c]
            if v is None:
                continue
            out.append({
                "sheet": sheet_name,
                "section_label": section_label,
                "row_label": row_label,
                "series": series_map[c],
                "value": v,
            })
    return out


def parse_workbook(content, ext):
    import io
    import pandas as pd
    engines = ["openpyxl", "xlrd"] if ext == "xlsx" else ["xlrd", "openpyxl"]
    xls = None
    last_err = None
    for eng in engines:
        try:
            xls = pd.ExcelFile(io.BytesIO(content), engine=eng)
            break
        except Exception as e:  # noqa: BLE001 - probing which engine fits
            last_err = e
    if xls is None:
        raise RuntimeError(f"could not open workbook: {last_err}")
    allrows = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None, dtype=object)
        grid = df.values.tolist()
        allrows.extend(parse_sheet(grid, str(sheet)))
    return allrows
