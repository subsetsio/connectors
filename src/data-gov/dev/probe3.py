import time
from subsets_utils import get
BASE = "https://catalog-old.data.gov/api/3"
def page(start, rows=1000, sort="metadata_created asc"):
    t=time.time()
    r = get(f"{BASE}/action/package_search", params={"rows":rows,"start":start,"sort":sort}, timeout=(10.0,180.0))
    r.raise_for_status()
    d=r.json()["result"]
    dt=time.time()-t
    payload=len(r.content)
    return dt, len(d["results"]), payload, d["count"]

for start in (0, 200000, 400000):
    dt,n,sz,cnt = page(start)
    print(f"start={start}: {dt:.1f}s rows={n} payload={sz/1e6:.1f}MB count={cnt}")
