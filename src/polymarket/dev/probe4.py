import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def ks(path="markets", **params):
    return get(f"https://gamma-api.polymarket.com/{path}/keyset", params=params, timeout=(10,60))

r = ks(limit=3)
j = r.json()
print("top-level keys:", list(j.keys()))
print("markets count:", len(j.get("markets", [])))
for k in j:
    if k != "markets":
        print(f"  {k} = {j[k]}")
# try larger limit
r = ks(limit=500)
print("\nlimit=500 ->", len(r.json().get("markets", [])))
# pagination: look for next_cursor field
print("\nfull non-markets payload:", {k:v for k,v in j.items() if k!='markets'})
# events keyset?
print("\n== events keyset ==")
r = get("https://gamma-api.polymarket.com/events/keyset", params={"limit":2}, timeout=(10,60))
print("status", r.status_code, "keys", list(r.json().keys()) if r.status_code==200 else r.text[:200])
