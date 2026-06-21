import time
from subsets_utils import get
BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

def count_window(coll, dt, max_pages=400):
    url = f"{BASE}/collections/{coll}/items"
    params = {"f":"json","limit":10000,"datetime":dt}
    total=0; pages=0; t=time.time()
    while True:
        r=get(url, params=params, timeout=(10,180)); j=r.json()
        n=j.get("numberReturned",0); total+=n; pages+=1
        nxt=[l["href"] for l in j.get("links",[]) if l.get("rel")=="next"]
        if not nxt or n==0 or pages>=max_pages: break
        url=nxt[0]; params=None
    return total, pages, time.time()-t

# daily for one recent day
print("daily 1 day:", count_window("daily","2025-06-10T00:00:00Z/2025-06-11T00:00:00Z"))
# continuous for one recent hour
print("continuous 1 hour:", count_window("continuous","2025-06-10T00:00:00Z/2025-06-10T01:00:00Z"))
