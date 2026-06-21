import sys; sys.path.insert(0,"src")
import time
from subsets_utils import get
base="https://api.weather.gc.ca"
def t(coll, off, params=None):
    p={"limit":10000,"offset":off,"f":"json"}
    if params: p.update(params)
    s=time.time(); r=get(f"{base}/collections/{coll}/items", params=p, timeout=(15,300))
    d=r.json(); return time.time()-s, d.get("numberReturned"), r.status_code
for coll,offs in [("hydrometric-monthly-mean",[0,500000,2000000]),("climate-monthly",[0,1000000,1900000])]:
    for o in offs:
        dt,n,st=t(coll,o); print(f"{coll} offset={o:>8} -> {dt:5.1f}s n={n} st={st}")
# year-partition alternative for climate-monthly (datetime works?)
dt,n,st=t("climate-monthly",0,{"datetime":"2015-01-01/2015-12-31"}); print(f"climate-monthly datetime=2015 -> {dt:5.1f}s n={n}")
# station-partition: one station
import time as _t
s=_t.time(); r=get(f"{base}/collections/climate-monthly/items", params={"CLIMATE_IDENTIFIER":"6158355","limit":10000,"f":"json"}, timeout=(15,120)); print(f"climate-monthly one-station -> {_t.time()-s:5.1f}s n={r.json().get('numberReturned')}")
