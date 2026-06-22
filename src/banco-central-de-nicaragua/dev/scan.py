import io, json, collections
import pandas as pd
from bs4 import BeautifulSoup
from subsets_utils import get

BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
ids=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/banco-central-de-nicaragua/work/entity_union.json"))
if isinstance(ids,dict): ids=list(ids)

def grid_from(content):
    if content[:4]==b"\xD0\xCF\x11\xE0":
        df=pd.read_excel(io.BytesIO(content),engine="xlrd",header=None)
        return [[("" if pd.isna(x) else str(x)).strip() for x in df.iloc[i].tolist()] for i in range(len(df))], "bin"
    h=content.decode("iso-8859-1","replace")
    soup=BeautifulSoup(h,"html5lib")
    g=[]
    for tr in soup.find_all("tr"):
        g.append([c.get_text(strip=True) for c in tr.find_all(["td","th"])])
    return g,"html"

MONTHS={"ene","feb","mar","abr","may","jun","jul","ago","sep","set","oct","nov","dic"}
def norm(s): return s.lower().strip().strip(".").replace(" ","")[:3]

hdrsets=collections.Counter()
fmts=collections.Counter()
problems=[]
for i,eid in enumerate(ids):
    try:
        r=get(BASE+eid+".xls",timeout=(10,60))
        g,fmt=grid_from(r.content)
        fmts[fmt]+=1
        # find header row containing 'año'/'year'
        hrow=None
        for row in g:
            low=[c.lower() for c in row]
            if any(c.startswith("a") and "o" in c and "a\xf1o"==c.replace(" ","") or c.strip().lower().startswith("a\xf1o") for c in low):
                hrow=row; break
            if any("a\xf1o" in c for c in low):
                hrow=row; break
        if hrow is None:
            problems.append((eid,fmt,"no-header",[ [c for c in rr if c][:6] for rr in g[:6]]))
            continue
        # period columns = cells after first that are month-like
        cols=[c for c in hrow if c]
        periodcols=[c for c in cols[1:] if norm(c) in MONTHS]
        key=(len(cols), tuple(norm(c) in MONTHS for c in cols[1:]))
        hdrsets[tuple(cols)]+=1
    except Exception as e:
        problems.append((eid,"ERR",str(e)[:80],None))
print("FORMATS",dict(fmts))
print("PROBLEMS",len(problems))
for p in problems[:40]: print("  PROB",p[0],p[1],p[2])
print("DISTINCT HEADER ROWS",len(hdrsets))
for hdr,cnt in hdrsets.most_common(25):
    print(f"  [{cnt}] {list(hdr)}")
