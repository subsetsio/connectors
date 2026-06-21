from subsets_utils import get
def show(t): print("\n=== "+t+" ===")

for st in [None, "open", "closed", "all"]:
    params={"limit":"2"}
    if st: params["status"]=st
    r=get("https://eonet.gsfc.nasa.gov/api/v3/events", params=params, timeout=(10,120))
    d=r.json()
    print("status param=",st,"-> n events", len(d.get("events",[])))

show("eonet one open event full shape")
r=get("https://eonet.gsfc.nasa.gov/api/v3/events", params={"status":"open","limit":"1"}, timeout=(10,120))
ev=r.json()["events"][0]
print("keys", list(ev.keys()))
print("categories", ev.get("categories"))
print("sources", ev.get("sources"))
print("geometry0", ev.get("geometry",[None])[0])

show("gistemp NH/SH first lines")
for f in ["NH.Ts+dSST.csv","SH.Ts+dSST.csv"]:
    r=get("https://data.giss.nasa.gov/gistemp/tabledata_v4/"+f, timeout=(10,120))
    print(f, "->", r.text.splitlines()[0])

show("JPL counts cad/sentry/nhats (full, no filter)")
for ep,p in [("cad.api",{"date-min":"1900-01-01","date-max":"2100-01-01"}),("sentry.api",{}),("nhats.api",{})]:
    r=get("https://ssd-api.jpl.nasa.gov/"+ep, params=p, timeout=(20,180))
    d=r.json()
    print(ep, "count", d.get("count"), "nfields", len(d.get("fields") or []) if isinstance(d.get("fields"),list) else "n/a")
    print("   fields", d.get("fields"))
