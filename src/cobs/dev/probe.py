import json
from subsets_utils import get

# Comet list
r = get("https://cobs.si/api/comet_list.api", params={"format": "json"}, timeout=(10, 120))
d = r.json()
print("=== comet_list info ===", d.get("info"))
print("=== comet_list sample ===")
print(json.dumps(d["objects"][0], indent=2))

# Observations for one comet (id=143 Hale-Bopp)
r2 = get("https://cobs.si/api/obs_list.api", params={"format": "json", "id": 143, "page": 1}, timeout=(10, 120))
d2 = r2.json()
print("=== obs info ===", d2.get("info"))
print("=== obs sample row ===")
print(json.dumps(d2["objects"][0], indent=2))
print("=== obs keys ===", sorted(d2["objects"][0].keys()))

# A comet with possibly few/zero obs - check id=1
r3 = get("https://cobs.si/api/obs_list.api", params={"format": "json", "id": 1, "page": 1}, timeout=(10, 120))
print("=== id=1 obs status/info ===", r3.status_code, r3.json().get("info"))

# Check whether comet id appears in obs row's comet dict
print("=== obs comet dict ===", json.dumps(d2["objects"][0].get("comet"), indent=2))
