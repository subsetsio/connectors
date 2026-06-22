import sys; sys.path.insert(0,"src")
import time
from subsets_utils import get
base="https://api.weather.gc.ca"
for off in [0, 300000, 590000]:
    s=time.time(); r=get(f"{base}/collections/climate-normals/items", params={"limit":10000,"offset":off,"f":"json"}, timeout=(15,300))
    print(f"climate-normals offset={off:>7} -> {time.time()-s:5.1f}s n={r.json().get('numberReturned')}")
