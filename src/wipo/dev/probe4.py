import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}


def g(path):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=H, timeout=(10, 120))
    r.raise_for_status()
    return r


def afr(ind):
    d = g(f"ips-search/table-result?selectedTab=patent&indicator={ind}&reportType=11&fromYear=2022&toYear=2022").json()
    for rec in d["records"]:
        if rec.get("selectedOffice") == "Africa":
            return rec.get("2022")
    return None


print("ind10 (Total 1)        Africa 2022:", afr(10))
print("ind11 (1a Direct)      Africa 2022:", afr(11))
print("ind12 (1b PCT natl)    Africa 2022:", afr(12))

# how many packed values does a simple single indicator give? check ind 11 across offices
d = g("ips-search/table-result?selectedTab=patent&indicator=11&reportType=11&fromYear=2022&toYear=2022").json()
import collections
counts = collections.Counter(str(r.get("2022")).count(",") + 1 if r.get("2022") not in (None, "") else 0 for r in d["records"])
print("\nind11 rt11 packed-count distribution:", dict(counts))

d = g("ips-search/table-result?selectedTab=patent&indicator=10&reportType=11&fromYear=2022&toYear=2022").json()
counts = collections.Counter(str(r.get("2022")).count(",") + 1 if r.get("2022") not in (None, "") else 0 for r in d["records"])
print("ind10 rt11 packed-count distribution:", dict(counts))
