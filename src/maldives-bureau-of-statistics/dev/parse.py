import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re, math
import pandas as pd

def _is_num(x):
    if x is None: return False
    if isinstance(x,(int,float)): return not (isinstance(x,float) and math.isnan(x))
    s=str(x).strip().replace(',','')
    if s=='': return False
    try: float(s); return True
    except: return False

def _to_num(x):
    if isinstance(x,(int,float)):
        return None if (isinstance(x,float) and math.isnan(x)) else float(x)
    s=str(x).strip().replace(',','')
    try: return float(s)
    except: return None

def _isnull(x):
    return x is None or (isinstance(x,float) and math.isnan(x)) or (isinstance(x,str) and x.strip()=='')

def parse_grid(df):
    rows=df.values.tolist()
    def nn(r): return sum(0 if _isnull(c) else 1 for c in r)
    start=0
    while start<len(rows) and nn(rows[start])<=1: start+=1
    block=rows[start:]
    if not block: return []
    ncol=max(len(r) for r in block)
    block=[list(r)+[None]*(ncol-len(r)) for r in block]
    keep=[j for j in range(ncol) if any(not _isnull(r[j]) for r in block)]
    block=[[r[j] for j in keep] for r in block]
    ncol=len(keep)
    if ncol<2: return []
    # per-column numeric fraction over non-null cells
    def frac_num(j):
        vals=[r[j] for r in block if not _isnull(r[j])]
        if not vals: return 0.0
        return sum(1 for v in vals if _is_num(v))/len(vals)
    value_col={j: frac_num(j)>=0.5 for j in range(ncol)}
    # value block starts at first consecutive pair of value cols; else col1
    b=None
    for j in range(ncol-1):
        if value_col[j] and value_col[j+1]: b=j; break
    if b is None:
        b=1 if any(value_col[j] for j in range(1,ncol)) else None
    if b is None or b<1: b=max(1,(b or 1))
    if b>=ncol: return []
    label_cols=list(range(b))
    value_cols=list(range(b,ncol))
    # header band: first row always header; then while no clean data row
    def has_text_value(r): return any((not _isnull(r[j])) and (not _is_num(r[j])) for j in value_cols)
    def has_label(r): return any(not _isnull(r[j]) for j in label_cols)
    def has_num(r): return any(_to_num(r[j]) is not None for j in value_cols)
    h=1
    while h<len(block):
        r=block[h]
        if has_text_value(r) or not has_label(r) or not has_num(r): h+=1
        else: break
    header_rows=block[:h]; data_rows=block[h:]
    if not data_rows: return []
    # build per-value-col header (ffill each header row L->R, join)
    ff=[]
    for hr in header_rows:
        out=[]; last=None
        for j in range(ncol):
            v=hr[j]
            if _isnull(v): out.append(last)
            else: last=str(v).strip(); out.append(last)
        ff.append(out)
    col_header={}
    for j in value_cols:
        parts=[ff[i][j] for i in range(len(ff)) if ff[i][j] not in (None,'')]
        col_header[j]=" | ".join(dict.fromkeys(parts)) if parts else f"col_{j}"
    recs=[]
    for r in data_rows:
        lbl=" | ".join(str(r[j]).strip() for j in label_cols if not _isnull(r[j]))
        if not lbl: continue
        for j in value_cols:
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
    p=os.path.join(os.path.dirname(__file__),"..","..","..","..","data","sources","maldives-bureau-of-statistics","work","entity_union.json")
    union=json.load(open(p)); ids=union if isinstance(union,list) else (union.get("entity_ids") or list(union))
    fails=[]; small=[]; ok=0; samples={}
    for tid in ids:
        url=hrefs.get(tid)
        if not url: fails.append((tid,"no-href")); continue
        try:
            r=get(url, timeout=(10,120)); ext=url.rsplit('.',1)[-1]
            df=pd.read_excel(io.BytesIO(r.content), header=None, engine=('openpyxl' if ext=='xlsx' else 'xlrd'))
            recs=parse_grid(df)
        except Exception as e:
            fails.append((tid,type(e).__name__+":"+str(e)[:50])); continue
        n=len(recs)
        if n==0: fails.append((tid,"0-rows"))
        elif n<5: small.append((tid,n))
        else: ok+=1
        if tid in ("12.7","24.3","1.1","22.1"): samples[tid]=recs[:4]
    print("OK(>=5):",ok," small:",len(small)," FAIL:",len(fails))
    print("small:",small); print("fails:",fails)
    for k,v in samples.items():
        print("---",k); [print("   ",s) for s in v]
