import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import re, json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}

# 1. Live: loadOffOrgClassList for pmh pct indicator 1001
for path in ["pmh-search/loadOffOrgClassList?indicator=1001",
             "ips-search/loadOffOrgTechList?indicator=10&rpType=11"]:
    r = get(f"{API}/{path}&lang=en", headers=H, timeout=(10, 120))
    print(f"=== {path} [{r.status_code}]")
    txt = r.text
    print(txt[:700])
    print()

# 2. Find param-name enum c.B and the request-object construction in JS
t = get('https://www3.wipo.int/ipstats/main.649b62b91ba3b94e.js', timeout=(10, 120)).text
t2 = get('https://www3.wipo.int/ipstats/184.4739a4f1ffa3d285.js', timeout=(10, 120)).text

# the enum mapping param keys; search for a cluster of "xxx:" with these names
for kw in ["offSelValues", "oriSelValues", "classSelValues", "OffSelValues", "selectedTab", "reportType", "fromYear", "indicator"]:
    for name, txt in [("main", t), ("184", t2)]:
        m = re.search(r'(\w+)\s*:\s*"' + kw + r'"', txt)
        if m:
            print(f"[{name}] {m.group(0)}")
