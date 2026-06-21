import re, io
import pandas as pd

_NUM_RE = re.compile(r'^-?\d{1,3}(?:[  .,]\d{3})*(?:[.,]\d+)?$|^-?\d+(?:[.,]\d+)?$')
def to_num(v):
    if v is None: return None
    s = str(v).strip().replace(' ',' ')
    if s in ("","-",".","..","...",":","—","–","n/a","N/A",".."): return None
    s2 = s.replace(' ','')
    # both separators present -> assume , thousands . decimal OR . thousands , decimal
    if ',' in s2 and '.' in s2:
        if s2.rfind(',') > s2.rfind('.'):   # comma is decimal
            s2 = s2.replace('.','').replace(',','.')
        else:
            s2 = s2.replace(',','')
    elif ',' in s2:
        # comma only: decimal if exactly one and <=3 trailing digits else thousands
        parts = s2.split(',')
        if len(parts)==2 and len(parts[1])!=3:
            s2 = s2.replace(',','.')
        else:
            s2 = s2.replace(',','')
    try:
        return float(s2)
    except ValueError:
        return None

def melt_sheet(df, source_file, sheet):
    # df: all-string grid (NaN -> None)
    g = df.where(pd.notna(df), None).values.tolist()
    nrows = len(g)
    if nrows == 0: return []
    ncols = max((len(r) for r in g), default=0)
    # normalize row lengths
    for r in g:
        r += [None]*(ncols-len(r))
    def num_cells(row):
        return sum(1 for j in range(1,ncols) if to_num(row[j]) is not None)
    # first data row: first row with >=2 numeric cells in cols>=1
    first_data = None
    for i,row in enumerate(g):
        if num_cells(row) >= 2:
            first_data = i; break
    if first_data is None:
        # fallback: rows with >=1 numeric
        for i,row in enumerate(g):
            if num_cells(row) >= 1:
                first_data = i; break
    if first_data is None: return []
    # header row: among up to 6 rows above first_data, the one with most non-empty cells
    cand = range(max(0,first_data-6), first_data)
    def nonempty(row): return sum(1 for c in row if c not in (None,""))
    header_idx = max(cand, key=lambda i: nonempty(g[i]), default=None)
    header = g[header_idx] if header_idx is not None else [None]*ncols
    # forward-fill header (merged cells) left->right
    filled = []; last=None
    for c in header:
        c = (str(c).strip() if c not in (None,"") else None)
        if c is not None: last=c
        filled.append(last)
    out=[]
    for i in range(first_data, nrows):
        row = g[i]
        if num_cells(row) == 0: 
            continue
        # row label: leftmost non-empty cell (prefer cols 0..2)
        rl=None
        for j in range(ncols):
            if row[j] not in (None,""):
                rl=str(row[j]).strip(); break
        for j in range(ncols):
            n = to_num(row[j])
            if n is None: continue
            cl = filled[j] if j < len(filled) else None
            if cl is None or cl==rl: cl = f"col{j}"
            out.append({
                "source_file": source_file, "sheet": str(sheet),
                "row_label": rl, "col_label": cl,
                "row_idx": i, "col_idx": j, "value": n,
            })
    return out

def melt_workbook(content, source_file):
    sheets = pd.read_excel(io.BytesIO(content), header=None, dtype=str, sheet_name=None)
    rows=[]
    for sh, df in sheets.items():
        rows.extend(melt_sheet(df, source_file, sh))
    return rows
