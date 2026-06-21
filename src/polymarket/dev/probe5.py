import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def ks(path="markets", cursor=None):
    params = {"limit": 100}
    if cursor: params["cursor"] = cursor
    return get(f"https://gamma-api.polymarket.com/{path}/keyset", params=params, timeout=(10,60)).json()

# verify cursor param name works and walk a handful of pages
cursor=None; total=0; pages=0; seen=set()
for i in range(6):
    j = ks(cursor=cursor)
    ms = j.get("markets", [])
    if not ms: 
        print("empty page, stop"); break
    total += len(ms); pages+=1
    for m in ms: seen.add(m["id"])
    nc = j.get("next_cursor")
    print(f"page {i}: {len(ms)} markets, next_cursor={'yes' if nc else 'NONE'}")
    if not nc: break
    cursor = nc
print(f"walked {pages} pages, {total} rows, {len(seen)} unique ids")
