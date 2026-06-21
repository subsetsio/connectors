import json
from subsets_utils import get

BASE = "https://api.seaaroundus.org/api/v1"

def gj(url):
    r = get(url, timeout=(10, 120))
    return r.status_code, len(r.content), (r.json() if "json" in r.headers.get("content-type","") or r.status_code==200 else r.text[:150])

# every dimension on eez/tonnage to confirm path names work
for dim in ["taxon","commercialgroup","functionalgroup","country","sector","catchtype","reporting-status"]:
    st, n, j = gj(f"{BASE}/eez/tonnage/{dim}/?region_id=76")
    d = j.get("data", []) if isinstance(j, dict) else j
    keys = list(d[0].keys()) if isinstance(d, list) and d else None
    sample_key = d[0].get("key") if isinstance(d, list) and d else None
    print(f"eez/tonnage/{dim:18} HTTP {st} n_series={len(d) if isinstance(d,list) else '?'} keys={keys} firstkey={sample_key!r}")

print("\n--- global region: does it need region_id? what id? ---")
for url in [f"{BASE}/global/tonnage/taxon/", f"{BASE}/global/tonnage/taxon/?region_id=1",
            f"{BASE}/global/tonnage/country/?region_id=1"]:
    st, n, j = gj(url)
    d = j.get("data", []) if isinstance(j, dict) else j
    print(f"  {url} -> HTTP {st} n={len(d) if isinstance(d,list) else j}")

print("\n--- taxa endpoint shape ---")
st, n, j = gj(f"{BASE}/taxa/")
print("HTTP", st, n, "bytes; type", type(j).__name__)
if isinstance(j, dict):
    print("keys:", list(j.keys()))
    d = j.get("data", [])
else:
    d = j
print("n taxa:", len(d) if isinstance(d, list) else "?")
if isinstance(d, list) and d:
    print("taxon[0]:", d[0])

print("\n--- fishing-entity catch (decide include or not) ---")
st, n, j = gj(f"{BASE}/fishing-entity/tonnage/taxon/?region_id=200")
d = j.get("data", []) if isinstance(j, dict) else j
print("  fishing-entity/tonnage/taxon region_id=200 -> HTTP", st, "n=", len(d) if isinstance(d,list) else j)

print("\n--- value measure on a dim with no breakdown metadata ---")
st, n, j = gj(f"{BASE}/lme/value/sector/?region_id=1")
d = j.get("data", []) if isinstance(j, dict) else j
print("  lme/value/sector region_id=1 -> n=", len(d), "first:", {k:str(v)[:40] for k,v in d[0].items()} if d else None)
