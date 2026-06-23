import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, configure_http

BASE = "https://clinicaltrials.gov/api/v2/studies"

# Default UA got a 403. Try a descriptive UA.
configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (data integration; contact@subsets.io)"})

params = {
    "pageSize": 3,
    "fields": "NCTId,BriefTitle,OverallStatus,Phases,Conditions,LeadSponsorName",
    "countTotal": "true",
}
r = get(BASE, params=params, timeout=(10, 60))
print("STATUS", r.status_code)
print("REQ UA", r.request.headers.get("user-agent"))
if r.status_code != 200:
    print("BODY", r.text[:500])
else:
    data = r.json()
    print("TOP KEYS", list(data.keys()))
    print("totalCount", data.get("totalCount"))
    print("nextPageToken?", "nextPageToken" in data)
    print("FIRST STUDY:")
    print(json.dumps(data["studies"][0], indent=2)[:2500])
