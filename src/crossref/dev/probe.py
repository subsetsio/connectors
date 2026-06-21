import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json
from subsets_utils import get

MAILTO = "ops@subsets.io"

def hit(url, **params):
    params.setdefault("mailto", MAILTO)
    r = get(url, params=params, timeout=(10.0, 120.0))
    print("URL:", str(r.url))
    print("STATUS:", r.status_code)
    print("RATE HEADERS:", {k:v for k,v in r.headers.items() if 'rate' in k.lower() or 'retry' in k.lower()})
    return r.json()

# 1. members - one page rows=2
print("===== MEMBERS =====")
j = hit("https://api.crossref.org/members", rows=2)
m = j["message"]
print("keys:", list(j.keys()), "| message keys:", list(m.keys()))
print("total-results:", m.get("total-results"), "items-per-page:", m.get("items-per-page"))
print("next-cursor present(default):", "next-cursor" in m)
print("FIRST MEMBER:")
print(json.dumps(m["items"][0], indent=1)[:2500])
