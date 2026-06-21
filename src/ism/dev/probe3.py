import json, re
from subsets_utils import get

def slug(name):
    s = name.strip().lower().replace("%","pct").replace("&","and")
    s = re.sub(r"[^a-z0-9]+","_",s).strip("_")
    return s or "value"

codes = json.loads(get("https://api.db.nomics.world/v22/datasets/ISM", timeout=(10,120)).text)["datasets"]["docs"]
allnames=set()
for d in sorted(c["code"] for c in codes):
    r = get(f"https://api.db.nomics.world/v22/series/ISM/{d}?observations=0&limit=1000", timeout=(10,120))
    docs = r.json()["series"]["docs"]
    pairs = [(s.get("series_code"), s.get("series_name")) for s in docs]
    slugs = [slug(n) for _,n in pairs]
    dup = len(slugs)!=len(set(slugs))
    print(f"{d:18s} n={len(pairs):2d} dup={dup} -> {[ (c,n,slug(n)) for c,n in pairs]}")
    allnames.update(n for _,n in pairs)
print("\nALL DISTINCT NAMES:", sorted(allnames))
