import json
from subsets_utils import get

BASE = "https://api.uktradeinfo.com"

# 1. Row counts per entity (OData /$count returns a plain integer)
for ent in ["OTS", "RTS", "Trade", "YearlyTrade", "Import", "Export", "Commodity"]:
    try:
        r = get(f"{BASE}/{ent}/$count", timeout=(10, 120))
        print(f"COUNT {ent}: {r.status_code} -> {r.text[:60]}")
    except Exception as e:
        print(f"COUNT {ent}: ERROR {type(e).__name__}: {e}")

# 2. Sample one row of each fact/dim to see field shape & types
for ent in ["OTS", "RTS", "Commodity", "YearlyTrade"]:
    r = get(f"{BASE}/{ent}", params={"$top": 1}, timeout=(10, 120))
    data = r.json()
    rows = data.get("value", [])
    print(f"\nSAMPLE {ent}: keys=", list(data.keys()))
    if rows:
        print(json.dumps(rows[0], indent=2)[:1200])

# 3. Check nextLink presence on a 40k+ entity
r = get(f"{BASE}/OTS", params={"$top": 5}, timeout=(10, 120))
d = r.json()
print("\nOTS nextLink present:", "@odata.nextLink" in d)
print("OTS context:", d.get("@odata.context"))
