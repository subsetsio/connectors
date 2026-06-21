import sys; sys.argv=["x"]
from nodes import geostat as G
G._ensure_client()
eid="agriculture-animal-20husbandry-table-3-01"
url=G.BASE+G.ENTITY_PATHS[eid]
meta=G._get_meta(url)
dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
b=list(G._blocks(dims))[0]
body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
ds=G._post_data(url,body)["dataset"]
print("has id?", "id" in ds, "| dimension type:", type(ds["dimension"]).__name__)
print("id value:", ds.get("id"))
print("size value:", ds.get("size"))
