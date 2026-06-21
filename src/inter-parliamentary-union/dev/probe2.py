import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import json
from subsets_utils import get

def latest(attr):
    if isinstance(attr,list):
        if not attr: return None
        cur=[e for e in attr if isinstance(e,dict) and not e.get("date_to")]
        e=cur[-1] if cur else attr[-1]
        return e.get("value") if isinstance(e,dict) else None
    if isinstance(attr,dict): return attr.get("value")
    return attr

r=get("https://api.data.ipu.org/v1/chambers/?page[size]=1",headers={"Accept-Language":"en"},timeout=(10,120))
row=r.json()["data"][0]; attrs=row["attributes"]
print("CHAMBER id",row["id"],"nfields",len(attrs))
for k in sorted(attrs):
    v=latest(attrs[k])
    t=type(v).__name__
    print(f"  {k}: ({t}) {json.dumps(v,ensure_ascii=False)[:90]}")
