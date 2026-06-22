import json
from subsets_utils import get

r = get("https://www.aurorasaurus.org/web-obs/list", params={"page": 1, "page_size": 3}, timeout=(10, 120))
d = r.json()
print("count:", d["count"])
print("next:", d["next"])
print("n results:", len(d["results"]))
rec = d["results"][0]
print("\n--- one record (pretty) ---")
print(json.dumps(rec, indent=2, default=str))
print("\n--- field types across 3 records ---")
keys = set()
for rr in d["results"]:
    keys |= set(rr.keys())
for k in sorted(keys):
    vals = [type(rr.get(k)).__name__ for rr in d["results"]]
    print(f"  {k}: {vals}  e.g. {repr(d['results'][0].get(k))[:80]}")
