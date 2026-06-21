import json
from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"  # 917 series, domain 3
d=get(f"{BASE}/domains/3/datasets/{ds}/?lang=EN", timeout=(10,120)).json()
size=d["size"]; ids=d["id"]
import math
prod=math.prod(size)
print("num_series:", d["extension"]["num_series"])
print("ids:", ids)
print("size:", size, "product:", prod)
v=d["value"]
print("value type:", type(v).__name__, "len:", len(v))
if isinstance(v,dict):
    print("sparse dict sample:", list(v.items())[:5])
    print("non-null count:", len(v))
else:
    nn=sum(1 for x in v if x is not None)
    print("dense list, non-null:", nn)
# reference_date dimension
rd=d["dimension"]["reference_date"]
print("\nreference_date keys:", list(rd.keys()))
cat=rd["category"]
print("ref category keys:", list(cat.keys()))
idx=cat["index"]
print("ref index type:", type(idx).__name__, "len:", len(idx) if hasattr(idx,'__len__') else "?")
if isinstance(idx,dict):
    print("ref index sample:", list(idx.items())[:3])
elif isinstance(idx,list):
    print("ref index sample:", idx[:3])
# one non-date dimension structure
nd=ids[0]
dim=d["dimension"][nd]
print("\nnon-date dim", nd, "keys:", list(dim.keys()))
print("category index sample:", list(dim["category"]["index"].items())[:3] if isinstance(dim["category"]["index"],dict) else dim["category"]["index"][:3])
print("category label sample:", list(dim["category"].get("label",{}).items())[:3])
print("\nseries count in extension:", len(d["extension"]["series"]))
