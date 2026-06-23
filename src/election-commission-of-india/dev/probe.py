import os, json
from subsets_utils import get

KEY = os.environ.get("DATA_GOV_IN_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
IDS = [
    "0bd877c0-031d-49da-a743-d102dec6e7b7",
    "194d454f-3ea8-4621-a915-b211c66e46a7",
    "1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd",
    "a27ba4e9-73c2-40d1-90b2-41d71ea7c283",
    "f7f1bf09-7633-4474-96b2-62630c70f33c",
]
for rid in IDS:
    r = get(f"https://api.data.gov.in/resource/{rid}",
            params={"format": "json", "limit": "10", "offset": "0", "api-key": KEY},
            timeout=(10.0, 60.0))
    d = r.json()
    print("===", rid, d.get("title"))
    print("total", d.get("total"), "count", d.get("count"), "limit", d.get("limit"))
    print("fields", [(f["id"], f["type"]) for f in d.get("field", [])])
    print("rec0", json.dumps(d["records"][0], ensure_ascii=False)[:400])
