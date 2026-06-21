import json, sys, collections
sys.path.insert(0, 'src')
from subsets_utils import get

BASE = "https://data.iadb.org/api/3/action"
union = json.load(open('/Users/nathansnellaert/Documents/hardened/data/sources/idb/work/entity_union.json'))
ids = union if isinstance(union, list) else list(union.keys())
print("n accepted:", len(ids))

TAB = {"CSV","XLSX","XLS","TSV","TXT"}
def show(pid):
    r = get(f"{BASE}/package_show", params={"id": pid}, timeout=60)
    return r.json()["result"]

notab=[]; mega=[]
for pid in ids:
    rec = show(pid)
    res = rec.get("resources",[]) or []
    fmts = [ (rr.get("format") or "").upper() for rr in res ]
    tab = [f for f in fmts if f in TAB]
    if not tab: notab.append((pid, fmts))
    if len(res) >= 50: mega.append((pid, len(res), dict(collections.Counter(fmts))))
print("\n--- accepted with NO tabular resource:", len(notab))
for p,f in notab: print("  ",p, f)
print("\n--- mega (>=50 resources):")
for p,n,c in mega: print("  ",p, n, c)
