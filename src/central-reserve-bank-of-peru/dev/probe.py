import time
from subsets_utils import get

BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

# 1) probe a batch of 10 monthly codes, json, english
codes = "PN00001MM-PN00002MM-PN00026MM"
t0 = time.time()
r = get(f"{BASE}/{codes}/json", timeout=(10, 120))
print("status", r.status_code, "elapsed", round(time.time() - t0, 2))
j = r.json()
print("top keys", list(j.keys()))
print("config keys", list(j["config"].keys()))
print("config.series sample", j["config"]["series"][:3])
print("n periods", len(j["periods"]))
print("period sample", j["periods"][:2])
print("period last", j["periods"][-1])

# 2) probe a daily series
t0 = time.time()
r2 = get(f"{BASE}/PD04637PD/json", timeout=(10, 120))
print("\ndaily status", r2.status_code, "elapsed", round(time.time() - t0, 2))
j2 = r2.json()
print("daily config.series", j2["config"]["series"][:2])
print("daily n periods", len(j2["periods"]))
print("daily period sample", j2["periods"][:2])

# 3) what does a bad code return?
r3 = get(f"{BASE}/ZZZBADCODE/json", timeout=(10, 120))
print("\nbad code status", r3.status_code)
print("bad code body[:300]", r3.text[:300])
