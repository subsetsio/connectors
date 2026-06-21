import json
from subsets_utils import get

BASE = "https://catalog-old.data.gov/api/3"

def j(path, **params):
    r = get(f"{BASE}/{path}", params=params, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()

# 1) max rows for package_search
for rows in (1000, 2000):
    d = j("action/package_search", rows=rows, start=0)
    res = d["result"]
    print(f"rows={rows} -> returned={len(res['results'])} count={res['count']}")

# 2) sample package: which fields, resource shape
d = j("action/package_search", rows=1, start=0)
pkg = d["result"]["results"][0]
print("\nPACKAGE top keys:", sorted(pkg.keys()))
print("org field:", type(pkg.get("organization")), (pkg.get("organization") or {}).get("name") if isinstance(pkg.get("organization"),dict) else pkg.get("organization"))
print("groups field sample:", pkg.get("groups"))
print("tags sample:", (pkg.get("tags") or [{}])[0])
res = pkg.get("resources") or []
print("num resources:", len(res))
if res:
    print("RESOURCE keys:", sorted(res[0].keys()))
    print("resource sample:", {k: res[0].get(k) for k in ("id","format","mimetype","name","size","created","last_modified","package_id")})

# 3) organization pagination
d = j("action/organization_list", all_fields="true", limit=200, offset=0)
print("\norg all_fields limit=200 ->", len(d["result"]))
