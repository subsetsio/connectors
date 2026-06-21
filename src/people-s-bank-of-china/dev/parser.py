"""Candidate production parser — tested standalone before porting to the node module."""
import pandas as pd, re, io

PERIOD = re.compile(r'^(\d{4})[.\-/年]\s*(\d{1,2})\s*月?$')
NOTE = re.compile(r'^\s*(注\s*[:：]|注\d|note|备注|资料来源|source\s*[:：])', re.I)
UNIT_RE = re.compile(r'unit\s*[:：]\s*(.+)', re.I)

def clean(v):
    s = "" if v is None else str(v)
    if s == "nan": s = ""
    return re.sub(r"\s+", " ", s.replace("\xa0", " ").replace("　", " ")).strip()

def to_num(s):
    s = s.replace(",", "").replace("%", "").strip()
    if s in ("", "-", "—", "…", "..", "/", "nan", "N/A", "NA"): return None
    try: return float(s)
    except Exception: return None

def grid_from_htm(text):
    out = []
    for df in pd.read_html(io.StringIO(text)):
        out.append(df.map(clean).values.tolist())
    # pick the widest/longest table (the data one)
    return max(out, key=lambda g: len(g)*(len(g[0]) if g else 0)) if out else []

def grid_from_xls(content):
    xls = pd.ExcelFile(io.BytesIO(content))
    best = []
    for sh in xls.sheet_names:
        df = xls.parse(sh, header=None)
        g = df.map(clean).values.tolist()
        if len(g)*(len(g[0]) if g else 0) > len(best)*(len(best[0]) if best else 0):
            best = g
    return best

def _unit(grid, upto):
    for r in grid[:upto]:
        for c in r:
            m = UNIT_RE.search(c)
            if m: return m.group(1).strip()
    return None

def parse_grid(grid):
    if not grid: return []
    nrows = len(grid); ncols = max(len(r) for r in grid)
    grid = [r + [""]*(ncols-len(r)) for r in grid]
    # ---- orientation A: a row holds >=2 period labels ----
    hdr = None; pcol = {}
    for ri, row in enumerate(grid):
        pc = {ci: PERIOD.match(c) for ci, c in enumerate(row) if PERIOD.match(c)}
        if len(pc) >= 2:
            hdr = ri; pcol = {ci: (int(m.group(1)), int(m.group(2))) for ci, m in pc.items()}; break
    if hdr is not None:
        return _parse_A(grid, hdr, pcol, ncols)
    # ---- orientation B: a column holds >=2 period labels (transposed) ----
    for ci in range(ncols):
        col = [grid[ri][ci] for ri in range(nrows)]
        pr = {ri: PERIOD.match(c) for ri, c in enumerate(col) if PERIOD.match(c)}
        if len(pr) >= 2:
            return _parse_B(grid, ci, {ri:(int(m.group(1)),int(m.group(2))) for ri,m in pr.items()}, nrows, ncols)
    return []

def _parse_A(grid, hdr, pcol, ncols):
    unit = _unit(grid, hdr)
    first_p = min(pcol)
    # detect measure sub-header rows directly under hdr (cells in period cols that are non-numeric text)
    measure = {ci: [] for ci in pcol}
    data_start = hdr + 1
    for ri in range(hdr+1, min(hdr+4, len(grid))):
        row = grid[ri]
        texty = [ci for ci in pcol if row[ci] and to_num(row[ci]) is None and not PERIOD.match(row[ci])]
        if len(texty) >= max(2, len(pcol)//2):
            for ci in pcol:
                if row[ci]: measure[ci].append(row[ci])
            data_start = ri + 1
        else:
            break
    recs = []
    pend_lbl = []; pend = None
    def flush():
        nonlocal pend_lbl, pend
        if pend and any(v is not None for _, v in pend):
            label = " ".join(dict.fromkeys([x for x in pend_lbl if x]))
            if label:
                for ci, v in pend:
                    if v is not None:
                        y, mo = pcol[ci]
                        meas = " ".join(dict.fromkeys([m for m in measure[ci] if m])) or None
                        recs.append({"item": label, "measure": meas, "period": f"{y}-{mo:02d}",
                                     "year": y, "month": mo, "value": v, "unit": unit})
        pend_lbl = []; pend = None
    for ri in range(data_start, len(grid)):
        row = grid[ri]
        joined = " ".join(c for c in row if c)
        if not joined: continue
        if NOTE.match(joined): break
        lead = [row[ci] for ci in range(first_p) if row[ci]]
        vals = [(ci, to_num(row[ci])) for ci in pcol]
        vt = tuple(v for _, v in vals)
        if all(v is None for v in vt): continue
        if pend is not None and vt == tuple(v for _, v in pend):
            pend_lbl.extend(lead)
        else:
            flush(); pend_lbl = list(lead); pend = vals
    flush()
    return recs

def _parse_B(grid, pci, prow, nrows, ncols):
    unit = _unit(grid, min(prow))
    # item header = the rows above the first period row, columns != pci
    first_p = min(prow)
    item_label = {}
    for ci in range(ncols):
        if ci == pci: continue
        parts = [grid[ri][ci] for ri in range(first_p) if grid[ri][ci]]
        item_label[ci] = " ".join(dict.fromkeys(parts))
    recs = []
    for ri in sorted(prow):
        y, mo = prow[ri]
        for ci in range(ncols):
            if ci == pci: continue
            lbl = item_label.get(ci, "")
            if not lbl: continue
            v = to_num(grid[ri][ci])
            if v is None: continue
            recs.append({"item": lbl, "measure": None, "period": f"{y}-{mo:02d}",
                         "year": y, "month": mo, "value": v, "unit": unit})
    return recs
