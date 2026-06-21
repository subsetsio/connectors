import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
MAILTO="ops@subsets.io"
def hit(url, **p):
    p.setdefault("mailto", MAILTO)
    r = get(url, params=p, timeout=(10.0,120.0)); r.raise_for_status(); return r.json()

print("=== members top-level keys (rows=1) ===")
it=hit("https://api.crossref.org/members", rows=1)["message"]["items"][0]
print("keys:", list(it.keys()))
print("id:", it.get("id"), "primary-name:", it.get("primary-name"), "location:", it.get("location"))
print("counts:", it.get("counts"))

print("=== works cursor in a date window, page through 2 pages ===")
cursor="*"
for i in range(2):
    m=hit("https://api.crossref.org/works", rows=5, cursor=cursor,
          filter="from-index-date:2015-01-01,until-index-date:2015-01-01")["message"]
    print(f"page{i}: total={m.get('total-results')} got={len(m['items'])} nextcur={m.get('next-cursor','')[:30]}")
    cursor=m.get("next-cursor")
    if not m["items"]: break

print("=== earliest index date probe: sort by indexed asc ===")
m=hit("https://api.crossref.org/works", rows=1, sort="indexed", order="asc")["message"]
it=m["items"][0]
print("earliest indexed:", it.get("indexed",{}).get("date-time"), "DOI:", it.get("DOI"))
