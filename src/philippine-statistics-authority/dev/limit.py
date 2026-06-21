import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post
BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"
mid = "2M/PI/CPI/2012/0012M4ACPI1.px"
meta = get(BASE+mid, timeout=(10,60)).json()
vars_={v["code"]:v["values"] for v in meta["variables"]}
# build a selection targeting ~N cells using Geolocation(101) x Commodity(148) x Year(10) x Period(13)
def try_cells(geo,com,yr,per):
    sel=[
      {"code":"Geolocation","selection":{"filter":"item","values":vars_["Geolocation"][:geo]}},
      {"code":"Commodity Description","selection":{"filter":"item","values":vars_["Commodity Description"][:com]}},
      {"code":"Year","selection":{"filter":"item","values":vars_["Year"][:yr]}},
      {"code":"Period","selection":{"filter":"item","values":vars_["Period"][:per]}},
    ]
    cells=geo*com*yr*per
    q={"query":sel,"response":{"format":"json-stat2"}}
    r=post(BASE+mid,json=q,timeout=(10,180))
    nval = None
    if r.status_code==200:
        try: nval=len(r.json().get("value",[]))
        except: pass
    print(f"cells={cells:>8}  status={r.status_code}  returned_values={nval}")
    time.sleep(1.2)
    return r.status_code
for combo in [(101,10,10,13),(101,30,10,13),(101,60,10,13),(101,100,10,13),(101,148,10,13)]:
    try_cells(*combo)
