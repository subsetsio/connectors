import sys; sys.path.insert(0,"src")
from nodes.reserve_bank_of_australia import MULTI_FILE, fetch_one
# Just verify partition labels are clean strings (no fetch) for j1
for ent in ("j1-forecasts","b12.1.1"):
    print(ent, "->", sorted(set(MULTI_FILE[ent].values())))
# sanity: every j1 member maps to a clean variable label
assert all(v and "/" not in v for v in MULTI_FILE["j1-forecasts"].values())
print("labels OK")
