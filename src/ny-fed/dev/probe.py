import json
from subsets_utils import get

BASE = "https://markets.newyorkfed.org/api"

def g(path):
    r = get(f"{BASE}/{path}", timeout=(10, 120))
    r.raise_for_status()
    return r.json()

def show(label, obj, n=1):
    print(f"\n===== {label} =====")
    if isinstance(obj, list):
        print(f"list len={len(obj)}")
        for x in obj[:n]:
            print(json.dumps(x, indent=1)[:1500])
    else:
        print(json.dumps(obj, indent=1)[:1500])

# Reference rates secured (includes SOFRAI)
d = g("rates/secured/all/search.json?startDate=2026-06-01&endDate=2026-06-15")
show("secured refRates", d["refRates"], 4)

# Unsecured
d = g("rates/all/search.json?startDate=2026-06-08&endDate=2026-06-12")
show("all refRates", [r for r in d["refRates"] if r.get("type") in ("EFFR","OBFR")], 2)

# Repo details
d = g("rp/results/search.json?startDate=2026-06-01&endDate=2026-06-10")
ops = d["repo"]["operations"]
show("repo op[0]", ops[0])
print("repo details sample:", json.dumps(ops[0].get("details", [])[:1], indent=1)[:800])

# AMBS details
d = g("ambs/all/results/details/search.json?startDate=2026-05-01&endDate=2026-06-01")
a = d["ambs"]["auctions"]
show("ambs auction[0]", a[0])
print("ambs details:", json.dumps(a[0].get("details", [])[:1], indent=1)[:800])

# Treasury details
d = g("tsy/all/results/details/search.json?startDate=2024-01-01&endDate=2024-06-01")
a = d["treasury"]["auctions"]
show("tsy auction[0]", a[0])
print("tsy details:", json.dumps(a[0].get("details", [])[:1], indent=1)[:800])

# Seclending details
d = g("seclending/all/results/details/search.json?startDate=2026-06-01&endDate=2026-06-05")
o = d["seclending"]["operations"]
show("seclending op[0]", o[0])
print("seclending details:", json.dumps(o[0].get("details", [])[:1], indent=1)[:800])

# FX swaps
d = g("fxs/all/search.json?startDate=2020-03-01&endDate=2020-04-01")
show("fxSwaps op[0]", d["fxSwaps"]["operations"][0])

# SOMA summary
d = g("soma/summary.json")
s = d["soma"]["summary"]
show("soma summary[-1]", s[-1])
print("soma summary count:", len(s), "first:", s[0]["asOfDate"], "last:", s[-1]["asOfDate"])

# SOMA tsy holdings latest
asof = s[-1]["asOfDate"]
d = g(f"soma/tsy/get/all/asof/{asof}.json")
h = d["soma"]["holdings"]
show(f"soma tsy holdings asof {asof}", h[0])
print("tsy holdings count:", len(h))
d = g(f"soma/agency/get/asof/{asof}.json")
h2 = d["soma"]["holdings"]
print("agency holdings count:", len(h2))
if h2: show("agency holding[0]", h2[0])

# Primary dealer
d = g("pd/list/timeseries.json")
ts = d["pd"]["timeseries"]
print("\npd series count:", len(ts), "sample:", ts[0])
import csv, io
r = get(f"{BASE}/pd/latest/{ts[0]['keyid']}.csv", timeout=(10,120))
print("pd csv status", r.status_code, "head:")
print(r.text[:400])
