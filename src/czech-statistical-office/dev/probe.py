from subsets_utils import get
import json

BASE = "https://vdb.czso.cz/pll/eweb"

for eid in ["010022", "sldb2021_byty_energie", "CZ_NACE_RES", "050101"]:
    print("="*70)
    print("ENTITY", eid)
    r = get(f"{BASE}/package_show", params={"id": eid}, timeout=(10,120))
    j = r.json()
    res = j["result"]["resources"]
    print(" #resources:", len(res))
    for rr in res:
        print("   format=", repr(rr.get("format")), "| name=", rr.get("name"), "| url=", rr.get("url"))
    # download the csv resource
    csv_res = [rr for rr in res if (rr.get("format") or "").lower() in ("csv","text/csv")]
    if not csv_res:
        print("  !! no csv resource; formats:", [rr.get("format") for rr in res]); continue
    url = csv_res[0]["url"]
    cr = get(url, timeout=(10,120))
    raw = cr.content
    print("  csv bytes:", len(raw), "| content-type:", cr.headers.get("content-type"))
    # encoding sniff
    for enc in ("utf-8","cp1250"):
        try:
            txt = raw.decode(enc)
            head = txt.splitlines()[:2]
            print(f"  decode {enc} OK; first line:", head[0][:160])
            if len(head)>1: print("     row1:", head[1][:160])
            break
        except UnicodeDecodeError as e:
            print(f"  decode {enc} FAIL: {e}")
