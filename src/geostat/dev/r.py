import sys; sys.argv=["x"]
from nodes import geostat as G
G._ensure_client()
eid="agriculture-animal-20husbandry-table-3-01"
url=G.BASE+G.ENTITY_PATHS[eid]
meta=G._get_meta(url)
dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
b=list(G._blocks(dims))[0]
body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
r=G._post_data(url,body)
print("top keys:", list(r.keys()))
import json
print(json.dumps(r, ensure_ascii=False)[:800])
