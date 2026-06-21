import sys
sys.path.insert(0, 'src')
from subsets_utils import get
for url,label in [
  ("https://data.iadb.org/file/download/73e73734-9825-47bd-85ea-d78c697b1037","LMW unemployment"),
]:
    body = get(url, timeout=60).content.decode("utf-8","replace")
    lines = body.splitlines()
    print(f"=== {label}: {len(lines)} lines ===")
    for l in lines[:6]: print("  ", l[:160])
# social indicators sample
from subsets_utils import get as g
BASE="https://data.iadb.org/api/3/action"
rec=g(f"{BASE}/package_show",params={"id":"social-indicators-of-latin-america-and-the-caribbean"},timeout=60).json()["result"]
res=[r for r in rec["resources"] if (r.get("format") or "").upper()=="CSV"][:2]
for rr in res:
    body=g(rr["url"],timeout=60).content.decode("utf-8","replace")
    lines=body.splitlines()
    print(f"=== SI {rr['name'][:40]}: {len(lines)} lines ===")
    for l in lines[:4]: print("  ", l[:160])
