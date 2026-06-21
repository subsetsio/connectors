from subsets_utils import get
import csv, io

BASE="https://www.opendata.nhs.scot/api/3/action"

def show(pkg):
    r=get(f"{BASE}/package_show", params={"id":pkg}, timeout=(10,120)).json()["result"]
    res=[x for x in r.get("resources",[]) if (x.get("format") or "").upper()=="CSV"]
    print(f"\n=== {pkg}: {len(res)} CSV resources (of {r.get('num_resources')}) ===")
    schemas=[]
    for x in res[:4]:
        rid=x["id"]
        # HEAD for size
        resp=get(f"https://www.opendata.nhs.scot/datastore/dump/{rid}", params={"bom":"true"}, timeout=(10,120))
        text=resp.text
        size=len(resp.content)
        rows=text.splitlines()
        hdr=rows[0] if rows else ""
        cols=next(csv.reader([hdr]))
        schemas.append(tuple(c.lstrip("﻿") for c in cols))
        print(f"  {x['name'][:40]:40} {size/1024:.0f}KB rows~{len(rows)-1} cols={len(cols)}")
    if len(set(schemas))==1:
        print(f"  -> all sampled schemas IDENTICAL ({len(schemas[0])} cols): {schemas[0][:8]}")
    else:
        print(f"  -> schemas DIFFER across resources:")
        for s in set(schemas): print("     ", s[:8], f"({len(s)} cols)")

for p in ["annual-cancer-incidence","prescriptions-in-the-community","gp-practice-populations","monthly-accident-and-emergency-activity-and-waiting-times","population-estimates"]:
    try: show(p)
    except Exception as e: print(p,"ERR",type(e).__name__,e)
