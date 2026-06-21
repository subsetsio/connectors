import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}

def g(path):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=H, timeout=(10,120))
    r.raise_for_status()
    return r

# 1. ips table-result full structure for patent ind 10 rt 11
r = g("ips-search/table-result?selectedTab=patent&indicator=10&reportType=11&fromYear=2022&toYear=2023")
d = r.json()
print("=== IPS table-result keys:", list(d.keys()))
print("recordInfo:", json.dumps(d.get("recordInfo")))
print("columns:", json.dumps(d.get("columns"))[:600])
print("rec[0]:", json.dumps(d["records"][0]))
print("rec[5]:", json.dumps(d["records"][5]))
print()
# Compare report types 11 vs 13 vs 15 for same indicator to see what the comma-packed values mean
for rt in (11,13,15):
    dd = g(f"ips-search/table-result?selectedTab=patent&indicator=10&reportType={rt}&fromYear=2022&toYear=2022").json()
    recs = dd.get("records") or []
    print(f"--- rt={rt} ncols={len(dd.get('columns') or [])} nrec={len(recs)} sample={json.dumps(recs[0]) if recs else None}")
