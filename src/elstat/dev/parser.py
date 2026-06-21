import io
import math
import re

import pandas as pd

_SKIP = {"", "nan", "nat", "none", "-", ".", "..", "...", ":", "n/a", "na", "n.a.", "*", "**"}


def _clean(v):
    if v is None:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    if s.lower() in _SKIP:
        return None
    return s


def to_num(v):
    s = _clean(v)
    if s is None:
        return None
    s2 = s.replace(" ", "").replace(" ", "")
    if "," in s2 and "." in s2:
        if s2.rfind(",") > s2.rfind("."):
            s2 = s2.replace(".", "").replace(",", ".")
        else:
            s2 = s2.replace(",", "")
    elif "," in s2:
        parts = s2.split(",")
        if len(parts) == 2 and len(parts[1]) != 3:
            s2 = s2.replace(",", ".")
        else:
            s2 = s2.replace(",", "")
    try:
        f = float(s2)
    except ValueError:
        return None
    return f if math.isfinite(f) else None


def melt_sheet(grid, source_file, sheet):
    g = [list(r) for r in grid]
    nrows = len(g)
    if nrows == 0:
        return []
    ncols = max((len(r) for r in g), default=0)
    for r in g:
        r += [None] * (ncols - len(r))

    def num_cells(row):
        return sum(1 for j in range(1, ncols) if to_num(row[j]) is not None)

    first_data = None
    for i, row in enumerate(g):
        if num_cells(row) >= 2:
            first_data = i
            break
    if first_data is None:
        for i, row in enumerate(g):
            if num_cells(row) >= 1:
                first_data = i
                break
    if first_data is None:
        return []

    cand = list(range(max(0, first_data - 6), first_data))

    def nonempty(row):
        return sum(1 for c in row if _clean(c) is not None)

    header_idx = max(cand, key=lambda i: nonempty(g[i])) if cand else None
    header = g[header_idx] if header_idx is not None else [None] * ncols
    filled, last = [], None
    for c in header:
        cc = _clean(c)
        if cc is not None:
            last = cc
        filled.append(last)

    out = []
    for i in range(first_data, nrows):
        row = g[i]
        if num_cells(row) == 0:
            continue
        rl = None
        for j in range(ncols):
            c = _clean(row[j])
            if c is not None and to_num(row[j]) is None:
                rl = c
                break
        if rl is None:
            for j in range(ncols):
                c = _clean(row[j])
                if c is not None:
                    rl = c
                    break
        for j in range(ncols):
            n = to_num(row[j])
            if n is None:
                continue
            cl = filled[j] if j < len(filled) else None
            if cl is None or cl == rl:
                cl = f"col{j}"
            out.append({
                "source_file": source_file,
                "sheet": str(sheet)[:120],
                "row_label": (rl or "")[:300],
                "col_label": cl[:300],
                "row_idx": i,
                "col_idx": j,
                "value": n,
            })
    return out


def melt_workbook(content, source_file):
    sheets = pd.read_excel(io.BytesIO(content), header=None, dtype=str, sheet_name=None)
    rows = []
    for sh, df in sheets.items():
        grid = df.where(pd.notna(df), None).values.tolist()
        rows.extend(melt_sheet(grid, source_file, sh))
    return rows


_LANG_RE = re.compile(r"_([A-Za-z?]{2})(?:_\d+)?\.(?:xlsx?|XLSX?)$")


def select_excel(files):
    def lang(fn):
        m = _LANG_RE.search(fn)
        return m.group(1).upper() if m else ""

    def stem(fn):
        return _LANG_RE.sub("", fn).upper()

    groups = {}
    for fn, content in files:
        groups.setdefault(stem(fn), []).append((fn, content))
    rank = {"EN": 0, "BI": 1, "": 2}
    chosen = []
    for members in groups.values():
        members.sort(key=lambda fc: rank.get(lang(fc[0]), 3))
        chosen.append(members[0])
    return chosen
