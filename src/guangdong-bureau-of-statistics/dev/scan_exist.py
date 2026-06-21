import json, concurrent.futures as cf
from subsets_utils import get

cat=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/guangdong-bureau-of-statistics/assets/collect/entities/current.json"))
union=set(json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/guangdong-bureau-of-statistics/work/entity_union.json")))
base="http://tjnj.gdstats.gov.cn:8080/tjnj/2025/directory"

# build entity -> parts (only union entities)
ents={eid:e["source_metadata"]["parts"] for eid,e in cat.items() if eid in union}
allparts=[(eid,p) for eid,ps in ents.items() for p in ps]
print("union entities:",len(ents),"total parts:",len(allparts))

def check(item):
    eid,p=item
    ch=p[:2]
    url=f"{base}/{ch}/excel/{p}.xls"
    try:
        r=get(url,timeout=(8,40))
        ok = r.status_code==200 and r.content[:2]==b'\xd0\xcf'
        return (eid,p,r.status_code,ok)
    except Exception as ex:
        return (eid,p,f"ERR:{type(ex).__name__}",False)

bad=[]
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for eid,p,st,ok in ex.map(check,allparts):
        if not ok: bad.append((eid,p,st))

print("missing/bad parts:",len(bad))
# entities with ALL parts bad (fully missing) vs partial
from collections import defaultdict
badparts=defaultdict(list)
for eid,p,st in bad: badparts[eid].append((p,st))
fully=[eid for eid in badparts if len(badparts[eid])==len(ents[eid])]
partial=[eid for eid in badparts if 0<len(badparts[eid])<len(ents[eid])]
print("entities fully missing:",len(fully))
print("entities partially missing:",len(partial))
print("FULLY MISSING:",sorted(fully))
print("PARTIAL:",[(e,badparts[e]) for e in sorted(partial)])
