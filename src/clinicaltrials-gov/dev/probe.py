import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, configure_http

BASE = "https://clinicaltrials.gov/api/v2/studies"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

for desc, hdrs in [
    ("browser-UA+accept", {"User-Agent": UA, "Accept": "application/json"}),
    ("only-accept", {"Accept": "application/json"}),
]:
    configure_http(headers=hdrs)
    try:
        r = get(BASE, params={"pageSize": 2, "fields": "NCTId,BriefTitle,Conditions", "countTotal": "true"}, timeout=(10, 60))
        print(desc, "->", r.status_code, "| sent UA:", r.request.headers.get("user-agent"))
        if r.status_code == 200:
            data = r.json()
            print("  TOP KEYS", list(data.keys()), "totalCount", data.get("totalCount"), "nextToken?", "nextPageToken" in data)
            print("  STUDY0", json.dumps(data["studies"][0])[:800])
            break
        else:
            print("  BODY", r.text[:200])
    except Exception as e:
        print(desc, "EXC", type(e).__name__, str(e)[:200])
