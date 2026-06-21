from subsets_utils import get
BASE="https://www.opendata.nhs.scot/api/3/action"

def show(pkg):
    r=get(f"{BASE}/package_show", params={"id":pkg}, timeout=(10,60)).json()["result"]
    res=[x for x in r.get("resources",[]) if (x.get("format") or "").upper()=="CSV"]
    print(f"\n=== {pkg}: {len(res)} CSV res (of {r.get('num_resources')}) ===")
    schemas=[]
    for x in res[:5]:
        rid=x["id"]
        try:
            ds=get(f"{BASE}/datastore_search", params={"resource_id":rid,"limit":0}, timeout=(10,60)).json()
            fields=[f["id"] for f in ds["result"]["fields"]]
            total=ds["result"].get("total")
        except Exception as e:
            fields=[f"ERR:{type(e).__name__}"]; total="?"
        schemas.append(tuple(fields))
        print(f"  {x['name'][:38]:38} total={total} cols={len(fields)} {fields[:6]}")
    uniq=set(schemas)
    print(f"  -> {'IDENTICAL' if len(uniq)==1 else 'DIFFER'} across {len(res[:5])} sampled")

for p in ["annual-cancer-incidence","prescriptions-in-the-community","gp-practice-populations","monthly-accident-and-emergency-activity-and-waiting-times","population-estimates","geography-codes-and-labels"]:
    try: show(p)
    except Exception as e: print(p,"ERR",type(e).__name__,e)
print("\nALLDONE")
