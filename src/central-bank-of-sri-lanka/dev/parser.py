import re

_YEAR_RE = re.compile(r'^\s*((?:19|20)\d{2})')
_NA = {"", "-", "–", "—", "n.a.", "n.a", "N.A.", "N.A", "na", "...", "…", "n/a"}

def _year_of(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int) and 1900 <= v <= 2100:
        return v
    if isinstance(v, float) and v.is_integer() and 1900 <= v <= 2100:
        return int(v)
    if isinstance(v, str):
        m = _YEAR_RE.match(v.strip())
        if m:
            return int(m.group(1))
    return None

def _num(v):
    """Return (float|None, text|None). Parses footnoted/parenthesised/comma numbers."""
    if v is None or isinstance(v, bool):
        return None, None
    if isinstance(v, (int, float)):
        return float(v), None
    s = str(v).strip()
    if s.lower() in _NA:
        return None, (s or None)
    paren = re.fullmatch(r'\((.*)\)', s)
    inner = paren.group(1) if paren else s
    cleaned = re.sub(r'\([^)]*\)', '', inner).replace(',', '').replace('%', '').strip()
    if re.fullmatch(r'[+-]?\d*\.?\d+', cleaned):
        f = float(cleaned)
        return (-f if paren else f), s
    return None, s

def _is_text(v):
    if v is None or isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return False
    s = str(v).strip()
    if s == "" or s.lower() in _NA:   # NA markers ("-", "n.a.") are neutral, not labels
        return False
    return _num(v)[0] is None

def _clean(v):
    return re.sub(r'\s+', ' ', str(v)).strip()

_DECOR = re.compile(r'^\s*(\d{2}\.\s|TABLE\s+\d|KEY ECONOMIC INDICATORS)', re.IGNORECASE)

def _sanitize(grid):
    # Blank decorative cells (chapter banner, "TABLE x.y" marker) so forward-fill
    # of grouped headers can't smear a page title across the value columns.
    for row in grid:
        for c in range(len(row)):
            v = row[c]
            if isinstance(v, str) and _DECOR.match(v.strip()):
                row[c] = None
    return grid

def parse_sheet(rows):
    grid = [list(r) for r in rows]
    if not grid:
        return [], "empty"
    ncols0 = max((len(r) for r in grid), default=0)
    for r in grid:
        r += [None] * (ncols0 - len(r))
    _sanitize(grid)
    grid = [r for r in grid if any(c is not None for c in r)]
    if not grid:
        return [], "empty"
    ncols = max(len(r) for r in grid)
    for r in grid:
        r += [None] * (ncols - len(r))
    nrows = len(grid)

    def realnum(r):
        # count cells holding a genuine measurement (a number that is NOT a year);
        # year-only rows are column headers, not data.
        return sum(1 for c in range(ncols)
                   if _num(grid[r][c])[0] is not None and _year_of(grid[r][c]) is None)

    # first data row: a row carrying at least one real (non-year) measurement.
    data_start = next((r for r in range(nrows) if realnum(r) >= 1), None)
    if data_start is None:
        return [], "no_data"

    # Orientation B: a left-region column that is a year for (almost) every data
    # row — a genuine vertical time axis. The fraction guard rejects value columns
    # whose numbers merely happen to fall in the year range (e.g. a CPI series).
    data_rows = [r for r in range(nrows) if realnum(r) >= 1]
    period_col = None
    for c in range(min(ncols, 3)):
        yc = sum(1 for r in data_rows if _year_of(grid[r][c]) is not None)
        if data_rows and yc >= 4 and yc >= 0.8 * len(data_rows):
            period_col = c
            break

    if period_col is not None:
        stub_cols = [period_col]
        # anchor to the first real data row (skip unit rows like "1952 = 100"
        # that live in the period column and parse as a year).
        data_start = min(r for r in data_rows if _year_of(grid[r][period_col]) is not None)
    else:
        # leading run of mostly-text columns over the data region = stub columns
        stub_cols = []
        for c in range(ncols):
            col_vals = [grid[r][c] for r in range(data_start, nrows)]
            if all(v is None for v in col_vals):
                if not stub_cols:
                    continue  # skip empty leading column(s)
                break
            texts = sum(1 for v in col_vals if _is_text(v))
            nums = sum(1 for v in col_vals if _num(v)[0] is not None)
            if texts >= nums and texts > 0:
                stub_cols.append(c)
            else:
                break
        if not stub_cols:
            stub_cols = [c for c in range(ncols) if any(grid[r][c] is not None for r in range(nrows))][:1]

    value_cols = [c for c in range(ncols)
                  if c not in stub_cols
                  and any(grid[r][c] is not None for r in range(nrows))]
    if not value_cols:
        return [], "no_value_cols"

    # header band: rows above data_start with content in a value column (skips
    # title/unit/section rows whose only content sits in the stub region).
    band = [r for r in range(data_start) if any(grid[r][c] is not None for c in value_cols)]
    headers = {}
    if band:
        filled = []
        for r in band:
            ff, last = [], None
            for c in range(ncols):
                if grid[r][c] is not None and str(grid[r][c]).strip() != "":
                    last = _clean(grid[r][c])
                ff.append(last)
            filled.append(ff)
        for c in value_cols:
            parts = []
            for fr in filled:
                p = fr[c]
                if p and (not parts or parts[-1] != p):
                    parts.append(p)
            headers[c] = " | ".join(parts) if parts else f"col_{c}"
    else:
        headers = {c: f"col_{c}" for c in value_cols}

    out = []
    section = None
    for r in range(data_start, nrows):
        stub_parts = [_clean(grid[r][c]) for c in stub_cols
                      if grid[r][c] is not None and str(grid[r][c]).strip() != ""]
        stub = " - ".join(stub_parts)
        emitted = 0
        recs = []
        for c in value_cols:
            val, txt = _num(grid[r][c])
            if val is None and txt is None:
                continue
            recs.append((c, val, txt))
        # section header row (only in non-B): label present, no values
        if period_col is None and stub and not recs:
            section = stub
            continue
        if not stub and not recs:
            continue
        row_label = f"{section} - {stub}" if (section and stub) else (stub or section or "")
        for c, val, txt in recs:
            col_label = headers.get(c, f"col_{c}")
            if period_col is not None:
                py = _year_of(grid[r][period_col])
            else:
                py = _year_of(col_label)
            out.append({
                "row_label": row_label or None,
                "col_label": col_label,
                "period_year": py,
                "value": val,
                "value_text": txt,
            })
    return out, ("B" if period_col is not None else "A")
