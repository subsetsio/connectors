import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get, post

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}


def try_get(path, label=""):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=H, timeout=(10, 120))
    print(f"GET [{r.status_code}] {label}\n    {r.text[:500]}\n")
    return r


# full pmhchart body
try_get("pmh-search/pmhchart?selectedTab=pct&indicator=1001&reportType=4001&fromYear=1995&toYear=2026", "pmhchart full")

# maybe a POST with a body is needed
for body in [
    {"selectedTab": "pct", "indicator": "1001", "reportType": "4001", "fromYear": "1995", "toYear": "2026"},
]:
    try:
        r = post(f"{API}/pmh-search/table-result?lang=en", headers={**H, "Content-Type": "application/json"},
                 json=body, timeout=(10, 120))
        print(f"POST table-result [{r.status_code}]\n    {r.text[:500]}\n")
    except Exception as e:
        print("POST err", e)

# discover the office/origin select endpoints the SPA might call
for ep in ["pmh-search/offices?selectedTab=pct", "pmh-search/origins?selectedTab=pct",
           "pmh-search/selectvalues?selectedTab=pct&indicator=1001",
           "pmh-search/to-year?selectedTab=pct", "pmh-search/formcontrols?selectedTab=pct&indicator=1001"]:
    try_get(ep, ep)
