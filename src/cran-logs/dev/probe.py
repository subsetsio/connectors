import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json

# 1) Batch multiple packages in one cranlogs request
pkgs = ["ggplot2","dplyr","data.table","Rcpp","jsonlite"]
url = f"https://cranlogs.r-pkg.org/downloads/daily/2024-01-01:2024-01-03/{','.join(pkgs)}"
r = get(url, timeout=(10,120))
d = r.json()
print("BATCH: status", r.status_code, "n_objs", len(d))
for o in d:
    print("  pkg", o.get("package"), "ndays", len(o.get("downloads") or []), "sample", (o.get("downloads") or [None])[0])

# 2) A package with zero/nonexistent
r2 = get("https://cranlogs.r-pkg.org/downloads/daily/2024-01-01:2024-01-03/thispkgdoesnotexist123", timeout=(10,120))
print("NONEXIST:", r2.status_code, r2.text[:300])

# 3) crandb bulk desc endpoint sizes
for ep in ["https://crandb.r-pkg.org/-/desc?limit=2", "https://crandb.r-pkg.org/-/latest?limit=2"]:
    try:
        rr = get(ep, timeout=(10,120))
        print("CRANDB", ep, rr.status_code, rr.text[:300])
    except Exception as e:
        print("CRANDB", ep, "ERR", e)
