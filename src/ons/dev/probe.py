from subsets_utils import get
import json

def show(did):
    r = get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}", timeout=(10,60))
    print(did, "->", r.status_code)
    if r.status_code != 200:
        print("  body:", r.text[:200]); return
    d = r.json()
    print("  dataset links keys:", list(d.get("links",{}).keys()))
    lv = d.get("links",{}).get("latest_version")
    print("  latest_version:", lv)
    # editions
    ed = get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}/editions", timeout=(10,60)).json()
    print("  editions count:", ed.get("total_count"), [e.get("edition") for e in ed.get("items",[])])
    for e in ed.get("items",[])[:1]:
        lvh = e.get("links",{}).get("latest_version",{})
        print("  edition latest_version:", lvh.get("href"), "id", lvh.get("id"))
        vr = get(lvh["href"], timeout=(10,60)).json()
        print("  version downloads keys:", list(vr.get("downloads",{}).keys()))
        print("  csv href:", vr.get("downloads",{}).get("csv",{}).get("href"))

for did in ["TS009","ts009","retail-sales-index"]:
    try: show(did)
    except Exception as e: print(did,"ERR",type(e).__name__,e)
    print()

# fetch a small census CSV head to see v4 format
r = get("https://api.beta.ons.gov.uk/v1/datasets/TS001/editions", timeout=(10,60)).json()
e = r["items"][0]
vr = get(e["links"]["latest_version"]["href"], timeout=(10,60)).json()
csvurl = vr["downloads"]["csv"]["href"]
print("TS001 csv url:", csvurl, "size", vr["downloads"]["csv"].get("size"))
cr = get(csvurl, timeout=(10,120))
print("status", cr.status_code, "final_url", str(cr.url))
lines = cr.text.splitlines()
print("rows:", len(lines))
print("header:", lines[0])
print("row1:", lines[1] if len(lines)>1 else None)
