import time
from subsets_utils import get

BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

# Does response order follow request order? Request in two different orders.
for codes in ["PN00026MM-PN00001MM-PN00002MM", "PN00002MM-PN00026MM-PN00001MM"]:
    r = get(f"{BASE}/{codes}/json/2024-1/2024-3", timeout=(10, 120))
    j = r.json()
    print("REQ", codes)
    for s in j["config"]["series"]:
        print("   ", s["name"][:70])

# Full history with explicit start
t0 = time.time()
r = get(f"{BASE}/PN00001MM/json/1900-1/2030-12", timeout=(10, 120))
j = r.json()
print("\nfull-history monthly n periods", len(j["periods"]), "first", j["periods"][0]["name"], "last", j["periods"][-1]["name"], "elapsed", round(time.time()-t0,2))

# annual series format
r = get(f"{BASE}/PM05317AA/json/1900/2030", timeout=(10, 120))
j = r.json()
print("annual config", j["config"]["series"][:1])
print("annual periods sample", j["periods"][:2], "...", j["periods"][-1] if j["periods"] else None, "n", len(j["periods"]))
