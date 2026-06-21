import json
from subsets_utils import get

base = "https://data.cms.gov/provider-data/api/1/datastore/query"

# limit cap test
print("=== PROVIDER limit cap ===")
for lim in [500, 1000, 5000]:
    r = get(f"{base}/0127-af37/0?limit={lim}&offset=0", timeout=(10,90))
    d = r.json()
    print(f"limit={lim} -> got {len(d.get('results',[]))}, count={d.get('count')}")

# offset test
r = get(f"{base}/0127-af37/0?limit=2&offset=5", timeout=(10,60))
print("offset=5 first row zip:", r.json()["results"][0].get("zip_code"))

# named provider ids
print("\n=== PROVIDER named ids ===")
for pid in ["footnotes", "clinical_depression", "covid-19_hcp", "complete_qip_data", "hbf-map", "shr", "vat_topic"]:
    r = get(f"{base}/{pid}/0?limit=1", timeout=(10,60))
    if r.status_code == 200:
        d = r.json()
        cols = list(d["results"][0].keys()) if d.get("results") else []
        print(f"  {pid}: OK count={d.get('count')} cols={cols[:5]}")
    else:
        print(f"  {pid}: {r.status_code} {r.text[:120]}")
