import sys, json, math
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,"src")
from subsets_utils import get
from constants import ENTITY_PATHS
BASE="https://data.stat.gov.lv/api/v1/en/OSP_PUB/"

def size_one(item):
    stem, px = item
    try:
        m=get(BASE+px, timeout=(10,60)).json()
        prod=1; has_empty=False; maxv=0
        for v in m["variables"]:
            n=len(v.get("values") or [])
            if n==0: has_empty=True; n=6000  # estimate for uncountable
            prod*=n; maxv=max(maxv,n)
        return (stem, prod, has_empty, maxv)
    except Exception as e:
        return (stem, -1, False, 0)

items=list(ENTITY_PATHS.items())
res=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    for r in ex.map(size_one, items):
        res.append(r)

errs=[r for r in res if r[1]==-1]
print("errors:", len(errs))
import collections
# cell-count buckets
def bucket(c):
    if c<0: return "err"
    if c<=100_000: return "<=100k (1 query)"
    if c<=1_000_000: return "<=1M"
    if c<=10_000_000: return "<=10M"
    if c<=100_000_000: return "<=100M"
    return ">100M"
b=collections.Counter(bucket(r[1]) for r in res)
for k in ["<=100k (1 query)","<=1M","<=10M","<=100M",">100M","err"]:
    print(f"  {k}: {b.get(k,0)}")
empt=[r for r in res if r[2]]
print("tables with uncountable dim:", len(empt))
big=[r for r in res if r[1]>10_000_000]
print("tables >10M cells:", len(big))
# est total queries at 90k/query
totq=sum(max(1, math.ceil(r[1]/90000)) for r in res if r[1]>0)
print("estimated total POST queries (full pull):", totq)
json.dump([(r[0],r[1],r[2]) for r in res], open("dev/sizes.json","w"))
print("wrote dev/sizes.json")
