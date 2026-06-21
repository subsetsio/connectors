from subsets_utils import get

BASE = "https://www.smard.de/app/chart_data"

def idx(f, r, res):
    url = f"{BASE}/{f}/{r}/index_{res}.json"
    resp = get(url, timeout=(10, 60))
    if resp.status_code != 200:
        return None
    return resp.json().get("timestamps", [])

# chunk counts at hour vs day for a generation module across regions
for res in ("hour", "day", "week"):
    ts = idx("4068", "DE", res)
    print(f"4068/DE {res}: {len(ts) if ts is not None else 'N/A'} chunks  first={ts[0] if ts else '-'} last={ts[-1] if ts else '-'}")

# which generation regions exist
print("--- generation region availability (4068, hour) ---")
for r in ["DE", "50Hertz", "Amprion", "TenneT", "TransnetBW", "AT", "APG", "DE-LU", "LU", "Creos"]:
    ts = idx("4068", r, "hour")
    print(f"  {r}: {len(ts) if ts is not None else 'NONE'}")

# price modules / region
print("--- price availability hour ---")
for f in ["4169","5078","4170","252","255","4996"]:
    for r in ["DE-LU","DE-AT-LU","AT","DE"]:
        ts = idx(f, r, "hour")
        if ts:
            print(f"  {f}/{r}: {len(ts)}"); break
    else:
        print(f"  {f}: none of tested regions")

# sample one hour chunk to see structure + size
import json
f,r,res = "4068","DE","hour"
ts = idx(f,r,res)
t0 = ts[0]
url = f"{BASE}/{f}/{r}/{f}_{r}_{res}_{t0}.json"
resp = get(url, timeout=(10,60))
data = resp.json()
print("--- sample chunk ---")
print("bytes:", len(resp.content), "series_len:", len(data["series"]), "meta:", data.get("meta_data"))
print("first3:", data["series"][:3])
