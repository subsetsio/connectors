import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import os
from subsets_utils import get
KEY=os.environ.get("DATA_GOV_IN_API_KEY","579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
BASE="https://api.data.gov.in/resource/"
def probe(rid, label, lim=1000):
    try:
        r=get(BASE+rid, params={"api-key":KEY,"format":"json","offset":0,"limit":lim}, timeout=(10,120))
        r.raise_for_status()
        d=r.json()
        recs=d.get("records") or []
        print(f"[{label}] total={d.get('total')} returned={len(recs)} (asked {lim}) status={d.get('status')}")
        if recs:
            print("   cols:", list(recs[0].keys()))
            print("   row0:", {k:recs[0][k] for k in list(recs[0])[:6]})
    except Exception as e:
        print(f"[{label}] ERROR {type(e).__name__}: {e}")
probe("35be999b-0208-4354-b557-f6ca9a5355de","crop-production")
probe("9ef84268-d588-465a-a308-a864a43d0070","current-daily-mandi")
probe("56cfa960-d511-45de-8243-6f75ca8d270b","total-crop-area-LUS")
probe("ec6ac2b5-cb27-4beb-8a10-8999ef9f47cb","agmarknet-slice")
probe("f1b0c966-eb87-473e-91ff-1764fca44ca7","kcc-slice")
