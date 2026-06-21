import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
KEY=os.environ.get("DATA_GOV_IN_API_KEY","579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
BASE="https://api.data.gov.in/resource/"
RES={
 "classified-area-LUS":"8a3761be-1b0b-423d-a907-1f99870b365a",
 "crop-wise-irrigated-LUS":"045d034e-524e-4065-ba50-8e781722e8c8",
 "current-daily-price":"9ef84268-d588-465a-a308-a864a43d0070",
 "crop-production":"35be999b-0208-4354-b557-f6ca9a5355de",
 "source-wise-irrigated-LUS":"512a034f-6924-42d8-9a76-d40bfb56424a",
 "operational-holdings":"0a42f538-0ccc-483f-9a4e-17aa9d146b04",
 "total-crop-area-LUS":"56cfa960-d511-45de-8243-6f75ca8d270b",
 "variety-wise-daily-price":"35985678-0d79-46b4-9ed6-6f13308a1d24",
 "pm-kisan-beneficiaries":"388208c6-d82a-4190-90df-91aa2c326fec",
}
def probe(rid):
    for a in range(10):
        r=get(BASE+rid, params={"api-key":KEY,"format":"json","offset":0,"limit":5}, timeout=(10,120))
        if r.status_code==429:
            time.sleep(20); continue
        return r.json()
    return {"error":"still 429"}
for label,rid in RES.items():
    d=probe(rid)
    recs=d.get("records") or []
    cols=list(recs[0].keys()) if recs else []
    print(label.ljust(28),"total=",d.get("total"),"status=",d.get("status"),"err=",d.get("error"),"cols=",cols)
    time.sleep(8)
