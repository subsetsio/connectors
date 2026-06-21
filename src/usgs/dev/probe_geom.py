from subsets_utils import get
BASE="https://api.waterdata.usgs.gov/ogcapi/v0"
for coll in ["monitoring-locations","combined-metadata","daily","peaks"]:
    r=get(f"{BASE}/collections/{coll}/items",params={"f":"json","limit":2},timeout=(10,120))
    j=r.json()
    f0=(j.get("features") or [{}])[0]
    g=f0.get("geometry")
    print(coll,"status",r.status_code,"nfeat",len(j.get("features") or []),"geom",g)
