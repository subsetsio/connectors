import sys
sys.path.insert(0, 'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
def csv_head(url, label):
    if not (url or "").startswith("http"):
        print(f"=== {label}: SKIP non-http url {url!r}"); return
    body = get(url, timeout=60).content.decode("utf-8","replace")
    lines = body.splitlines()
    print(f"=== {label}: {len(lines)} lines ===")
    for l in lines[:5]: print("  ", l[:150])

csv_head("https://data.iadb.org/file/download/73e73734-9825-47bd-85ea-d78c697b1037","LMW unemployment")
for pid in ("social-indicators-of-latin-america-and-the-caribbean","idb-group-impact-framework-performance-targets-2024-2030-dataset"):
    rec=get(f"{BASE}/package_show",params={"id":pid},timeout=60).json()["result"]
    res=[r for r in rec["resources"] if (r.get("format") or "").upper()=="CSV"][:2]
    for rr in res: csv_head(rr.get("url"), f"{pid[:20]} / {rr['name'][:35]}")
