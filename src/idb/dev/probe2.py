import sys, io, csv, collections
sys.path.insert(0, 'src')
from subsets_utils import get
BASE = "https://data.iadb.org/api/3/action"
def show(pid):
    return get(f"{BASE}/package_show", params={"id": pid}, timeout=60).json()["result"]

for pid in ("latin-macro-watch-dataset","social-indicators-of-latin-america-and-the-caribbean"):
    rec = show(pid)
    res = [r for r in rec["resources"] if (r.get("format") or "").upper()=="CSV"]
    print(f"\n==== {pid}: {len(res)} csv resources ====")
    # sample first 3 resources' headers + sizes
    hdrs=collections.Counter()
    for rr in res[:5]:
        url = rr.get("url")
        body = get(url, timeout=60).content
        txt = body.decode("utf-8","replace")
        line0 = txt.splitlines()[0] if txt else ""
        rows = txt.count("\n")
        print(f"  res={rr.get('name')[:40]!r:42} bytes={len(body):>8} rows~={rows:>6} hdr={line0[:120]}")
