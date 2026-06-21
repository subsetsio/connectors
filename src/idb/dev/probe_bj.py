import sys
sys.path.insert(0,'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
rec=get(f"{BASE}/package_show",params={"id":"2020-better-jobs-index-database-latin-america"},timeout=60).json()["result"]
for rr in rec["resources"]:
    print("name:", rr.get("name"))
    print("  format:", rr.get("format"), "datastore_active:", rr.get("datastore_active"))
    print("  url:", repr(rr.get("url")))
    print("  url_type:", rr.get("url_type"), "mimetype:", rr.get("mimetype"))
