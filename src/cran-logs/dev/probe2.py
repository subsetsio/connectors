import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json, time

# crandb full desc catalog (all packages, key->{version,title})
r = get("https://crandb.r-pkg.org/-/desc", timeout=(15,180))
desc = r.json()
names = list(desc.keys())
print("CRANDB desc total packages:", len(names))
print("sample names:", names[:3], "...", names[-3:])
print("sample val:", desc[names[0]])

# Big batch: 100 packages, full range
batch = names[:100]
t=time.time()
url = "https://cranlogs.r-pkg.org/downloads/daily/2012-10-01:2026-06-20/" + ",".join(batch)
r2 = get(url, timeout=(15,300))
print("BATCH100 full-range:", r2.status_code, "len(url)=", len(url), "secs=%.1f"%(time.time()-t))
d = r2.json()
print("  n_objs", len(d))
# count total day-records
tot = sum(len(o.get("downloads") or []) for o in d)
print("  total day-records:", tot, " bytes:", len(r2.content))
# find earliest day across
days = [dl["day"] for o in d for dl in (o.get("downloads") or [])]
if days: print("  min day", min(days), "max day", max(days))
