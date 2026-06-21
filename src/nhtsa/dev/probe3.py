from subsets_utils import get
def fetch(u):
    r=get(u, timeout=(10,60))
    return r.status_code, r.headers.get("content-type"), r.text[:300]
B="https://api.nhtsa.gov/SafetyRatings"
# real traversal to a VehicleId
import json
def j(u): return get(u,timeout=(10,60)).json()
makes=j(f"{B}/modelyear/2020")["Results"]
mk=makes[0]["Make"]
models=j(f"{B}/modelyear/2020/make/{mk}")["Results"]
md=models[0]["Model"]
variants=j(f"{B}/modelyear/2020/make/{mk}/model/{md}")["Results"]
print("variants:", variants)
vid=variants[0]["VehicleId"]
print("chosen vid:", vid)
print("DETAIL status/type/body:", fetch(f"{B}/VehicleId/{vid}"))
