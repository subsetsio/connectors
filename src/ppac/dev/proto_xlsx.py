import re, io, datetime
from subsets_utils import get
import openpyxl
def load(p):
    h=get(f"https://ppac.gov.in/{p}").text
    urls=re.findall(r'(https://ppac\.gov\.in/uploads/[^"\']+\.xlsx|https://ppac\.gov\.in/download\.php\?file=[^"\']+\.xlsx)',h)
    u=list(dict.fromkeys(urls))[0]
    return openpyxl.load_workbook(io.BytesIO(get(u).content),read_only=True,data_only=True), u.split('/')[-1]
def num(v):
    if v is None: return None
    if isinstance(v,(int,float)): return float(v)
    s=str(v).replace(',','').strip()
    try: return float(s)
    except: return None
def rows_of(ws): return [list(r) for r in ws.iter_rows(values_only=True)]

# A) state/date/value snapshot (active-domestic, pmuy)
def parse_snapshot(ws):
    rs=rows_of(ws); out=[]
    hdr=None
    for i,r in enumerate(rs):
        if r and str(r[0]).strip().upper().startswith("STATE"): hdr=i; break
    if hdr is None: return out
    asof=rs[hdr][1]
    for r in rs[hdr+1:]:
        st=r[0]; v=num(r[1]) if len(r)>1 else None
        if st and v is not None: out.append({"state":str(st).strip(),"as_of":str(asof)[:10],"value":v})
    return out

# B) refinery capacity
def parse_refcap(ws):
    rs=rows_of(ws); out=[]; hdr=None
    for i,r in enumerate(rs):
        if any(str(c).strip().upper()=="REFINERIES" for c in r if c): hdr=i; break
    if hdr is None: return out
    asof=rs[hdr][-1]; company=None
    for r in rs[hdr+1:]:
        comp=r[1] if len(r)>1 else None
        refi=r[2] if len(r)>2 else None
        state=r[3] if len(r)>3 else None
        cap=num(r[4]) if len(r)>4 else None
        if comp and str(comp).strip(): company=str(comp).strip()
        if refi and cap is not None:
            out.append({"company":company,"refinery":str(refi).strip(),"state":(str(state).strip() if state else None),"capacity":cap,"as_of":str(asof)})
    return out

# C) state-wise consumption (year columns, region headers, multi-sheet)
def parse_statewise(wb):
    out=[]
    for ws in wb.worksheets:
        rs=rows_of(ws); hdr=None
        for i,r in enumerate(rs):
            if r and str(r[0]).strip().upper().startswith("STATE"): hdr=i; break
        if hdr is None: continue
        years=[(j,str(y).strip()) for j,y in enumerate(rs[hdr]) if j>=1 and y and re.match(r'\d{4}-\d{2,4}',str(y).strip())]
        region=None
        for r in rs[hdr+1:]:
            lbl=r[0]
            if not lbl: continue
            lbl=str(lbl).strip()
            vals=[num(r[j]) if j<len(r) else None for j,_ in years]
            if all(v is None for v in vals):
                if lbl.upper().startswith("REGION"): region=lbl
                continue
            for (j,yr),v in zip(years,vals):
                if v is not None: out.append({"sheet":ws.title.strip(),"region":region,"state":lbl,"fiscal_year":yr,"value":v})
    return out

# D) LNG import main sheet
def parse_lng(wb):
    ws=wb.worksheets[0]; rs=rows_of(ws); out=[]; hdr=None
    for i,r in enumerate(rs):
        if r and str(r[0]).strip().lower()=="year": hdr=i; break
    if hdr is None: return out
    years=[(j,str(y).strip()) for j,y in enumerate(rs[hdr]) if j>=1 and re.match(r'\d{4}-\d{2}',str(y).strip() if y else '')]
    for r in rs[hdr+1:]:
        lbl=r[0]
        if not lbl: continue
        for j,yr in years:
            v=num(r[j]) if j<len(r) else None
            if v is not None: out.append({"metric":str(lbl).strip(),"fiscal_year":yr,"value":v})
    return out

for p,fn in [("consumption/active-domestic-customers","snap"),("consumption/state-wise-pmuy-data","snap"),
             ("infrastructure/installed-refinery-capacity","ref"),("consumption/state-wise","sw"),
             ("natural-gas/import","lng")]:
    wb,fname=load(p)
    if fn=="snap": o=parse_snapshot(wb.worksheets[0])
    elif fn=="ref": o=parse_refcap(wb.worksheets[0])
    elif fn=="sw": o=parse_statewise(wb)
    elif fn=="lng": o=parse_lng(wb)
    print(f"\n### {p} ({fname}) -> {len(o)} rows")
    for r in o[:3]: print("   ",r)
    for r in o[-2:]: print("   ",r)
