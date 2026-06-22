import io, time, httpx, json, pandas as pd
from subsets_utils import get, configure_http
configure_http(headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36","Connection":"close"})
BASE="https://data.gov.au/data/api/3/action"
res=json.loads(get(f"{BASE}/package_show?id=pb_agcomd9abcc20141209_11a",timeout=(15,60)).content)["result"]["resources"]
urls=[x["url"] for x in res if (x.get("format") or "").lower().startswith("microsoft")]
print("downloading",len(urls),"files with Connection:close")
ok=resets=0
t=time.time()
for u in urls*2:  # 2 passes to stress
    try:
        c=get(u,timeout=(15,120)).content; ok+=1
    except httpx.ReadError: resets+=1
print(f"ok={ok} resets={resets} elapsed={time.time()-t:.1f}s")
