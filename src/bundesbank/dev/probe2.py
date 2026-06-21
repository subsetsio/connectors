from subsets_utils import get

url = "https://api.statistiken.bundesbank.de/rest/data/BBZVS01?format=csv"
r = get(url, timeout=(10,120))
lines = r.text.splitlines()
print("=== ALL LINES (first cell only + count cols) ===")
for i, ln in enumerate(lines):
    cells = ln.split(";")
    print(i, "ncols", len(cells), "| first:", repr(cells[0][:40]))
print()
print("=== try standard SDMX-CSV via Accept header ===")
r2 = get(url.replace("?format=csv",""), headers={"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=(10,120))
print("status", r2.status_code, "ctype", r2.headers.get("content-type"))
for ln in r2.text.splitlines()[:5]:
    print(repr(ln[:300]))
