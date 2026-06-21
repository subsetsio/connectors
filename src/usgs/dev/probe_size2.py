import time
from subsets_utils import get
BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"
def crawl(coll, cap=150):
    url=f"{BASE}/collections/{coll}/items"; params={"f":"json","limit":10000}
    total=0; pages=0; t=time.time()
    while True:
        r=get(url,params=params,timeout=(10,180)); j=r.json()
        n=j.get("numberReturned",0); total+=n; pages+=1
        nxt=[l["href"] for l in j.get("links",[]) if l.get("rel")=="next"]
        if not nxt or n==0: 
            return total,pages,round(time.time()-t,1),"TERMINATED"
        if pages>=cap:
            return total,pages,round(time.time()-t,1),"CAPPED(more exists)"
        url=nxt[0]; params=None
for c in ["peaks","monitoring-locations","time-series-metadata","channel-measurements","combined-metadata","field-measurements"]:
    print(c, crawl(c))
