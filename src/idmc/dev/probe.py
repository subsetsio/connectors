import json
from subsets_utils import get

CID = "IDMCWSHSOLO009"
BASE = "https://helix-tools-api.idmcdb.org/external-api"


def envelope(path):
    r = get(f"{BASE}/{path}", params={"client_id": CID, "limit": 2})
    print(f"\n=== {path} -> {r.status_code}")
    j = r.json()
    if isinstance(j, dict):
        print("keys:", list(j.keys()))
        print("count:", j.get("count"))
        results = j.get("results", [])
        if results:
            print("first record keys:", list(results[0].keys()))
            print(json.dumps(results[0], indent=2, default=str)[:1500])
    else:
        print("type:", type(j), "len:", len(j) if hasattr(j, "__len__") else "?")


for p in [
    "gidd/conflicts/",
    "gidd/disasters/",
    "gidd/displacements/",
]:
    envelope(p)

# IDU: redirect to gzip S3 json array
r = get(f"{BASE}/idus/all/", params={"client_id": CID})
print(f"\n=== idus/all -> {r.status_code}, content-type={r.headers.get('content-type')}, len bytes={len(r.content)}")
data = r.json()
print("idu type:", type(data), "len:", len(data) if hasattr(data, "__len__") else "?")
if isinstance(data, list) and data:
    print("idu first keys:", list(data[0].keys()))
    print(json.dumps(data[0], indent=2, default=str)[:1500])

# disaggregations geojson
r = get(f"{BASE}/gidd/disaggregations/disaggregation-geojson/", params={"client_id": CID})
print(f"\n=== disaggregation-geojson -> {r.status_code}, content-type={r.headers.get('content-type')}, len bytes={len(r.content)}")
gj = r.json()
print("geojson keys:", list(gj.keys()) if isinstance(gj, dict) else type(gj))
feats = gj.get("features", []) if isinstance(gj, dict) else []
print("num features:", len(feats))
if feats:
    print("feature keys:", list(feats[0].keys()))
    print("property keys:", list(feats[0].get("properties", {}).keys()))
    print("geometry:", json.dumps(feats[0].get("geometry"), default=str)[:300])
    print(json.dumps(feats[0].get("properties"), indent=2, default=str)[:1500])
