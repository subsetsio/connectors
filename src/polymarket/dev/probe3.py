import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def ks(**params):
    r = get("https://gamma-api.polymarket.com/markets/keyset", params=params, timeout=(10,60))
    return r

print("== keyset no params ==")
r = ks(limit=3)
print("status", r.status_code)
print(r.text[:600])
