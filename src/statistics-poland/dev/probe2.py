from subsets_utils import get

BASE = "https://bdl.stat.gov.pl/api/v1"
POLAND = "000000000000"

def g(path, **params):
    params.setdefault("format", "json")
    params.setdefault("lang", "en")
    r = get(f"{BASE}/{path}", params=params, timeout=(10, 120))
    return r.status_code, (r.json() if r.headers.get("content-type","").startswith("application/json") else r.text)

# by-unit batching multiple var-id for national unit
sc, d = g(f"data/by-unit/{POLAND}", **{"var-id": [60559, 458238, 458603], "page-size": 100})
print("by-unit multi var-id status:", sc)
if isinstance(d, dict):
    print("  keys:", list(d.keys()), "| totalRecords:", d.get("totalRecords"))
    for r in d.get("results", [])[:3]:
        print("   var", r.get("id"), "| #values:", len(r.get("values", [])), "| sample:", r.get("values", [])[:1])
else:
    print("  ", str(d)[:300])

# how many var-ids can we batch? try 60
many = list(range(60559, 60559+60))
sc, d = g(f"data/by-unit/{POLAND}", **{"var-id": many, "page-size": 100})
print("\nby-unit 60 var-ids status:", sc, "| returned:", (d.get("totalRecords") if isinstance(d, dict) else str(d)[:200]))

# does GDP-per-capita (regional accounts) have a national value?
sc, d = g("data/by-variable/458421", **{"unit-level": 0, "page-size": 10})
print("\nGDP per capita var 458421 unit-level=0 status:", sc, "| units:", d.get("totalRecords") if isinstance(d,dict) else d)
if isinstance(d, dict) and d.get("results"):
    print("  ", d["results"][0]["name"], d["results"][0]["values"][:2])
