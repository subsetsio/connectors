import sys; sys.path.insert(0,"src")
from subsets_utils import get
base="https://api.weather.gc.ca"
# full count
full=get(f"{base}/collections/climate-monthly/items", params={"limit":1,"f":"json"}, timeout=(15,120)).json().get("numberMatched")
# bogus field
r=get(f"{base}/collections/climate-monthly/items", params={"BOGUS_FIELD":"xyz","limit":1,"f":"json"}, timeout=(15,120))
print("bogus param: status", r.status_code, "matched", r.json().get("numberMatched") if r.status_code==200 else r.text[:150])
# real field, nonexistent value
r2=get(f"{base}/collections/climate-monthly/items", params={"CLIMATE_IDENTIFIER":"ZZZZNONE","limit":1,"f":"json"}, timeout=(15,120))
print("real field bad value: status", r2.status_code, "matched", r2.json().get("numberMatched"))
print("full collection matched:", full)
