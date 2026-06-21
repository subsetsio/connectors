from subsets_utils import get
from urllib.parse import urljoin
import requests

BASE="https://apis.datos.gob.ar"
def chain(path):
    cur=urljoin(BASE,path); hops=[]
    for _ in range(6):
        r=get(cur,follow_redirects=False,timeout=(10,60))
        hops.append((r.status_code,cur))
        if r.status_code in (301,302,303,307,308):
            cur=urljoin(cur,r.headers["location"]); continue
        return cur,r,hops
    return cur,None,hops

for p in [
  "/series/api/dump/series-tiempo-valores-csv.zip",
  "/series/api/dump/sspm/series-tiempo-valores-csv.zip",
  "/series/api/dump/",
]:
    print("==>",p)
    final,r,hops=chain(p)
    for s,u in hops: print("   ",s,u[:110])
    if r is not None: print("    final",r.status_code,r.headers.get("content-type"),len(r.content))
    # try single-slash fix
    if "files//" in final:
        fixed=final.replace("/series/files//","/series/files/")
        rr=requests.get(fixed,timeout=120)
        print("    single-slash:",rr.status_code,len(rr.content))
