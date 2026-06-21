import json
from subsets_utils import get
ids=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/canadian-centre-for-energy-information/work/entity_union.json"))
base="https://energy-information.canada.ca/sdmx/rest/data/"
bad=[]; empty=[]; ok=0
for eid in ids:
    agency,flow=eid.split(":",1)
    url=f"{base}{agency},{flow}/?firstNObservations=1"
    try:
        r=get(url, headers={"Accept":"text/csv"}, timeout=(10,120))
        if r.status_code!=200:
            bad.append((eid,r.status_code)); continue
        lines=[l for l in r.text.splitlines() if l.strip()]
        if len(lines)<2:
            empty.append(eid)
        else:
            ok+=1
    except Exception as e:
        bad.append((eid,type(e).__name__))
print("RESULT total",len(ids),"ok",ok,"bad",len(bad),"empty",len(empty))
print("BAD_LIST",json.dumps(bad))
print("EMPTY_LIST",json.dumps(empty))
