import sys, json
sys.path.insert(0,"src")
from nodes.central_statistical_bureau import _get_json, BASE
meta=_get_json(BASE+"TIR/AT/ATD/ATD060m")
print("title:", meta["title"][:60])
for v in meta["variables"]:
    print("code:",v.get("code"),"keys:",sorted(v.keys()),"nvals:", len(v.get("values",[])))
