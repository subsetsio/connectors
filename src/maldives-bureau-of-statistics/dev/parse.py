import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re, math
import pandas as pd

def _is_num(x):
    if x is None: return False
    if isinstance(x,(int,float)):
        return not (isinstance(x,float) and math.isnan(x))
    s=str(x).strip().replace(',','')
    if s=='' : return False
    try: float(s); return True
    except: return False

def _to_num(x):
    if isinstance(x,(int,float)): return float(x)
    s=str(x).strip().replace(',','')
    try: return float(s)
    except: return None

def _isnull(x):
    return x is None or (isinstance(x,float) and math.isnan(x)) or (isinstance(x,str) and x.strip()=='')

def parse_grid(df):
    # df: raw grid header=None
    rows = df.values.tolist()
    # 1) drop leading sparse rows (<=1 non-null) -> titles/blanks/subtitles
    def nonnull_count(r): return sum(0 if _isnull(c) else 1 for c in r)
    start=0
    while start<len(rows) and nonnull_count(rows[start])<=1:
        start+=1
    block=rows[start:]
    if not block: return []
    ncol=max(len(r) for r in block)
    block=[list(r)+[None]*(ncol-len(r)) for r in block]
    # 2) drop fully-empty columns over the block
    keep=[j for j in range(ncol) if any(not _isnull(r[j]) for r in block)]
    block=[[r[j] for j in keep] for r in block]
    ncol=len(keep)
    if ncol<2: return []
    # 3) header band: first row always header; continue while col0 null OR text in value cols
    def has_text_value(r):
        return any((not _isnull(r[j])) and (not _is_num(r[j])) for j in range(1,ncol))
    h=1
    while h<len(block):
        r=block[h]
        if _isnull(r[0]) or has_text_value(r):
            h+=1
        else:
            break
    header_rows=block[:h]
    data_rows=block[h:]
    if not data_rows: return []
    # 4) build per-column header by ffill each header row then join col-wise
    ff=[]
    for hr in header_rows:
        out=[]; last=None
        for j in range(ncol):
            v=hr[j]
            if _isnull(v): out.append(last)
            else: last=str(v).strip(); out.append(last)
        ff.append(out)
    col_header={}
    for j in range(1,ncol):
        parts=[ff[i][j] for i in range(len(ff)) if ff[i][j] not in (None,'')]
        col_header[j]=" | ".join(dict.fromkeys(parts)) if parts else f"col_{j}"
    # 5) melt
    recs=[]
    for r in data_rows:
        lbl=r[0]
        if _isnull(lbl): continue
        lbl=str(lbl).strip()
        for j in range(1,ncol):
            v=_to_num(r[j])
            if v is None: continue
            recs.append({"row_label":lbl,"column":col_header[j],"value":v})
    return recs

if __name__=="__main__":
    from subsets_utils import get
    import json
    page=get("https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/", timeout=(10,120)).text
    hrefs={}
    for m in re.finditer(r'href="([^"]+/(\d+\.\d+)\.xlsx?)"', page):
        hrefs.setdefault(m.group(2), m.group(1))
    union=json.load(open(os.path.join(os.path.dirname(__file__),"..","..","..","..","data","sources","maldives-bureau-of-statistics","work","entity_union.json")))
    ids = union if isinstance(union,list) else union.get("entity_ids") or list(union)
    print("union size", len(ids))
    fails=[]; small=[]; ok=0
    for tid in ids:
        url=hrefs.get(tid)
        if not url: fails.append((tid,"no-href")); continue
        try:
            r=get(url, timeout=(10,120))
            ext=url.rsplit('.',1)[-1]
            df=pd.read_excel(io.BytesIO(r.content), header=None, engine=('openpyxl' if ext=='xlsx' else 'xlrd'))
            recs=parse_grid(df)
        except Exception as e:
            fails.append((tid, type(e).__name__+":"+str(e)[:60])); continue
        n=len(recs)
        if n==0: fails.append((tid,"0-rows"))
        elif n<5: small.append((tid,n))
        else: ok+=1
    print("OK(>=5 rows):",ok,"  small(<5):",len(small),"  FAIL:",len(fails))
    print("small:",small)
    print("fails:",fails)
