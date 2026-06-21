import time, json
from subsets_utils import get
BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

# max limit test + throughput + payload size for a big page
for coll in ["monitoring-locations","peaks","daily"]:
    t=time.time()
    r = get(f"{BASE}/collections/{coll}/items", params={"f":"json","limit":10000}, timeout=(10,300))
    dt=time.time()-t
    j=r.json()
    nr=j.get("numberReturned")
    sz=len(r.content)
    print(f"{coll:22s} limit10000 -> returned={nr} bytes={sz/1e6:.1f}MB time={dt:.1f}s")

# try resultType=hits for count
for coll in ["peaks","monitoring-locations"]:
    for p in [{"f":"json","limit":1,"resultType":"hits"},{"f":"json","limit":1,"count":"true"}]:
        try:
            r=get(f"{BASE}/collections/{coll}/items",params=p,timeout=(10,120))
            j=r.json()
            print(coll,p,"-> numberMatched",j.get("numberMatched"),"returned",j.get("numberReturned"))
        except Exception as e:
            print(coll,p,"ERR",e)
