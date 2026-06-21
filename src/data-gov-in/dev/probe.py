import os
from subsets_utils import get
KEY=os.environ.get("DATA_GOV_IN_API_KEY","579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
rid="56f202fe-c935-4a67-9d15-861e295c66d4"
r=get(f"https://api.data.gov.in/resource/{rid}",
      params={"api-key":KEY,"format":"json","offset":0,"limit":3}, timeout=(10,90))
print("status",r.status_code)
d=r.json()
print("envelope keys:", list(d.keys()))
print("total",d.get("total"),"count",d.get("count"),"limit",d.get("limit"),"offset",d.get("offset"))
recs=d.get("records",[])
print("n records",len(recs))
if recs:
    print("record0 keys:", list(recs[0].keys()))
    print("record0:", recs[0])
