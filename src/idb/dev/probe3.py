import sys, collections
sys.path.insert(0, 'src')
from subsets_utils import get
BASE = "https://data.iadb.org/api/3/action"
def show(pid):
    return get(f"{BASE}/package_show", params={"id": pid}, timeout=60).json()["result"]
rec = show("latin-macro-watch-dataset")
res = [r for r in rec["resources"] if (r.get("format") or "").upper()=="CSV"]
for rr in res[:5]:
    print("name:", rr.get("name"))
    print("  id:", rr.get("id"))
    print("  url:", repr(rr.get("url")))
    print("  url_type:", rr.get("url_type"), "datastore_active:", rr.get("datastore_active"))
# count url schemes
import urllib.parse
schemes=collections.Counter()
empty=0
for rr in res:
    u=rr.get("url") or ""
    schemes[urllib.parse.urlparse(u).scheme or "NONE"]+=1
print("schemes:", dict(schemes))
