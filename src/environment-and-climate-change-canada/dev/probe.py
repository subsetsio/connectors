import sys; sys.path.insert(0,"src")
import json
from subsets_utils import get

ENTS = ["ahccd-annual","ahccd-monthly","ahccd-seasonal","ahccd-stations","ahccd-trends",
"aqhi-observations-realtime","aqhi-stations","climate-daily","climate-hourly","climate-monthly",
"climate-normals","climate-stations","hydrometric-annual-peaks","hydrometric-annual-statistics",
"hydrometric-daily-mean","hydrometric-monthly-mean","hydrometric-realtime","hydrometric-stations",
"ltce-precipitation","ltce-snowfall","ltce-stations","ltce-temperature","swob-realtime","swob-stations"]

base="https://api.weather.gc.ca"
for e in ENTS:
    try:
        r=get(f"{base}/collections/{e}/items", params={"limit":1,"f":"json"}, timeout=(10,120))
        d=r.json()
        nm=d.get("numberMatched")
        feats=d.get("features",[])
        props=sorted(feats[0]["properties"].keys()) if feats else []
        print(f"{e:32s} matched={nm!s:>11}  nprops={len(props)}")
    except Exception as ex:
        print(f"{e:32s} ERROR {type(ex).__name__}: {ex}")
