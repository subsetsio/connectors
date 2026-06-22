import io, re, json
import pandas as pd
from bs4 import BeautifulSoup

MONTHS={"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,"jul":7,"ago":8,
        "sep":9,"set":9,"oct":10,"nov":11,"dic":12}
QUARTERS={"i":1,"ii":4,"iii":7,"iv":10}
SKIP_PERIOD={"total","promedio","prom","acumulado","anual","prom.","promedio1/"}
NULLS={"","-","--","---","...","..","n.d.","nd","n/d","s.d.","sd","na","n.a."}

def _grid(content):
    if content[:4]==b"\xD0\xCF\x11\xE0":
        df=pd.read_excel(io.BytesIO(content),engine="xlrd",header=None)
        return [[("" if pd.isna(x) else str(x)).strip() for x in df.iloc[i].tolist()]
                for i in range(len(df))]
    h=content.decode("iso-8859-1","replace")
    soup=BeautifulSoup(h,"html5lib")
    return [[c.get_text(strip=True) for c in tr.find_all(["td","th"])]
            for tr in soup.find_all("tr")]

def _norm(s): return s.lower().strip().rstrip(".").replace(" ","")

def _num(s):
    s=s.strip()
    if _norm(s) in NULLS: return None
    neg=False
    if s.startswith("(") and s.endswith(")"): neg=True; s=s[1:-1]
    s=s.replace(",","").replace("%","").strip()
    s=re.sub(r"\s+","",s)
    try: v=float(s)
    except ValueError: return None
    return -v if neg else v

def parse(content):
    g=_grid(content)
    # collapse fully-empty cells but keep positions; find header row with 'año'
    hidx=None
    for i,row in enumerate(g):
        cells=[c for c in row]
        first=next((c for c in cells if c.strip()),"")
        if _norm(first) in ("año","ano","ańo") or _norm(first).startswith("año"):
            hidx=i; header=[c for c in row if c.strip()!=""]
            break
    if hidx is None:
        raise ValueError("no header row")
    period_labels=header[1:]  # after 'Año'
    out=[]
    for row in g[hidx+1:]:
        cells=[c for c in row if c.strip()!=""]
        if not cells: continue
        m=re.match(r"^\s*(\d{4})",cells[0])
        if not m: continue
        year=int(m.group(1))
        if not (1900<=year<=2100): continue
        vals=cells[1:]
        for ci,lab in enumerate(period_labels):
            nlab=_norm(lab)
            if nlab in SKIP_PERIOD: continue
            if ci>=len(vals): continue
            v=_num(vals[ci])
            if v is None: continue
            month=MONTHS.get(nlab) or QUARTERS.get(nlab)
            date=f"{year}-{month:02d}-01" if month else None
            out.append({"year":year,"col_index":ci,"month":month,
                        "date":date,"period_label":lab,"value":v})
    return out

if __name__=="__main__":
    from subsets_utils import get
    BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
    ids=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/banco-central-de-nicaragua/work/entity_union.json"))
    if isinstance(ids,dict): ids=list(ids)
    import collections
    tot=0; empties=[]; nodate=[]
    for eid in ids:
        r=get(BASE+eid+".xls",timeout=(10,60))
        rows=parse(r.content)
        tot+=len(rows)
        if not rows: empties.append(eid)
        nd=sum(1 for x in rows if x["date"] is None)
        if nd: nodate.append((eid,nd))
    print("total rows",tot,"entities",len(ids))
    print("EMPTY",empties)
    print("rows with no date (non month/quarter):",sum(n for _,n in nodate),"in",len(nodate),"tables")
    # show a sample
    r=get(BASE+"4.IMAE.xls",timeout=(10,60))
    print("IMAE sample",parse(r.content)[:3], "n=",len(parse(r.content)))
    r=get(BASE+"1a.15.1.xls",timeout=(10,60))
    s=parse(r.content); print("1a.15.1 (dup quarter) n=",len(s),"sample",s[:6])
