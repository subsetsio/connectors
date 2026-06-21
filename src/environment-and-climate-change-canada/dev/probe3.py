import sys; sys.path.insert(0,"src")
from subsets_utils import get
base="https://api.weather.gc.ca"
# limit cap honored?
for lim in [10000, 50000]:
    r=get(f"{base}/collections/climate-monthly/items", params={"limit":lim,"f":"json"}, timeout=(15,180))
    d=r.json()
    print(f"requested limit={lim} -> numberReturned={d.get('numberReturned')} status={r.status_code}")
# inspect a feature shape (flat properties + geometry)
r=get(f"{base}/collections/climate-monthly/items", params={"limit":1,"f":"json"}, timeout=(15,120))
f=r.json()["features"][0]
print("keys:", list(f.keys()))
print("geometry:", f.get("geometry"))
import json
print("properties sample:", json.dumps(dict(list(f["properties"].items())[:8]), default=str))
