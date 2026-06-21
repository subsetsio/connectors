import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, time
from subsets_utils import get, post

BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"

# 1) metadata for a small national table and a big one
for path in ["2I/0082I5DFCF2.px", "2M/PI/CPI/2012/0012M4ACPI1.px"]:
    r = get(BASE + path, timeout=(10,60))
    meta = r.json()
    title = meta.get("title")
    vars_ = meta.get("variables", [])
    cells = 1
    dims = []
    for v in vars_:
        nv = len(v["values"])
        cells *= nv
        dims.append((v["code"], nv, v.get("time", False)))
    print(f"\n=== {path}")
    print("title:", title[:90])
    print("dims:", dims, "total_cells:", cells)

# 2) Try a small POST query (json-stat2) to see data shape — select first value of each dim
path = "2I/0082I5DFCF2.px"
meta = get(BASE+path, timeout=(10,60)).json()
sel = []
for v in meta["variables"]:
    vals = v["values"][:2] if not v.get("time") else v["values"][-2:]
    sel.append({"code": v["code"], "selection": {"filter":"item","values":vals}})
query = {"query": sel, "response": {"format": "json-stat2"}}
r = post(BASE+path, json=query, timeout=(10,120))
print("\nPOST status:", r.status_code, "len:", len(r.content))
js = r.json()
print("json-stat2 keys:", list(js.keys()))
print("dimension order (id):", js.get("id"))
print("size:", js.get("size"))
print("value sample:", js.get("value")[:8])
# show one dimension's category structure
dim0 = js["id"][0]
print("dim0 category:", json.dumps(js["dimension"][dim0]["category"])[:300])
