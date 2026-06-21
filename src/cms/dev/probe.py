import json
from subsets_utils import get

# === MAIN catalog: data-api by UUID ===
uuid = "01edb62e-5c45-4f43-8c91-16cba21cbb74"
print("=== MAIN data-api ===")
url = f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data?size=3&offset=0"
r = get(url, timeout=(10, 60))
print("status", r.status_code)
try:
    data = r.json()
    print("type", type(data), "len" , len(data) if isinstance(data, list) else "n/a")
    if isinstance(data, list) and data:
        print("first row keys:", list(data[0].keys())[:20])
        print("first row:", json.dumps(data[0], indent=2)[:800])
except Exception as e:
    print("json err", e, r.text[:300])

# data.json - find this dataset and its distributions
print("\n=== MAIN data.json (probe one dataset distribution) ===")
r = get("https://data.cms.gov/data.json", timeout=(10, 120))
print("status", r.status_code, "len bytes", len(r.content))
dj = r.json()
ds_list = dj.get("dataset", [])
print("total datasets in data.json:", len(ds_list))
# find by uuid in identifier
for d in ds_list:
    ident = d.get("identifier", "")
    if uuid in ident:
        print("found, identifier:", ident)
        for dist in d.get("distribution", []):
            print("  dist:", dist.get("mediaType"), dist.get("format"), str(dist.get("downloadURL"))[:120], "| accessURL:", str(dist.get("accessURL"))[:100])
        break
