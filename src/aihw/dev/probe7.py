from subsets_utils import get
import io, csv
CKAN="https://data.gov.au/data/api/3/action"
def hdr(rid):
    u=get(f"{CKAN}/resource_show", params={"id":rid}, timeout=(10,60)).json()["result"]["url"]
    resp=get(u, timeout=(10,120)); 
    txt=resp.content[:4000].decode("utf-8-sig", errors="replace")
    return next(csv.reader(io.StringIO(txt)))
for rid,l in [("7fbac314-4bf9-4601-b812-0307316ef5a4","ACIM Counts"),
              ("c39b4db3-5d92-4cc1-b49d-92e63fc72b77","ACIM Ratio"),
              ("a5de4e7e-d062-4356-9d1b-39f44b1961dc","MORT_1")]:
    print(l,"->",hdr(rid))
