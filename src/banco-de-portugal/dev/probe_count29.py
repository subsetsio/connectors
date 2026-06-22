import sys; sys.path.insert(0,"src")
from subsets_utils import get
r=get("https://bpstat.bportugal.pt/data/v1/domains/29/datasets/23e0cdd56bddb4ad3016a9c3ad63a539/",
      params={"lang":"EN","page":1,"page_size":1}, timeout=(10,180))
d=r.json()
print("status",r.status_code,"len",len(r.text))
# count metadata
print("size dims:", d.get("size"))
print("num series on this page:", len(d.get("extension",{}).get("series",[])))
# the dataset listing tells num_series
r2=get("https://bpstat.bportugal.pt/data/v1/domains/29/datasets/",params={"lang":"EN"},timeout=(10,120))
ds=r2.json()
items=ds.get("link",{}).get("item",[])
for it in items:
    if it.get("id")=="23e0cdd56bddb4ad3016a9c3ad63a539" or it.get("href","").endswith("23e0cdd56bddb4ad3016a9c3ad63a539/"):
        print("dataset meta:", {k:it.get(k) for k in ("id","num_series","label")})
