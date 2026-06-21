from subsets_utils import get
import json

# 1. How does deep pagination behave on a broad single query? Distinct names?
seen = set()
dups = 0
for frm in (0, 1000, 5000, 9000, 9750):
    r = get("https://registry.npmjs.org/-/v1/search",
            params={"text":"a","size":250,"from":frm,"popularity":1.0,"quality":0.0,"maintenance":0.0},
            timeout=(10,120))
    objs = r.json().get("objects", [])
    names = [o["package"]["name"] for o in objs]
    new = sum(1 for n in names if n not in seen)
    dups += len(names) - new
    seen.update(names)
    print(f"from={frm}: returned {len(names)}, new={new}, first={names[0] if names else None}")
print(f"total distinct so far={len(seen)}, dups={dups}")

# 2. Beyond 10000?
r = get("https://registry.npmjs.org/-/v1/search",
        params={"text":"a","size":20,"from":10001,"popularity":1.0},timeout=(10,120))
print("from=10001 status", r.status_code, "objects", len(r.json().get("objects",[])))
