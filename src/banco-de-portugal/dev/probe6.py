import json
from subsets_utils import get
spec=get("https://bpstat.bportugal.pt/data/docs/?format=openapi", timeout=(10,60)).json()
print("basePath:", spec.get("basePath"))
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        if method not in ("get","post"): continue
        params=op.get("parameters",[])
        pnames=[(p.get("name"),p.get("required"),p.get("description","")[:50]) for p in params]
        print(f"\n{method.upper()} {path}")
        print("   ", op.get("summary",""))
        for pn in pnames:
            print("     param:",pn)
