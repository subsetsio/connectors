import sys
sys.path.insert(0, 'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
# small datastore resource from impact-framework
rec=get(f"{BASE}/package_show",params={"id":"idb-group-impact-framework-performance-targets-2024-2030-dataset"},timeout=60).json()["result"]
target=None
for rr in rec["resources"]:
    if (rr.get("format") or "").upper()=="CSV" and not (rr.get("url") or "").startswith("http"):
        target=rr; break
print("target:", target["name"][:50], "id:", target["id"], "ds_active:", target.get("datastore_active"), flush=True)
rid=target["id"]
j=get(f"{BASE}/datastore_search", params={"resource_id":rid,"limit":3}, timeout=60).json()
print("ds_search success:", j["success"], "total:", j["result"]["total"], flush=True)
print("fields:", [(f["id"],f.get("type")) for f in j["result"]["fields"]], flush=True)
print("sample rec:", j["result"]["records"][0] if j["result"]["records"] else None, flush=True)
# datastore dump stream first 500 bytes
r=get(f"https://data.iadb.org/datastore/dump/{rid}", timeout=60)
print("dump status", r.status_code, "ctype", r.headers.get("content-type"), "first:", r.text[:200], flush=True)
