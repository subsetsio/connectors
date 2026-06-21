import json
from subsets_utils import get

BASE = "https://api.uis.unesco.org/api/public"

# indicators catalog
inds = get(f"{BASE}/definitions/indicators", timeout=(10, 120)).json()
print("indicators type:", type(inds), "len:", len(inds))
print("sample indicator:", json.dumps(inds[0], indent=2)[:600])
# max totalRecordCount -> cap risk
counts = [(i.get("indicatorCode"), i.get("dataAvailability", {}).get("totalRecordCount", 0)) for i in inds]
counts.sort(key=lambda x: -x[1])
print("top-5 by record count:", counts[:5])
print("how many indicators with >100k records:", sum(1 for _, c in counts if c > 100000))
print("how many > 90k:", sum(1 for _, c in counts if c > 90000))

# geounits
geo = get(f"{BASE}/definitions/geounits", timeout=(10, 120)).json()
print("\ngeounits type:", type(geo), "len:", len(geo))
print("sample geo:", json.dumps(geo[:3], indent=2))
print("geo keys union:", sorted({k for g in geo for k in g}))

# one indicator's data
code = inds[0]["indicatorCode"]
d = get(f"{BASE}/data/indicators", params={"indicator": code}, timeout=(10, 120)).json()
print("\ndata top-level keys:", list(d.keys()))
print("hints:", d.get("hints"))
print("n records:", len(d.get("records", [])))
print("sample record:", json.dumps(d["records"][0], indent=2) if d.get("records") else "none")
print("record keys union (first 2000):", sorted({k for r in d["records"][:2000] for k in r}))
# value types
vals = [r["value"] for r in d["records"][:5000]]
print("value types seen:", sorted({type(v).__name__ for v in vals}))
print("magnitude vals:", sorted({r.get("magnitude") for r in d["records"][:5000]})[:10])
print("qualifier vals:", sorted({str(r.get("qualifier")) for r in d["records"][:5000]})[:10])
