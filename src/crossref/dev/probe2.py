import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
MAILTO="ops@subsets.io"
def hit(url, **p):
    p.setdefault("mailto", MAILTO)
    r = get(url, params=p, timeout=(10.0,120.0)); r.raise_for_status(); return r.json()

print("=== CURSOR on members ===")
j = hit("https://api.crossref.org/members", rows=2, cursor="*")
m=j["message"]
print("next-cursor:", m.get("next-cursor","")[:40], "| got", len(m["items"]))

for ep,label in [("journals","JOURNALS"),("funders","FUNDERS")]:
    print(f"=== {label} ===")
    j=hit(f"https://api.crossref.org/{ep}", rows=1)
    m=j["message"]
    print("total:", m.get("total-results"), "msg keys:", list(m.keys()))
    print(json.dumps(m["items"][0], indent=1)[:1200])

print("=== WORKS rows=1 ===")
j=hit("https://api.crossref.org/works", rows=1)
m=j["message"]
print("total:", m.get("total-results"), "msg keys:", list(m.keys()))
print("item keys:", list(m["items"][0].keys()))
print(json.dumps(m["items"][0], indent=1)[:2000])
