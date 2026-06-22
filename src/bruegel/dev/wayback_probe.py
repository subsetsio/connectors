import sys
sys.path.insert(0, "src")
from utils import resolve_links, get
PAGES = {
    "sovereign": "/dataset/sovereign-bond-holdings",
    "reer": "/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database",
    "gini": "/dataset/global-and-regional-gini-coefficients-income-inequality",
}
for name, page in PAGES.items():
    try:
        links = resolve_links(page)
        url = links[0]
        print(f"\n[{name}] resolved file: {url}")
        cdx = get("https://web.archive.org/cdx/search/cdx",
                  params={"url": url, "output": "json", "limit": "-5",
                          "filter": "statuscode:200", "fl": "timestamp,length"},
                  timeout=(10.0, 60.0))
        rows = cdx.json()
        print(f"  wayback snapshots: {len(rows)-1 if rows else 0}  -> {rows[1:] if len(rows)>1 else 'NONE'}")
    except Exception as e:
        print(f"[{name}] ERROR: {type(e).__name__}: {e}")
