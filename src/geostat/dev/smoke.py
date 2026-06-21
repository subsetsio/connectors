import sys
sys.argv=["x"]
from nodes import geostat as G
G._ensure_client()

def run(eid):
    url=G.BASE+G.ENTITY_PATHS[eid]
    meta=G._get_meta(url)
    used=set()
    colmap={v["code"]:G._col_name(v["code"],used) for v in meta["variables"]}
    dims=[[v["code"],list(v["values"])] for v in meta["variables"]]
    import math
    total=math.prod(len(v) for _,v in dims)
    blocks=list(G._blocks(dims))
    # verify block coverage == total cells and each block <= cap
    bc=sum(math.prod(len(v) for _,v in b) for b in blocks)
    rows=[]
    for b in blocks:
        body={"query":[{"code":c,"selection":{"filter":"item","values":vv}} for c,vv in b],"response":{"format":"json-stat"}}
        rows.extend(G._decode(G._post_data(url,body)["dataset"], colmap))
    print(f"{eid}\n  cols={list(colmap.values())} total_cells={total} blocks={len(blocks)} block_cell_sum={bc} rows={len(rows)}")
    print("  sample row:", rows[0])
    nn=sum(1 for r in rows if r['value'] is not None)
    print("  non-null values:", nn)

# small 2-dim
run("agriculture-animal-20husbandry-table-3-01")
# find a large multi-dim census table from constants to stress split
import constants
big=[e for e,p in constants.ENTITY_PATHS.items() if e.startswith("population-census")][:1]
for e in big: run(e)
