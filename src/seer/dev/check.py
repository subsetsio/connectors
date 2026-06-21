import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import load_raw_ndjson
from collections import defaultdict
rows = load_raw_ndjson("seer-prevalence-complete")
bysite = defaultdict(lambda:[0,0])
for r in rows:
    s=r.get("site"); v=r.get("percent")
    bysite[s][0]+=1
    if v is None: bysite[s][1]+=1
# sites fully null?
fully_null=[s for s,(n,nul) in bysite.items() if n==nul]
print("total sites:", len(bysite), "fully-null sites:", len(fully_null))
print("sample fully-null:", fully_null[:10])
# overall null rate
tot=sum(n for n,_ in bysite.values()); nul=sum(x for _,x in bysite.values())
print(f"overall percent-null rate: {nul}/{tot} = {nul/tot:.2%}")
# show a couple sites with their nonnull counts
for s,(n,nl) in list(bysite.items())[:5]:
    print(f"  {s}: {n} rows, {nl} null percent")
