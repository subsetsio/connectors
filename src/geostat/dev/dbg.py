import sys, json; sys.argv=["x"]
from nodes import geostat as G
G._ensure_client()
eid="agriculture-animal-20husbandry-table-3-01"
url=G.BASE+G.ENTITY_PATHS[eid]
meta=G._get_meta(url)
used=set()
colmap={v["code"]:G._col_name(v["code"],used) for v in meta["variables"]}
dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
for bi,b in enumerate(G._blocks(dims)):
    body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
    ds=G._post_data(url,body)["dataset"]
    print("block",bi,"dataset keys:",list(ds.keys()),"dim type:",type(ds["dimension"]).__name__)
    if isinstance(ds["dimension"], list):
        print("  DIMENSION IS LIST. id=",ds.get("id"))
        print("  full:", json.dumps(ds,ensure_ascii=False)[:1200])
        break
