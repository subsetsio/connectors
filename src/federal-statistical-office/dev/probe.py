import json
from subsets_utils import get, post
U="https://www.pxweb.bfs.admin.ch/api/v1/en/px-x-0102020000_201/px-x-0102020000_201.px"
m=get(U, timeout=60).json()
vars={v["code"]:v["values"] for v in m["variables"]}
geo=[c for c,vv in vars.items() if len(vv)>100][0]
q=[{"code":c,"selection":{"filter":"item","values":(vars[c][:2] if c==geo else vars[c])}} for c in vars]
r=post(U, json={"query":q,"response":{"format":"json-stat2"}}, timeout=120)
d=r.json()
print("keys:", list(d.keys()))
print("id:", d["id"])
print("size:", d["size"])
print("value len:", len(d["value"]), "expected:", 1)
import math
print("product:", math.prod(d["size"]))
# show one dimension structure
dim0=d["id"][0]
cat=d["dimension"][dim0]["category"]
print("dim0", dim0, "index sample:", dict(list(cat["index"].items())[:3]), "label sample:", dict(list(cat.get("label",{}).items())[:3]))
print("value sample:", d["value"][:5])
