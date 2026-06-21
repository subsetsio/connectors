import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}
HC = {"Accept-Language": "en"}


def g(path, headers=H):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=headers, timeout=(10, 120))
    return r


# A) keyindicators-json
r = g("keyindicator/keyindicators-json")
print("=== keyindicators-json status", r.status_code)
d = r.json()
print("type", type(d).__name__)
print(json.dumps(d)[:1500])

# B) keyindicator downloadCsv/{id}
r = g("keyindicator/downloadCsv/201", headers=HC)
print("\n=== keyindicator downloadCsv/201 status", r.status_code, "ctype", r.headers.get("content-type"))
print(repr(r.text[:1500]))

# C) ips formcontrols
r = g("ips-search/formcontrols?selectedTab=patent")
print("\n=== ips formcontrols patent status", r.status_code)
d = r.json()
print("keys", list(d.keys()))
for k in ("ipsIndicatorMap", "ipsRpTypeMap", "ipsFYears", "ipsToYearList", "ipsToYear"):
    print(k, "=>", json.dumps(d.get(k))[:400])

# D) ips downloadCsv exact format
r = g("ips-search/downloadCsv?selectedTab=patent&indicator=10&reportType=11&fromYear=2022&toYear=2023", headers=HC)
print("\n=== ips downloadCsv status", r.status_code, "ctype", r.headers.get("content-type"))
print(repr(r.text[:1500]))
