import subsets_utils as su
import json, io, csv

BASE="https://data-api.globalforestwatch.org"

def show(name):
    r=su.get(f"{BASE}/dataset/{name}", timeout=60)
    d=r.json()["data"]
    print("===",name,"=== versions:",d.get("versions"))
    return d.get("versions")

# 1. version resolution + does 'latest' redirect work in download path?
for n in ["gadm__tcl__iso_summary","gadm__integrated_alerts__iso_daily_alerts","carbonflux_iso_summary","fao_forestry_employment","nasa_viirs_fire_alerts"]:
    show(n)

# 2. 'latest' redirect on download/csv
import urllib.parse
sql="SELECT * FROM data LIMIT 3"
url=f"{BASE}/dataset/gadm__tcl__iso_summary/latest/download/csv"
r=su.get(url, params={"sql":sql}, timeout=120)
print("latest download status", r.status_code, "final url", str(r.url))
print("content-type", r.headers.get("content-type"))
txt=r.text
print("first 800 chars:\n", txt[:800])

# 3. count(*) via download endpoint?
for n in ["gadm__tcl__iso_summary","carbonflux_iso_summary","fao_forestry_employment","gadm__integrated_alerts__iso_daily_alerts","gadm__viirs__adm2_daily_alerts","nasa_viirs_fire_alerts"]:
    r=su.get(f"{BASE}/dataset/{n}/latest/download/csv", params={"sql":"SELECT count(*) AS n FROM data"}, timeout=120)
    print(n, r.status_code, repr(r.text[:120]))
