import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post
BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"
mid = "2M/PI/CPI/2012/0012M4ACPI1.px"
meta = get(BASE+mid, timeout=(10,60)).json()
vars_={v["code"]:v["values"] for v in meta["variables"]}
def try_cells(geo,com,yr,per):
    sel=[
      {"code":"Geolocation","selection":{"filter":"item","values":vars_["Geolocation"][:geo]}},
      {"code":"Commodity Description","selection":{"filter":"item","values":vars_["Commodity Description"][:com]}},
      {"code":"Year","selection":{"filter":"item","values":vars_["Year"][:yr]}},
      {"code":"Period","selection":{"filter":"item","values":vars_["Period"][:per]}},
    ]
    cells=geo*com*yr*per
    r=post(BASE+mid,json={"query":sel,"response":{"format":"json-stat2"}},timeout=(10,180))
    print(f"cells={cells:>8}  status={r.status_code}")
    time.sleep(1.2)
    return r.status_code
# narrow between 1010 and 131300
for combo in [(101,10,10,5),(101,10,10,10),(101,20,10,10),(101,30,10,10),(101,40,10,13),(101,50,10,13)]:
    try_cells(*combo)
