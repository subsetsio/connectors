import json
from subsets_utils import get

BASE = "https://api.ojp.gov/bjsdataset/v1/"

def probe(rid, ext="json", params=None):
    url = f"{BASE}{rid}.{ext}"
    r = get(url, params=params or {}, timeout=(10.0, 120.0))
    print("URL", r.url)
    print("status", r.status_code, "ctype", r.headers.get("content-type"))
    return r

# count(*) on a NIBRS aggregate and NCVS microdata
for rid in ["r32q-bdaw", "gcuy-rt5g"]:
    r = probe(rid, "json", {"$select": "count(*)"})
    print("count:", r.text[:200])
    print("---")

# shape of NIBRS aggregate
r = probe("r32q-bdaw", "json", {"$limit": 2})
rows = r.json()
print("NIBRS r32q-bdaw first row keys:", sorted(rows[0].keys()))
print("NIBRS sample row:", json.dumps(rows[0], indent=2)[:1500])
print("types:", {k: type(v).__name__ for k, v in rows[0].items()})
print("=====")

# shape of NCVS microdata
r = probe("gcuy-rt5g", "json", {"$limit": 2})
rows = r.json()
print("NCVS gcuy-rt5g first row keys:", sorted(rows[0].keys()))
print("NCVS sample row:", json.dumps(rows[0], indent=2)[:1500])
print("types:", {k: type(v).__name__ for k, v in rows[0].items()})
