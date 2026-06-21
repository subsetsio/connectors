import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def page(off, lim=100, **extra):
    params = {"limit": lim, "offset": off}; params.update(extra)
    r = get("https://gamma-api.polymarket.com/markets", params=params, timeout=(10,60))
    return r

print("== offset 5000 raw ==")
r = page(5000)
print("status", r.status_code, "| body head:", r.text[:300])

print("\n== with order param ==")
r = page(5000, order="id", ascending="true")
j = r.json()
print("type", type(j).__name__, "len", len(j) if isinstance(j,list) else "-")

print("\n== closed markets count via paginated param? try closed=true ==")
for off in [0, 5000, 20000]:
    r = page(off, order="id", ascending="true")
    j = r.json()
    n = len(j) if isinstance(j, list) else None
    fid = j[0]['id'] if isinstance(j,list) and j else None
    print(f"offset {off}: type={type(j).__name__} n={n} first={fid}")
