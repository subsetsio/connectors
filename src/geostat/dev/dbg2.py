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
    try:
        rows=G._decode(ds, colmap)
        print("block",bi,"rows",len(rows),"sample",rows[0])
    except Exception as e:
        print("ERR block",bi,type(e).__name__,e)
        print("dim type:",type(ds["dimension"]).__name__,"id:",ds.get("id"),"size:",ds.get("size"))
        print(json.dumps(ds,ensure_ascii=False)[:1500])
