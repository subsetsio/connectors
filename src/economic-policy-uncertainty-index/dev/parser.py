import datetime as _dt
import pandas as pd

DATE_TOKENS = {"year","month","day","date","datem","quarter","qtr","time","period",
               "observation_date","yyyymm","yearmonth"}

def _norm(x):
    return str(x).strip().lower() if x is not None and str(x).strip()!="" and str(x).lower()!="nan" else ""

def _to_float(x):
    if x is None: return None
    s=str(x).strip()
    if s=="" or s.lower()=="nan": return None
    s=s.replace(",","").replace("%","").replace("−","-")
    try: return float(s)
    except ValueError: return None

def _find_header(raw, max_scan=25):
    n=min(len(raw), max_scan)
    for r in range(n):
        cells=[_norm(c) for c in raw.iloc[r].tolist()]
        if any(c in DATE_TOKENS for c in cells):
            # need at least 2 non-empty header cells
            if sum(1 for c in cells if c)>=2:
                return r
    return None

def _build_dates(df, roles):
    # roles: dict col-> role in {year,month,day,quarter,date}
    if "date" in roles.values():
        dcol=[c for c,r in roles.items() if r=="date"][0]
        return pd.to_datetime(df[dcol], errors="coerce").dt.date
    ycol=[c for c,r in roles.items() if r=="year"]
    if not ycol: return None
    y=pd.to_numeric(df[ycol[0]], errors="coerce")
    qcol=[c for c,r in roles.items() if r=="quarter"]
    mcol=[c for c,r in roles.items() if r=="month"]
    dcol=[c for c,r in roles.items() if r=="day"]
    if qcol:
        q=pd.to_numeric(df[qcol[0]], errors="coerce")
        m=(q-1)*3+1
    elif mcol:
        m=pd.to_numeric(df[mcol[0]], errors="coerce")
    else:
        m=pd.Series([1]*len(df))
    d=pd.to_numeric(df[dcol[0]], errors="coerce") if dcol else pd.Series([1]*len(df))
    out=[]
    for yy,mm,dd in zip(y,m,d):
        try:
            out.append(_dt.date(int(yy), int(mm) if pd.notna(mm) and 1<=int(mm)<=12 else 1,
                                int(dd) if pd.notna(dd) and 1<=int(dd)<=31 else 1))
        except (ValueError, TypeError):
            out.append(None)
    return pd.Series(out)

def _classify(series_vals):
    sample=[v for v in series_vals[:80] if _norm(v)!=""]
    if not sample: return "measure"   # empty -> treat as sparse measure
    num=sum(1 for v in sample if _to_float(v) is not None)
    return "measure" if num >= 0.6*len(sample) else "dim"

def parse_sheet(raw, sheet_label):
    """raw: DataFrame read with header=None, dtype object. Returns list of (date,series,value)."""
    hr=_find_header(raw)
    if hr is None: return []
    headers=[_norm(c) for c in raw.iloc[hr].tolist()]
    body=raw.iloc[hr+1:].reset_index(drop=True)
    body.columns=range(body.shape[1])
    # assign roles
    roles={}
    used=set()
    for ci,h in enumerate(headers):
        if not h: continue
        if h in ("date","datem","observation_date","time","period","yyyymm","yearmonth"):
            roles[ci]="date"
        elif h=="year": roles[ci]="year"
        elif h=="month": roles[ci]="month"
        elif h=="day": roles[ci]="day"
        elif h in ("quarter","qtr"): roles[ci]="quarter"
    if not roles: return []
    dates=_build_dates(body, roles)
    if dates is None: return []
    datecols=set(roles)
    # candidate value/dim columns: header non-empty, not a date col
    cand=[ci for ci,h in enumerate(headers) if h and ci not in datecols]
    dims=[ci for ci in cand if _classify(body[ci].tolist())=="dim"]
    measures=[ci for ci in cand if ci not in dims]
    rows=[]
    multi_measure = len(measures)>1
    for i in range(len(body)):
        dt=dates.iloc[i] if i < len(dates) else None
        if dt is None or pd.isna(dt): continue
        dimvals=[str(body[ci].iloc[i]).strip() for ci in dims if _norm(body[ci].iloc[i])!=""]
        for m in measures:
            v=_to_float(body[m].iloc[i])
            if v is None: continue
            parts=list(dimvals)
            if multi_measure or not dimvals:
                parts.append(headers_orig.get((sheet_label,m), str(headers[m])))
            series=" | ".join([p for p in parts if p])
            if not series: continue
            rows.append((dt, series, v))
    return rows

# we need original (non-lowercased) header text for measure names
headers_orig={}

def parse_file(path, fn):
    global headers_orig
    rows=[]
    if fn.lower().endswith(".csv"):
        raw=pd.read_csv(path, header=None, dtype=object, keep_default_na=False, na_values=[""])
        sheets=[("",raw)]
    else:
        xl=pd.ExcelFile(path)
        sheets=[(s, pd.read_excel(path, sheet_name=s, header=None, dtype=object)) for s in xl.sheet_names]
    # build original header map per sheet
    parsed_sheets=[]
    for label, raw in sheets:
        hr=_find_header(raw)
        if hr is None: continue
        orig=[("" if (c is None or str(c).lower()=="nan") else str(c).strip()) for c in raw.iloc[hr].tolist()]
        for ci,h in enumerate(orig):
            headers_orig[(label,ci)]=h
        parsed_sheets.append((label,raw))
    multi = len(parsed_sheets)>1
    for label, raw in parsed_sheets:
        srows=parse_sheet(raw, label)
        if multi and label:
            srows=[(d, f"{label} :: {s}", v) for (d,s,v) in srows]
        rows.extend(srows)
    # dedup (date,series) keep last
    seen={}
    for d,s,v in rows:
        seen[(d,s)]=v
    return [(d,s,v) for (d,s),v in seen.items()]

if __name__=="__main__":
    import json, sys
    mapping=json.load(open("dev/mapping.json"))
    names=sys.argv[1:] or list(mapping.values())
    bad=[]
    for fn in names:
        try:
            rows=parse_file("dev/files/"+fn, fn)
            if not rows:
                print(f"!!! ZERO {fn}"); bad.append(fn); continue
            ds=sorted(set(s for _,s,_ in rows))
            dts=sorted(set(d for d,_,_ in rows))
            print(f"OK {fn}: rows={len(rows)} series={len(ds)} dates={dts[0]}..{dts[-1]} | sample series: {ds[:3]}")
        except Exception as e:
            import traceback; print(f"ERR {fn}: {type(e).__name__}: {e}"); bad.append(fn)
    print("\nBAD:", bad)
