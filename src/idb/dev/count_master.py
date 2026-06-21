import sys, httpx
sys.path.insert(0,'src')
from subsets_utils import get, get_client
BASE="https://data.iadb.org/api/3/action"
rec=get(f"{BASE}/package_show",params={"id":"social-indicators-of-latin-america-and-the-caribbean"},timeout=60).json()["result"]
master=max((r for r in rec["resources"] if r.get("datastore_active")), key=lambda r: get(f"{BASE}/datastore_search",params={"resource_id":r["id"],"limit":0},timeout=60).json()["result"].get("total") or 0)
rid=master["id"]
ds=get(f"{BASE}/datastore_search",params={"resource_id":rid,"limit":0},timeout=60).json()["result"]
print("master rid:", rid, "datastore total:", ds.get("total"), flush=True)
# stream-count the dump lines
url=f"https://data.iadb.org/datastore/dump/{rid}"
n=0
with get_client().stream("GET", url, timeout=httpx.Timeout(30.0, read=900.0)) as resp:
    print("dump status", resp.status_code, "clen", resp.headers.get("content-length"), flush=True)
    for _ in resp.iter_lines():
        n+=1
        if n % 2000000==0: print("  lines so far", n, flush=True)
print("TOTAL dump lines (incl header):", n, flush=True)
