import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
MAILTO="ops@subsets.io"
def hit(url, **p):
    p.setdefault("mailto", MAILTO)
    r = get(url, params=p, timeout=(10.0,120.0)); r.raise_for_status(); return r.json()

print("=== FUNDERS item ===")
j=hit("https://api.crossref.org/funders", rows=1); m=j["message"]
print("total:", m.get("total-results"))
print(json.dumps(m["items"][0], indent=1)[:900])

print("=== JOURNALS top-level keys ===")
j=hit("https://api.crossref.org/journals", rows=1); it=j["message"]["items"][0]
print("keys:", list(it.keys()))
print("title:", repr(it.get("title")), "| ISSN:", it.get("ISSN"), "| publisher:", repr(it.get("publisher")))

print("=== WORKS item flat fields ===")
j=hit("https://api.crossref.org/works", rows=2); items=j["message"]["items"]
for it in items[:1]:
    for k in ["DOI","type","title","container-title","publisher","member","ISSN","published","issued","created","indexed","volume","issue","page","reference-count","is-referenced-by-count","references-count","language","subject","score"]:
        v = it.get(k)
        print(f"  {k}: {json.dumps(v)[:120] if v is not None else None}")

print("=== WORKS index-date filter + cursor ===")
j=hit("https://api.crossref.org/works", rows=1, cursor="*", **{"filter":"from-index-date:2024-01-01,until-index-date:2024-01-01"})
m=j["message"]
print("total in window 2024-01-01:", m.get("total-results"))
