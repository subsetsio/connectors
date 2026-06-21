import json
from subsets_utils import get

BASE = "https://api.seaaroundus.org/api/v1"

def gj(url):
    r = get(url, timeout=(10, 120))
    return r.status_code, len(r.content), (r.json() if r.status_code == 200 else r.text[:200])

def feats(j):
    d = j.get("data", {})
    if isinstance(d, dict):
        return d.get("features", [])
    return d if isinstance(d, list) else []

# region counts across region types
for rt in ["eez", "lme", "rfmo", "global", "high-seas", "fishing-entity"]:
    st, n, j = gj(f"{BASE}/{rt}/")
    if isinstance(j, str):
        print(f"{rt:14} HTTP {st} {n}b  -> {j}")
        continue
    fs = feats(j)
    samp = []
    for f in fs[:3]:
        p = f.get("properties", f) if isinstance(f, dict) else f
        if isinstance(p, dict):
            samp.append({k: p.get(k) for k in ("region_id", "title", "region", "id")})
    print(f"{rt:14} HTTP {st} {n}b  n={len(fs)}  sample={samp}")

print("\n--- catch data shape ---")
st, n, j = gj(f"{BASE}/eez/tonnage/taxon/?region_id=76&limit=4")
print("HTTP", st, n, "bytes; top keys:", list(j.keys()))
data = j.get("data", [])
print("n series:", len(data))
for s in data[:3]:
    print("  series keys:", list(s.keys()))
    print("   ", {k: (str(v)[:70]) for k, v in s.items()})
    break
# look at the values array
if data:
    print("values sample:", data[0].get("values", [])[:3])

print("\n--- catch by sector (different dimension) ---")
st, n, j = gj(f"{BASE}/eez/value/sector/?region_id=76&limit=4")
data = j.get("data", [])
print("n:", len(data), "keys:", list(data[0].keys()) if data else None)
if data:
    print("  sample:", {k: str(v)[:60] for k, v in data[0].items()})

print("\n--- global catch by taxon (region_id=1?) ---")
for rid in [1, 0]:
    st, n, j = gj(f"{BASE}/global/tonnage/taxon/?region_id={rid}&limit=2")
    d = j.get("data", []) if isinstance(j, dict) else []
    print(f"  global rid={rid}: HTTP {st} n_series={len(d)}")

print("\n--- error semantics: bad region ---")
st, n, j = gj(f"{BASE}/eez/tonnage/taxon/?region_id=999999&limit=2")
print("  HTTP", st, "n", n, "data:", (j.get("data") if isinstance(j, dict) else j))
