import sys
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _plan_blocks, _get_json, BASE, MAX_CELLS, MAX_VALUES
path="TIR/AT/ATD/ATD060m"
meta=_get_json(BASE+path)
for v in meta["variables"]:
    print("var",v["code"],"nvals",len(v["values"]))
blocks=_plan_blocks(meta["variables"])
print("n blocks:", len(blocks))
# verify all blocks within limits
bad=0
for b in blocks:
    n=1
    for vals in b.values(): n*=max(1,len(vals))
    if n>MAX_CELLS or any(len(v)>MAX_VALUES for v in b.values()): bad+=1
print("blocks over limit:", bad)
