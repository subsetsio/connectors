import sys; sys.path.insert(0,"src")
from subsets_utils import get
base="https://api.weather.gc.ca"
# verify station-id field exists in stations collection AND filtering obs works
checks=[
 ("climate-stations","CLIMATE_IDENTIFIER","climate-monthly"),
 ("ahccd-stations","station_id__id_station","ahccd-monthly"),
 ("hydrometric-stations","STATION_NUMBER","hydrometric-monthly-mean"),
 ("ltce-stations","VIRTUAL_CLIMATE_ID","ltce-temperature"),
 ("aqhi-stations","location_id","aqhi-observations-realtime"),
]
for stn_coll, field, obs in checks:
    r=get(f"{base}/collections/{stn_coll}/items", params={"limit":1,"f":"json"}, timeout=(15,120))
    f0=r.json()["features"][0]["properties"]
    val=f0.get(field)
    # filter obs by that value
    r2=get(f"{base}/collections/{obs}/items", params={field:val,"limit":1,"f":"json"}, timeout=(15,120))
    m=r2.json().get("numberMatched")
    print(f"{stn_coll}.{field}={val!r:>14} -> {obs} filtered matched={m}")
# how many stations in each master list
for c in ["climate-stations","ahccd-stations","hydrometric-stations","ltce-stations","aqhi-stations"]:
    r=get(f"{base}/collections/{c}/items", params={"limit":1,"f":"json"}, timeout=(15,120))
    print(c, "count=", r.json().get("numberMatched"))
