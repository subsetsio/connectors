import json
from subsets_utils import get
ids=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/canadian-centre-for-energy-information/work/entity_union.json"))
base="https://energy-information.canada.ca/sdmx/rest/data/"
bad=[]
empty=[]
for eid in ids:
    agency,flow=eid.split(":",1)
    url=f"{base}{agency},{flow}/?detail=serieskeysonly"
    try:
        r=get(url, headers={"Accept":"text/csv"}, timeout=(10,120))
        if r.status_code!=200:
            bad.append((eid,r.status_code)); continue
        n=len(r.text.splitlines())-1
        if n<=0:
            empty.append(eid)
    except Exception as e:
        bad.append((eid,type(e).__name__))
print("total",len(ids))
print("BAD",len(bad)); [print("  ",b) for b in bad]
print("EMPTY",len(empty)); [print("  ",e) for e in empty]
