import time
from subsets_utils import get

BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

# CSV format for a batch — does it label columns by code?
r = get(f"{BASE}/PN00026MM-PN00001MM-PN00002MM/csv/2024-1/2024-3", timeout=(10, 120))
print("CSV status", r.status_code)
print(r.text[:800])

# valid wide window monthly
for win in ["1990-1/2026-12", "1950-1/2026-12"]:
    r = get(f"{BASE}/PN00001MM/json/{win}", timeout=(10, 120))
    ok = r.headers.get("content-type", "")
    try:
        j = r.json(); n = len(j["periods"]); first = j["periods"][0]["name"]; last=j["periods"][-1]["name"]
        print(f"win {win}: n={n} first={first} last={last}")
    except Exception as e:
        print(f"win {win}: FAILED ({ct(r)})", r.text[:80])

# annual valid window
r = get(f"{BASE}/PM05317AA/json/1950/2026", timeout=(10, 120))
try:
    j = r.json(); print("annual n", len(j["periods"]), j["periods"][:2], j["periods"][-1])
except Exception as e:
    print("annual failed", r.text[:100])

# no-window single (full default?)
r = get(f"{BASE}/PM05317AA/json", timeout=(10, 120))
j = r.json(); print("annual no-window n", len(j["periods"]), "first", j["periods"][0]["name"], "last", j["periods"][-1]["name"])
