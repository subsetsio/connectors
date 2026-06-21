import sys
sys.path.insert(0, 'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
rec=get(f"{BASE}/package_show",params={"id":"social-indicators-of-latin-america-and-the-caribbean"},timeout=60).json()["result"]
# find a CSV resource with empty url but datastore_active
for rr in rec["resources"]:
    if (rr.get("format") or "").upper()=="CSV" and not (rr.get("url") or "").startswith("http"):
        rid=rr["id"]
        print("resource:", rr["name"][:50], "id:", rid, "datastore_active:", rr.get("datastore_active"))
        # try datastore dump
        for ep in (f"https://data.iadb.org/datastore/dump/{rid}",):
            try:
                r=get(ep, timeout=60)
                txt=r.content.decode("utf-8","replace")
                print(f"  DUMP {ep[-40:]}: status={r.status_code} len={len(txt)}")
                for l in txt.splitlines()[:4]: print("    ", l[:140])
            except Exception as e:
                print("  DUMP err", type(e).__name__, str(e)[:80])
        # try datastore_search
        r=get(f"{BASE}/datastore_search", params={"resource_id":rid,"limit":2}, timeout=60)
        j=r.json()
        print("  datastore_search success:", j.get("success"), "total:", j.get("result",{}).get("total"))
        fields=j.get("result",{}).get("fields")
        print("  fields:", [f.get("id") for f in (fields or [])][:15])
        break
