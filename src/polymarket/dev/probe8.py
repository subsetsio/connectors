import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def ks(path, cursor=None, limit=100):
    p={"limit":limit}
    if cursor: p["after_cursor"]=cursor
    return get(f"https://gamma-api.polymarket.com/{path}/keyset", params=p, timeout=(10,90)).json()

for path in ["markets","events"]:
    cursor=None; total=0; pages=0; seen=set(); t0=time.time()
    while True:
        j=ks(path, cursor)
        rows=j.get(path,[])
        if not rows: break
        total+=len(rows); pages+=1
        for r in rows: seen.add(r["id"])
        cursor=j.get("next_cursor")
        if not cursor: break
        if pages>=15: break  # cap probe
    print(f"{path}: {pages} pages, {total} rows, {len(seen)} unique, {time.time()-t0:.1f}s (probe capped at 15 pages)")
