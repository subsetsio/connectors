import json
from subsets_utils import get
BASE = "https://api.datahub.itu.int/v2"
cats = get(f"{BASE}/dictionaries/getcategories", timeout=(10,60)).json()
# collect all codeIDs + their category/subcat
codeids=[]
for c in cats:
    for sc in c["subCategory"]:
        for it in sc["items"]:
            codeids.append(it["codeID"])
print("total catalogue codeIDs:", len(codeids))
print("getcategories item keys:", sorted(cats[0]["subCategory"][0]["items"][0].keys()))
# getbyids for first 5
ids=",".join(str(x) for x in codeids[:5])
m = get(f"{BASE}/dictionaries/getbyids", params={"codeids":ids}, timeout=(10,60)).json()
print("getbyids top-level len:", len(m), "outer keys:", sorted(m[0].keys()))
code0 = m[0]["codes"][0]
print("code record keys:", sorted(code0.keys()))
print("code sample:", json.dumps({k:code0[k] for k in list(code0)[:14]}, default=str)[:500])
