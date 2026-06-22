import sys, os, io, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pandas as pd
from subsets_utils import get

def is_num(v):
    if v is None: return False
    if isinstance(v, bool): return False
    if isinstance(v, (int, float)):
        return not (isinstance(v, float) and math.isnan(v))
    s = str(v).strip().replace(",", "")
    if s in ("", "nan", "NA", "#DIV/0!", "#N/A", "NaN"): return False
    try:
        float(s); return True
    except: return False

def clean(v):
    if v is None: return ""
    s = str(v).strip()
    return "" if s.lower() == "nan" else s

def find_table(df):
    """Return (header_row_idx, header list) for the best data table in a sheet."""
    n = len(df)
    best = None
    for i in range(min(n, 45)):
        row = df.iloc[i].tolist()
        first = clean(row[0])
        if not first or ":" in first or "http" in first.lower(): continue
        nonnull_hdr = sum(1 for v in row if clean(v))
        if nonnull_hdr < 3: continue
        if i+1 >= n: continue
        nxt = df.iloc[i+1].tolist()
        numeric_after = sum(1 for v in nxt[1:] if is_num(v))
        if numeric_after >= 2:
            # count data rows below
            cnt = 0
            for k in range(i+1, n):
                r = df.iloc[k].tolist()
                if not clean(r[0]): break
                if sum(1 for v in r[1:] if is_num(v)) >= 1: cnt += 1
                else: break
            if best is None or cnt > best[2]:
                best = (i, [clean(x) for x in row], cnt)
    return best

def parse(content):
    xls = pd.ExcelFile(io.BytesIO(content))
    best = None
    for sh in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sh, header=None)
        t = find_table(df)
        if t and (best is None or t[2] > best[3]):
            best = (sh, t[0], t[1], t[2], df)
    if not best: return None, None, []
    sh, hi, header, cnt, df = best
    rows = []
    n = len(df)
    for k in range(hi+1, n):
        r = df.iloc[k].tolist()
        cat = clean(r[0])
        if not cat: break
        for j in range(1, len(header)):
            m = header[j] if j < len(header) else ""
            if not m: continue
            v = r[j] if j < len(r) else None
            if is_num(v):
                rows.append((cat, m, float(str(v).replace(",",""))))
    return sh, header, rows

for fam,url in [
  ("betas","datasets/betas.xls"),
  ("pedata","datasets/pedata.xls"),
  ("wacc","datasets/wacc.xls"),
  ("histretsp","datasets/histretSP.xls"),
  ("ctryprem","datasets/ctryprem.xls"),
  ("countrytaxrates","datasets/countrytaxrates.xls"),
  ("mktcaprisk","datasets/mktcaprisk.xls"),
  ("roe","datasets/roe.xls"),
]:
    r = get("https://pages.stern.nyu.edu/~adamodar/pc/"+url, timeout=(10,120))
    if r.status_code!=200:
        print(fam, "HTTP", r.status_code); continue
    sh, header, rows = parse(r.content)
    cats = sorted(set(c for c,_,_ in rows))
    mets = [m for m in (header[1:] if header else [])]
    print(f"\n### {fam}: sheet='{sh}' rows={len(rows)} cats={len(cats)} metrics={len(mets)}")
    print("  header:", header[:8] if header else None)
    print("  sample rows:", rows[:3])
    print("  sample cats:", cats[:5])
