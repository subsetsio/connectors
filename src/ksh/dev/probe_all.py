import csv, io, json
import xml.etree.ElementTree as ET
from subsets_utils import get
from constants import ENTITY_META, ENTITY_IDS

def _ln(t): return t.rsplit("}",1)[-1]
def parse_csv(text):
    rows=list(csv.reader(io.StringIO(text),delimiter=";"))
    if not rows: return [],[]
    header=[h.strip() for h in rows[0]]
    out=[]
    for raw in rows[1:]:
        if not any(c.strip() for c in raw): continue
        d={}
        for i,col in enumerate(header):
            if not col: continue
            v=raw[i].strip() if i<len(raw) else ""
            d[col]=v if v!="" else None
        out.append(d)
    return out,[h for h in header if h]
def parse_xml(text):
    root=ET.fromstring(text.encode("utf-8")); out=[]; cols=set()
    for el in root.iter():
        if _ln(el.tag)!="Series": continue
        sa=dict(el.attrib)
        obs=[c for c in el if _ln(c.tag)=="Obs"]
        for o in (obs or [None]):
            row=dict(sa)
            if o is not None: row.update(o.attrib)
            row={k:(v if v!="" else None) for k,v in row.items()}
            cols.update(row); out.append(row)
    return out,sorted(cols)

import sys
summary={}
for rid in ENTITY_IDS:
    m=ENTITY_META[rid]
    r=get(f"https://data.ksh.hu/datasets/{m['dataset_id']}/data/{rid}.{m['format']}",timeout=120)
    if m["format"]=="csv":
        rows,cols=parse_csv(r.content.decode("utf-8-sig","replace"))
    else:
        rows,cols=parse_xml(r.content.decode("utf-8","replace"))
    summary[rid]={"fmt":m["format"],"n":len(rows),"cols":cols}
    print(m["format"], len(rows), rid[:8], cols[:12])
json.dump(summary,open("/Users/nathansnellaert/Documents/hardened/connectors/src/ksh/dev/summary.json","w"))
print("TOTAL rows:", sum(s["n"] for s in summary.values()))
print("min rows:", min(s["n"] for s in summary.values()))
