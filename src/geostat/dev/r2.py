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
print("dataset keys:", list(ds.keys()))
for k in ds:
    if k!="dimension":
        v=ds[k]
        print(" ",k,"=", (v if not isinstance(v,list) else f"list len {len(v)} head {v[:3]}"))
