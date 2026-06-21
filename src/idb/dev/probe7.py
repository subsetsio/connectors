import sys
sys.path.insert(0,'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
def rows_for(rid):
    try:
        j=get(f"{BASE}/datastore_search", params={"resource_id":rid,"limit":0}, timeout=60).json()
        return j["result"].get("total")
    except Exception as e:
        return f"err:{type(e).__name__}"
for pid in ("latin-macro-watch-dataset","social-indicators-of-latin-america-and-the-caribbean",
            "idb-group-impact-framework-portfolio-results-dataset"):
    rec=get(f"{BASE}/package_show",params={"id":pid},timeout=60).json()["result"]
    res=[r for r in rec["resources"] if (r.get("format") or "").upper()=="CSV"]
    # sample row counts of first 8 datastore-active resources
    total=0; counted=0; ds=0; filed=0
    cols=set()
    for rr in res:
        if rr.get("datastore_active"): ds+=1
        elif (rr.get("url") or "").startswith("http"): filed+=1
    print(f"{pid}: {len(res)} csv | datastore_active={ds} file={filed}", flush=True)
    # row counts for first 5 ds resources + their fields
    for rr in res[:5]:
        if rr.get("datastore_active"):
            j=get(f"{BASE}/datastore_search", params={"resource_id":rr["id"],"limit":1}, timeout=60).json()
            t=j["result"].get("total"); fs=tuple(f["id"] for f in j["result"]["fields"])
            cols.add(fs)
            print(f"   {rr['name'][:35]:37} total={t} fields={fs}", flush=True)
    print("   distinct field-sets in sample:", len(cols), flush=True)
