import sys
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _get_json, _resolve_values, _plan_blocks, BASE, MAX_CELLS, MAX_VALUES
path="TIR/AT/ATD/ATD060m"
meta=_get_json(BASE+path)
res=_resolve_values(BASE+path, meta["variables"])
print({k:len(v) for k,v in res.items()})
blocks=_plan_blocks(res)
print("n blocks:", len(blocks))
bad=sum(1 for b in blocks if (lambda n: n>MAX_CELLS)(__import__('math').prod(len(v) for v in b.values())) or any(len(v)>MAX_VALUES for v in b.values()))
print("over-limit blocks:", bad)
# total cells
import math
tot=math.prod(len(v) for v in res.values())
print("total cells:", tot, "≈ posts:", len(blocks))
