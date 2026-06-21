import sys, math, time; sys.argv=["x"]
from nodes import geostat as G
import constants
G._ensure_client()
# Scan a handful of census/gender tables to find one exceeding the 10000 cap
cands=[e for e in constants.ENTITY_IDS if e.startswith(("population-census","gender-statistics"))][:40]
found=None
for e in cands:
    url=G.BASE+constants.ENTITY_PATHS[e]
    try:
        meta=G._get_meta(url)
    except Exception as ex:
        print("meta err",e,ex); continue
    total=math.prod(len(v["values"]) for v in meta["variables"])
    if total>10000:
        found=(e,total,[(v["code"],len(v["values"])) for v in meta["variables"]]); break
print("largest-found:", found)
if found:
    e=found[0]; url=G.BASE+constants.ENTITY_PATHS[e]
    meta=G._get_meta(url)
    used=set(); colmap={v["code"]:G._col_name(v["code"],used) for v in meta["variables"]}
    dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
    blocks=list(G._blocks(dims))
    maxb=max(math.prod(len(v) for _,v in b) for b in blocks)
    bc=sum(math.prod(len(v) for _,v in b) for b in blocks)
    print(f"total={math.prod(len(v) for _,v in dims)} blocks={len(blocks)} max_block_cells={maxb} sum={bc}")
    t=time.time(); rows=[]
    for b in blocks:
        body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
        rows.extend(G._decode(G._post_data(url,body)["dataset"], colmap))
    print(f"rows={len(rows)} cols={list(colmap.values())} elapsed={time.time()-t:.1f}s")
    print("sample:", rows[0])
