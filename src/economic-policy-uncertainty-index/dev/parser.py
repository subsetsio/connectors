import datetime as _dt
import re
import pandas as pd

DATE_TOKENS = {"year","month","day","date","datem","quarter","qtr","time","period",
               "observation_date","yyyymm","yearmonth"}
_PERIOD_M = re.compile(r"^\s*(\d{4})[mM](\d{1,2})\s*$")
_PERIOD_Q = re.compile(r"^\s*(\d{4})[qQ](\d)\s*$")
_ISO      = re.compile(r"^\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})")
_DMY      = re.compile(r"^\s*(\d{1,2})[-/](\d{1,2})[-/](\d{4})\s*$")
_YEAR     = re.compile(r"^\s*(\d{4})\s*$")
_THOUS    = re.compile(r"^-?\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
_EUDEC    = re.compile(r"^-?\d+,\d+$")

def _norm(x):
    if x is None: return ""
    s=str(x).strip()
    return "" if s=="" or s.lower()=="nan" else s.lower()

def _orig(x):
    if x is None: return ""
    s=str(x).strip()
    return "" if s.lower()=="nan" else s

def _to_float(x):
    if x is None: return None
    if isinstance(x,(int,float)):
        try:
            f=float(x)
            return None if f!=f else f
        except (ValueError, OverflowError):
            return None
    s=str(x).strip()
    if s=="" or s.lower()=="nan": return None
    s=s.replace("−","-").replace("%","").strip()
    if _THOUS.match(s): s=s.replace(",","")
    elif _EUDEC.match(s): s=s.replace(",",".")
    try: return float(s)
    except ValueError: return None

def _parse_any_date(v):
    if v is None: return None
    if isinstance(v,(pd.Timestamp,_dt.datetime,_dt.date)):
        try: return pd.Timestamp(v).date()
        except (ValueError, OverflowError): return None
    s=str(v).strip()
    if s=="" or s.lower()=="nan": return None
    m=_PERIOD_M.match(s)
    if m:
        y,mo=int(m.group(1)),int(m.group(2))
        if 1<=mo<=12: return _dt.date(y,mo,1)
        return None
    m=_PERIOD_Q.match(s)
    if m:
        y,q=int(m.group(1)),int(m.group(2))
        if 1<=q<=4: return _dt.date(y,(q-1)*3+1,1)
        return None
    m=_ISO.match(s)
    if m:
        try: return _dt.date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
        except ValueError: return None
    m=_DMY.match(s)
    if m:
        try: return _dt.date(int(m.group(3)),int(m.group(2)),int(m.group(1)))
        except ValueError: return None
    m=_YEAR.match(s)
    if m:
        y=int(m.group(1))
        if 1850<=y<=2100: return _dt.date(y,1,1)
    return None

def _is_datelike(v):
    return _parse_any_date(v) is not None and not isinstance(v,(int,float))

def _col_datelike_frac(body, ci, limit=40):
    vals=[v for v in body[ci].tolist() if _norm(v)!=""][:limit]
    if not vals: return 0.0
    return sum(1 for v in vals if _parse_any_date(v) is not None)/len(vals)

def _find_header(raw):
    n=min(len(raw),25)
    # primary: a row carrying a date-ish token
    for r in range(n):
        cells=[_norm(c) for c in raw.iloc[r].tolist()]
        if sum(1 for c in cells if c)<2: continue
        if any(c in DATE_TOKENS or c.startswith("date") for c in cells):
            return r
    # fallback: first datelike data row -> header is the row above
    for r in range(1,min(len(raw),25)):
        row=raw.iloc[r].tolist()
        if any(_is_datelike(v) for v in row):
            return r-1
    return None

def _roles(headers):
    roles={}
    for ci,h in enumerate(headers):
        if not h: continue
        if h in ("date","datem","observation_date","time","period","yyyymm","yearmonth") or h.startswith("date"):
            roles[ci]="date"
        elif h=="year": roles[ci]="year"
        elif h=="month": roles[ci]="month"
        elif h=="day": roles[ci]="day"
        elif h in ("quarter","qtr"): roles[ci]="quarter"
    return roles

def _build_dates(body, roles, headers):
    ycols=[c for c,r in roles.items() if r=="year"]
    if ycols:
        y=pd.to_numeric(body[ycols[0]],errors="coerce")
        qcols=[c for c,r in roles.items() if r=="quarter"]
        mcols=[c for c,r in roles.items() if r=="month"]
        dcols=[c for c,r in roles.items() if r=="day"]
        if qcols:
            q=pd.to_numeric(body[qcols[0]],errors="coerce"); m=(q-1)*3+1
        elif mcols:
            m=pd.to_numeric(body[mcols[0]],errors="coerce")
            nn=m.dropna()
            if len(nn) and nn.median()>12:        # packed YYYYMM
                y=(m//100); m=(m%100)
        else:
            m=pd.Series([1]*len(body))
        d=pd.to_numeric(body[dcols[0]],errors="coerce") if dcols else pd.Series([1]*len(body))
        out=[]
        for yy,mm,dd in zip(y,m,d):
            try:
                out.append(_dt.date(int(yy),
                                    int(mm) if pd.notna(mm) and 1<=int(mm)<=12 else 1,
                                    int(dd) if pd.notna(dd) and 1<=int(dd)<=31 else 1))
            except (ValueError,TypeError):
                out.append(None)
        return pd.Series(out), set(ycols)|set(qcols)|set(mcols)|set(dcols)
    # no year: find a single date column
    date_ci=None
    for c,r in roles.items():
        if r=="date": date_ci=c; break
    if date_ci is None:
        for c,r in roles.items():
            if _col_datelike_frac(body,c)>=0.6: date_ci=c; break
    if date_ci is None:
        for ci in range(body.shape[1]):
            if _col_datelike_frac(body,ci)>=0.6: date_ci=ci; break
    if date_ci is None: return None, set()
    return body[date_ci].map(_parse_any_date), {date_ci}

def parse_sheet(raw, sheet_label):
    hr=_find_header(raw)
    if hr is None: return []
    headers_lc=[_norm(c) for c in raw.iloc[hr].tolist()]
    headers_orig=[_orig(c) for c in raw.iloc[hr].tolist()]
    body=raw.iloc[hr+1:].reset_index(drop=True)
    body.columns=range(body.shape[1])
    roles=_roles(headers_lc)
    dates,datecols=_build_dates(body,roles,headers_lc)
    if dates is None: return []
    cand=[ci for ci in range(body.shape[1]) if ci not in datecols and headers_orig[ci]]
    measures=[]; dims=[]
    n=len(body)
    for ci in cand:
        vals=body[ci].tolist()
        nonnull=[v for v in vals if _norm(v)!=""]
        if not nonnull: continue
        nnum=sum(1 for v in nonnull if _to_float(v) is not None)
        if nnum>=0.6*len(nonnull):
            measures.append(ci)
        else:
            distinct=len(set(str(v).strip() for v in nonnull))
            if len(nonnull)>=0.9*n and 2<=distinct<=0.5*len(nonnull):
                dims.append(ci)
    if not measures: return []
    multi_measure=len(measures)>1
    rows=[]
    dvals=dates.tolist()
    for i in range(n):
        dt=dvals[i] if i<len(dvals) else None
        if dt is None or (isinstance(dt,float)): continue
        dimvals=[str(body[ci].iloc[i]).strip() for ci in dims if _norm(body[ci].iloc[i])!=""]
        for m in measures:
            v=_to_float(body[m].iloc[i])
            if v is None: continue
            parts=list(dimvals)
            if multi_measure or not dimvals:
                parts.append(headers_orig[m])
            series=" | ".join(p for p in parts if p)
            if series:
                rows.append((dt,series,v))
    return rows

def parse_file(path, fn):
    if fn.lower().endswith(".csv"):
        with open(path,encoding="utf-8",errors="replace") as fh:
            first=fh.readline()
        sep=";" if first.count(";")>first.count(",") else ","
        raw=pd.read_csv(path,header=None,dtype=object,sep=sep,keep_default_na=True,
                        na_values=[""],encoding="utf-8",on_bad_lines="skip")
        sheets=[("",raw)]
    else:
        xl=pd.ExcelFile(path)
        sheets=[(s,pd.read_excel(path,sheet_name=s,header=None,dtype=object)) for s in xl.sheet_names]
    per=[]
    for label,raw in sheets:
        try: r=parse_sheet(raw,label)
        except Exception: r=[]
        if r: per.append((label,r))
    multi=len(per)>1
    rows=[]
    for label,r in per:
        if multi and label:
            r=[(d,f"{label} :: {s}",v) for (d,s,v) in r]
        rows.extend(r)
    seen={}
    for d,s,v in rows: seen[(d,s)]=v
    return [(d,s,v) for (d,s),v in seen.items()]

if __name__=="__main__":
    import json,sys
    mapping=json.load(open("dev/mapping.json"))
    names=sys.argv[1:] or list(mapping.values())
    bad=[]
    for fn in names:
        try:
            rows=parse_file("dev/files/"+fn,fn)
            if not rows: print(f"!!! ZERO {fn}"); bad.append(fn); continue
            ds=sorted(set(s for _,s,_ in rows)); dts=sorted(set(d for d,_,_ in rows))
            print(f"OK {fn}: rows={len(rows)} series={len(ds)} {dts[0]}..{dts[-1]} | {ds[:3]}")
        except Exception as e:
            import traceback; traceback.print_exc(); print(f"ERR {fn}: {e}"); bad.append(fn)
    print("\nBAD:",bad)
