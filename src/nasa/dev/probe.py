import json
from subsets_utils import get

def show(title): print("\n===== "+title+" =====")

# 1. TAP json shape + types
show("TAP json: select top 2 pl_name,disc_year,pl_orbper from ps")
r = get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
        params={"query":"select top 2 pl_name,disc_year,pl_orbper from ps","format":"json"},
        timeout=(10,120))
print("status", r.status_code, "ctype", r.headers.get("content-type"))
print(r.text[:600])

# 2. TAP uppercase table name case handling
show("TAP json count Q1_Q17_DR25_KOI (uppercase)")
r = get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
        params={"query":"select count(*) as n from Q1_Q17_DR25_KOI","format":"json"}, timeout=(10,120))
print(r.status_code, r.text[:300])

# 3. JPL envelope (fireball small)
show("JPL fireball.api?limit=2")
r = get("https://ssd-api.jpl.nasa.gov/fireball.api", params={"limit":"2"}, timeout=(10,120))
d = r.json()
print("keys", list(d.keys()), "count", d.get("count"), "version", d.get("signature",{}).get("version"))
print("fields", d.get("fields"))
print("row0", d.get("data",[None])[0])

# 4. gistemp csv head
show("gistemp GLB.Ts+dSST.csv head")
r = get("https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv", timeout=(10,120))
print(r.status_code, "ctype", r.headers.get("content-type"))
print("\n".join(r.text.splitlines()[:4]))
show("gistemp ZonAnn head")
r = get("https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv", timeout=(10,120))
print("\n".join(r.text.splitlines()[:3]))

# 5. eonet events geometry
show("eonet events?limit=1&status=all")
r = get("https://eonet.gsfc.nasa.gov/api/v3/events", params={"limit":"1","status":"all"}, timeout=(10,120))
d = r.json()
ev = d.get("events",[])[0]
print("event keys", list(ev.keys()))
print("categories", ev.get("categories"))
print("sources", ev.get("sources"))
print("geometry0", ev.get("geometry",[None])[0])
