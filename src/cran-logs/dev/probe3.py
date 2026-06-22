import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json, time
t=time.time()
r = get("https://crandb.r-pkg.org/-/latest", timeout=(15,300))
print("status", r.status_code, "bytes", len(r.content), "secs %.1f"%(time.time()-t))
d = r.json()
print("n packages", len(d))
k=list(d.keys())[0]
print("keys for", k, sorted(d[k].keys()))
print("sample license/published:", d[k].get("License"), d[k].get("Date/Publication") or d[k].get("Published"))
