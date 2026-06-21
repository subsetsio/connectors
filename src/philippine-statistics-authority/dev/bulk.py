import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post
BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"

# A ~5616-cell table (>1000) — try to pull ALL in one POST
path = "2I/0082I5DFCF2.px"  # small, 72 cells -> baseline
# Use a medium table: CPI 2012 has 1.9M; pick mid. Find one ~5k from metadata
mid = "2M/PI/CPI/2012/0012M4ACPI1.px"
meta = get(BASE+mid, timeout=(10,60)).json()
# select ALL values of every variable -> ~1.9M cells, expect 400 maxValues
sel = [{"code": v["code"], "selection": {"filter":"all","values":["*"]}} for v in meta["variables"]]
q = {"query": sel, "response":{"format":"json-stat2"}}
r = post(BASE+mid, json=q, timeout=(10,120))
print("FULL pull status:", r.status_code)
print("body head:", r.text[:300])

# Try selecting just over 1000: Geolocation(101) x Period one value? do Geolocation all (101) x Year all(10) =1010
sel2=[]
for v in meta["variables"]:
    if v["code"]=="Geolocation": sel2.append({"code":v["code"],"selection":{"filter":"all","values":["*"]}})
    elif v["code"]=="Year": sel2.append({"code":v["code"],"selection":{"filter":"all","values":["*"]}})
    else: sel2.append({"code":v["code"],"selection":{"filter":"item","values":[v["values"][0]]}})
q2={"query":sel2,"response":{"format":"json-stat2"}}
r2=post(BASE+mid,json=q2,timeout=(10,120))
print("\n1010-cell pull status:", r2.status_code, "body head:", r2.text[:200])
