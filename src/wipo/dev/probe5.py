import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}


def g(path, raw=False):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=H, timeout=(10, 120))
    return r


# pmh formcontrols for pct — see all keys
r = g("pmh-search/formcontrols?selectedTab=pct")
print("=== pmh formcontrols pct status", r.status_code)
d = r.json()
print("keys:", list(d.keys()))
for k, v in d.items():
    print(f"  {k}: {json.dumps(v)[:300]}")
