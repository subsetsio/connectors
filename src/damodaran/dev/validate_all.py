import sys, os, io, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pandas as pd
from subsets_utils import get

# (slug, us_file, anchor, sheet_hint)
FAMS = [
 ("inshold","inshold","Industry Name","Industry Averages"),
 ("histretsp","histretSP","Year","Returns by year"),
 ("histimpl","histimpl","Year","Historical Impl Premiums"),
 ("ctryprem","ctryprem","Country","ERPs by country"),
 ("betas","betas","Industry Name","Industry Averages"),
 ("countrytaxrates","countrytaxrates","Country",None),
 ("totalbeta","totalbeta","Industry Name","Industry Averages"),
 ("mktcaprisk","mktcaprisk","Market Cap","Sheet1"),
 ("wacc","wacc","Industry Name","Industry Averages"),
 ("taxrate","taxrate","Industry Name","Industry Averages"),
 ("dollarvalue","DollarUS","Industry Name","Industry Averages"),
 ("mktcap","MktCap","Industry Name","Industry Averages"),
 ("employee","Employee","Industry Name","Industry Averages"),
 ("eva","EVA","Industry Name","Industry Averages"),
 ("debtdetails","debtdetails","Industry Name","Industry Averages"),
 ("dbtfund","dbtfund","Industry Name","Industry Averages"),
 ("leaseeffect","leaseeffect","Industry Name","Industry Averages"),
 ("macro","macro","Date","Annual Data"),
 ("divfcfe","divfcfe","Industry Name","Industry Averages"),
 ("divfund","divfund","Industry Name","Industry Averages"),
 ("capex","capex","Industry Name","Industry Averages"),
 ("rd","R&D","Industry Name","Industry Averages"),
 ("goodwill","goodwill","Industry Name","Industry Averages"),
 ("margin","margin","Industry Name","Industry Averages"),
 ("finflows","finflows","Industry Name","Industry Averages"),
 ("wcdata","wcdata","Industry Name","Industry Averages"),
 ("roe","roe","Industry Name","Industry Averages"),
 ("fundgr","fundgr","Industry Name","Industry Averages"),
 ("histgr","histgr","Industry Name","Industry Averages"),
 ("fundgreb","fundgrEB","Industry Name","Industry Averages"),
 ("pedata","pedata","Industry Name","Industry Averages"),
 ("pbvdata","pbvdata","Industry Name","Industry Averages"),
 ("psdata","psdata","Industry Name","Industry Averages"),
 ("vebitda","vebitda","Industry Name","Industry Averages"),
 ("mktcapmult","mktcapmult","Market Cap","Sheet1"),
 ("countrystats","countrystats","Country","Sheet1"),
 ("optvar","optvar","Industry Name","Industry Averages"),
]
def is_num(v):
    if v is None or isinstance(v,bool): return False
    if isinstance(v,(int,float)): return not (isinstance(v,float) and math.isnan(v))
    s=str(v).strip().replace(",","").replace("%","")
    if s in ("","nan","NA","#DIV/0!","#N/A","NaN","#VALUE!","#REF!"): return False
    try: float(s); return True
    except: return False
def clean(v):
    if v is None: return ""
    s=str(v).strip(); return "" if s.lower()=="nan" else s
def norm(x): return " ".join(clean(x).lower().split())
def find_header(df, anchor):
    a=norm(anchor)
    for i in range(min(len(df),60)):
        row=df.iloc[i].tolist()
        if norm(row[0]).startswith(a) and sum(1 for v in row if clean(v))>=3:
            return i
    return None
def parse(content, anchor, sheet_hint):
    xls=pd.ExcelFile(io.BytesIO(content))
    order = ([sheet_hint] if (sheet_hint and sheet_hint in xls.sheet_names) else [])
    order += [s for s in xls.sheet_names if s not in order]
    sheets = order
    for sh in sheets:
        df=pd.read_excel(xls,sheet_name=sh,header=None)
        hi=find_header(df,anchor)
        if hi is None: continue
        header=[clean(x) for x in df.iloc[hi].tolist()]
        rows=[]
        for k in range(hi+1,len(df)):
            r=df.iloc[k].tolist()
            cat=clean(r[0])
            if not cat: break
            for j in range(1,len(header)):
                m=header[j]
                if not m: continue
                v=r[j] if j<len(r) else None
                if is_num(v):
                    rows.append((cat,m,float(str(v).replace(",","").replace("%",""))))
        if rows: return sh,header,rows
    return None,None,[]

bad=[]
for slug,uf,anchor,sheet in FAMS:
    try:
        r=get(f"https://pages.stern.nyu.edu/~adamodar/pc/datasets/{uf}.xls",timeout=(10,120))
        if r.status_code!=200: print(f"{slug:16} HTTP {r.status_code}"); bad.append(slug); continue
        sh,header,rows=parse(r.content,anchor,sheet)
        cats=len(set(c for c,_,_ in rows)); mets=len(set(m for _,m,_ in rows))
        flag = "" if rows and cats>=5 and mets>=1 else "  <<< CHECK"
        print(f"{slug:16} sheet={str(sh)[:24]:24} rows={len(rows):5} cats={cats:4} metrics={mets:3}{flag}")
        if not (rows and cats>=5): bad.append(slug)
    except Exception as e:
        print(f"{slug:16} ERR {type(e).__name__}: {e}"); bad.append(slug)
print("\nPROBLEM FAMILIES:", bad)
