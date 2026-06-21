import sys, json, math, collections
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _get_json, BASE
from constants import ENTITY_PATHS

res=[]
for i,(stem,px) in enumerate(ENTITY_PATHS.items()):
    try:
        m=_get_json(BASE+px)
        prod=1; has_empty=False
        for v in m["variables"]:
            n=len(v.get("values") or [])
            if n==0: has_empty=True; n=6000
            prod*=n
        res.append((stem,prod,has_empty))
    except Exception as e:
        res.append((stem,-1,False))
    if (i+1)%200==0: print("...",i+1, file=sys.stderr)

errs=[r for r in res if r[1]==-1]
print("errors:", len(errs))
def bucket(c):
    if c<0: return "err"
    if c<=100_000: return "<=100k"
    if c<=1_000_000: return "<=1M"
    if c<=10_000_000: return "<=10M"
    if c<=100_000_000: return "<=100M"
    return ">100M"
b=collections.Counter(bucket(r[1]) for r in res)
for k in ["<=100k","<=1M","<=10M","<=100M",">100M","err"]:
    print(f"  {k}: {b.get(k,0)}")
print("uncountable-dim tables:", sum(1 for r in res if r[2]))
print(">2M cells:", sum(1 for r in res if r[1]>2_000_000))
totq=sum(max(1,math.ceil(r[1]/90000)) for r in res if r[1]>0)
print("est total POST queries:", totq)
json.dump(res, open("dev/sizes.json","w"))
