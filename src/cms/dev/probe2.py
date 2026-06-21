import json
from subsets_utils import get

uuid = "01edb62e-5c45-4f43-8c91-16cba21cbb74"

# pagination / stats for main data-api
print("=== MAIN stats endpoint ===")
for path in [f"/data-api/v1/dataset/{uuid}/data/stats", f"/data-api/v1/dataset/{uuid}/data?size=1&offset=0&count=true"]:
    r = get("https://data.cms.gov"+path, timeout=(10,60))
    print(path, "->", r.status_code, r.text[:200])

# big size test
print("\n=== MAIN large size ===")
r = get(f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data?size=10000&offset=0", timeout=(10,120))
d = r.json()
print("requested 10000, got", len(d) if isinstance(d,list) else d)
r = get(f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data?size=5000&offset=0", timeout=(10,120))
d = r.json()
print("requested 5000, got", len(d) if isinstance(d,list) else type(d))

# === PROVIDER catalog ===
print("\n=== PROVIDER metastore item ===")
pid = "0127-af37"
r = get(f"https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/{pid}?show-reference-ids", timeout=(10,60))
print("status", r.status_code)
try:
    item = r.json()
    print("keys:", list(item.keys()))
    for dist in item.get("distribution", []):
        dd = dist.get("data", dist)
        print("  dist downloadURL:", str(dd.get("downloadURL"))[:120], "| identifier:", dist.get("identifier"))
except Exception as e:
    print("err", e, r.text[:300])

# provider datastore query
print("\n=== PROVIDER datastore SQL/query by dataset id ===")
for path in [f"/provider-data/api/1/datastore/query/{pid}/0?limit=3", f"/provider-data/api/1/datastore/query/{pid}?limit=3"]:
    r = get("https://data.cms.gov"+path, timeout=(10,60))
    print(path, "->", r.status_code)
    if r.status_code==200:
        d=r.json()
        print("  keys:", list(d.keys()) if isinstance(d,dict) else type(d))
        print("  count:", d.get("count") if isinstance(d,dict) else None)
        results = d.get("results") if isinstance(d,dict) else None
        if results: print("  first row:", json.dumps(results[0],indent=2)[:500])
    else:
        print("  ", r.text[:200])
