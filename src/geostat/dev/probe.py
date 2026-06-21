import math, json
from subsets_utils import get, post

BASE = "https://pc-axis.geostat.ge/PXWeb/api/v1/en/Database/"
# a 3-dim table (Holding Type, Categories, Year) to validate decode
path = "Agriculture/Animal%20Husbandry/TABLE_3.18.px"

m = get(BASE+path, timeout=(10,60), verify=False).json()
print("TITLE:", m["title"])
for v in m["variables"]:
    print("  var", repr(v["code"]), "n=", len(v["values"]), "sample_labels=", v.get("valueTexts", v["values"])[:3])
total = math.prod(len(v["values"]) for v in m["variables"])
print("total cells:", total)

query=[{"code":v["code"],"selection":{"filter":"all","values":["*"]}} for v in m["variables"]]
r = post(BASE+path, json={"query":query,"response":{"format":"json-stat"}}, timeout=(10,120), verify=False)
print("POST status", r.status_code)
ds = r.json()["dataset"]
print("id order:", ds["id"], "size:", ds["size"], "value type:", type(ds["value"]).__name__, "nvals:", len(ds["value"]))
# decode first 2 cells
dims=ds["id"]; sizes=ds["size"]
pos2label={}
for d in dims:
    cat=ds["dimension"][d]["category"]; idx=cat["index"]; lab=cat.get("label",{})
    arr=[None]*len(idx)
    for code,p in idx.items(): arr[p]=lab.get(code,code)
    pos2label[d]=arr
vals=ds["value"]
for i in range(min(3,len(vals))):
    rem=i; rp={}
    for k in range(len(dims)-1,-1,-1):
        rp[dims[k]]=rem%sizes[k]; rem//=sizes[k]
    print({d:pos2label[d][rp[d]] for d in dims}, "value=", vals[i])
