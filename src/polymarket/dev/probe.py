import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json
from subsets_utils import get

# How does pagination behave? Find total reachable markets.
def page(off, lim=100, **extra):
    params = {"limit": lim, "offset": off}
    params.update(extra)
    r = get("https://gamma-api.polymarket.com/markets", params=params, timeout=(10,60))
    return r.json()

print("== default order, walk offsets ==")
for off in [0, 1000, 5000, 10000, 20000, 30000, 35000, 38000, 39000, 39500]:
    p = page(off)
    ids = [m['id'] for m in p[:2]]
    print(f"offset {off:>6}: returned {len(p):>3}  first_ids={ids}")
