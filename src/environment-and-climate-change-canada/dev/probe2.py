import sys; sys.path.insert(0,"src")
import json
from subsets_utils import get
base="https://api.weather.gc.ca"

# 1) deep offset cap?
for off in [9000, 10000, 20000, 50000]:
    r=get(f"{base}/collections/climate-daily/items", params={"limit":10,"offset":off,"f":"json"}, timeout=(10,120))
    body=r.text[:200].replace("\n"," ")
    print(f"offset={off:>6} status={r.status_code} body0={body[:120]}")

# 2) per-station partition: does CLIMATE_IDENTIFIER filter + sortby work? how big is one busy station?
r=get(f"{base}/collections/climate-daily/items", params={"CLIMATE_IDENTIFIER":"6158355","limit":1,"f":"json"}, timeout=(10,120))
print("station 6158355 (Toronto) climate-daily matched:", r.json().get("numberMatched"))

# 3) sortby support
r=get(f"{base}/collections/climate-daily/items", params={"limit":2,"sortby":"LOCAL_DATE","f":"json"}, timeout=(10,120))
print("sortby status:", r.status_code, "n=", r.json().get("numberReturned"))

# 4) queryables for a few families - what's the station property name?
for c in ["climate-daily","hydrometric-daily-mean","ahccd-annual","ltce-temperature","aqhi-observations-realtime","swob-realtime"]:
    r=get(f"{base}/collections/{c}/queryables", params={"f":"json"}, timeout=(10,120))
    props=list(r.json().get("properties",{}).keys())
    # show id-ish props
    idish=[p for p in props if any(k in p.upper() for k in ["ID","STATION","STN","CLIMATE","NUMBER"])]
    print(f"{c}: idish={idish}")
