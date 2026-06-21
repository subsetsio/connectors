import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import json
from subsets_utils import get

def show(ep, n=1, report=False):
    url=f"https://api.data.ipu.org/v1/{ep}"
    sep = "&" if "?" in url else "?"
    if not report:
        url=f"{url}{sep}page[size]={n}"
    r=get(url, headers={"Accept-Language":"en"}, timeout=(10,120))
    d=r.json()
    data=d.get("data")
    if isinstance(data,dict): rows=list(data.values())
    elif isinstance(data,list): rows=data
    else: rows=[]
    print(f"\n===== {ep}  total={d.get('meta',{}).get('total')} rows={len(rows)} =====")
    row=rows[0] if rows else {}
    if isinstance(row,dict) and "attributes" in row:
        print("id=",row.get("id"),"type=",row.get("type"))
        attrs=row["attributes"]
        for k in sorted(attrs)[:200]:
            v=attrs[k]
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:120]}")
    else:
        for k in sorted(row):
            print(f"  {k}: {json.dumps(row[k], ensure_ascii=False)[:120]}")

for ep in ["countries","parliaments","elections","political_parties","people","specialized_bodies"]:
    show(ep)
