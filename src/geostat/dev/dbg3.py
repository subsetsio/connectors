import sys, json; sys.argv=["x"]
from nodes import geostat as G
G._ensure_client()
url=G.BASE+G.ENTITY_PATHS["agriculture-animal-20husbandry-table-3-01"]
meta=G._get_meta(url)
dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
b=list(G._blocks(dims))[0]
body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
ds=G._post_data(url,body)["dataset"]
order = ds.get("id") or list(ds["dimension"].keys())
print("order:", order, [type(x).__name__ for x in order])
print("ds['id']:", repr(ds.get("id")))
d=order[0]
print("dim[d] type:", type(ds["dimension"][d]).__name__)
print("category type:", type(ds["dimension"][d]["category"]).__name__)
print("index type:", type(ds["dimension"][d]["category"]["index"]).__name__)
